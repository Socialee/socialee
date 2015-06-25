# Root of the project (Git repository).
# This gets determined via the Makefile, which can be a symlink.
PROJECT_ROOT?=$(dir $(or $(shell readlink $(firstword $(MAKEFILE_LIST))), $(firstword $(MAKEFILE_LIST))))
# Remove trailing slash.
PROJECT_ROOT:=$(PROJECT_ROOT:%/=%)
PROJECT_ROOT_SRC=$(PROJECT_ROOT)/socialee

# Django settings.
export DJANGO_DEBUG?=1
override DJANGO_DEBUG:=$(filter-out 0,$(DJANGO_DEBUG))
export DJANGO_SETTINGS_MODULE?=config.settings

# Control the make process.
# Set to 1 for more verbose output, and call `make` with `--debug=v`.
DEBUG:=0
override DEBUG:=$(filter-out 0,$(DEBUG))


# Default target.
all: dev

# Uncomment this to get more info during the make process.
MY_MAKE_ARGS?=$(if $(DEBUG), --debug=v,)
# Allow to pass on global options for all sub-makes.
MY_MAKE=$(MAKE)$(MY_MAKE_ARGS)

# TODO: $(filter Dev,$(DJANGO_CONFIGURATION))
USE_SCSS_SOURCEMAPS:=$(DJANGO_DEBUG)

# Pick up CACHE_DIR from Heroku.
CACHE_DIR?=build/cache
CACHE_DIR_ABS:=$(abspath $(CACHE_DIR))
BUNDLER_DIR:=$(CACHE_DIR)/bundler

# Use cache/storage with Bower.
export bower_storage__packages:=$(CACHE_DIR_ABS)/bower/packages
export bower_storage__registry:=$(CACHE_DIR_ABS)/bower/registry

# Install sass via bundler (Gemfile).
export GEM_HOME:=$(CACHE_DIR)/rubygems
GEM_PATH:=$(GEM_HOME):$(GEM_PATH)

# Use existing bundler from PATH, or install it through rubygems.
BUNDLER_BIN:=$(shell command -v bundle || true)
ifeq ($(BUNDLER_BIN),)
BUNDLER_BIN:=$(GEM_HOME)/bin/bundle
$(BUNDLER_BIN):
	gem install bundler
endif

# Install scss through Gemfile.
SCSS_BIN:=$(BUNDLER_DIR)/bin/scss
$(SCSS_BIN): | $(BUNDLER_BIN) .bundle/config
.bundle/config:
	$(BUNDLER_BIN) install --path $(BUNDLER_DIR) --binstubs $(BUNDLER_DIR)/bin

BOWER_COMPONENTS_ROOT:=socialee/static
BOWER_COMPONENTS:=$(BOWER_COMPONENTS_ROOT)/bower_components

MAIN_SCSS:=socialee.scss

SCSS_DIR=$(PROJECT_ROOT_SRC)/static/scss
CSS_DIR=$(PROJECT_ROOT_SRC)/static/css
SCSS_FILES=$(addprefix $(SCSS_DIR)/, $(MAIN_SCSS) admin.scss)
CSS_FILES=$(patsubst $(SCSS_DIR)/%.scss,$(CSS_DIR)/%.css,$(SCSS_FILES))

# SCSS dependencies/includes for main scss.
SCSS_COMPONENTS:=$(wildcard $(BOWER_COMPONENTS)/foundation/scss/foundation/components/*.scss)
SCSS_COMPONENTS+=$(addprefix $(BOWER_COMPONENTS)/,\
	slick.js/slick/slick.scss \
	fullpage.js/jquery.fullPage.scss \
	foundation-icon-fonts/_foundation-icons.scss \
	)

SCSS_RUN_NO_SOURCEMAP:=$(SCSS_BIN) --quiet --cache-location /tmp/sass-cache \
	 -I $(BOWER_COMPONENTS)
SCSS_RUN:=$(SCSS_RUN_NO_SOURCEMAP) \
	 $(if $(USE_SCSS_SOURCEMAPS),--sourcemap,)

NOTIFY_SEND:=$(shell command -v notify-send >/dev/null 2>&1 && echo notify-send || true)
define func-notify-send
$(if $(NOTIFY_SEND),$(NOTIFY_SEND) $(1),:)
endef


# Build sass/scss files.
# They get written to a tmp file first, and only moved on success.
# The sourcemap reference gets fixed, and "@charset" gets added (for
# consistency across different Ruby versions).  My "scss" keeps removing
# them, while another one might add add them again.
scss: $(CSS_FILES)
$(CSS_DIR)/%.css: $(SCSS_DIR)/%.scss | $(BOWER_COMPONENTS) $(SCSS_BIN)
	@echo "SCSS: building $@"
	@mkdir -p $(CSS_DIR)
	$(if $(DEBUG),,@)r=$$($(SCSS_RUN) $< $@.tmp 2>&1) || { \
		$(call func-notify-send, "scss failed: $$r"); \
		echo "ERROR: scss failed: $$r"; echo "command: $(SCSS_RUN) $< $@.tmp"; exit 1; } \
	&& { head -n1 $@.tmp | grep -q "@charset" || { \
		echo '@charset "UTF-8";' | cat - $@.tmp >$@.tmp2; mv $@.tmp2 $@.tmp; };} \
	$(if $(USE_SCSS_SOURCEMAPS),\
		&& sed -i.bak '$$ s/\.tmp\.map/.map/' $@.tmp \
		&& mv $@.tmp.map $@.map,) \
	&& mv $@.tmp $@ \
	&& $(RM) $@.tmp.bak
$(SCSS_DIR)/$(MAIN_SCSS): $(SCSS_DIR)/_settings.scss $(SCSS_COMPONENTS)
	touch $@

scss_force:
	touch $(SCSS_FILES)
	$(MY_MAKE) scss

# Watch
watch:
	bin/devserver livereload_only

run:
	python manage.py runserver

# Main target for development.
# TODO: start tmux with watch process.
dev: migrate run

# Install bower components.
bower_install:
	@# Create the bower_components folder manually. "bower install" does not respect umask/acl!
	@# NOTE: messed up because of umask not being effective from /.bashrc (in Docker)?
	mkdir -p -m 775 $(BOWER_COMPONENTS)
	@# Create registry cache for bower manually, otherwise it fails silently.
	mkdir -p $(bower_storage__registry)
	cd $(BOWER_COMPONENTS_ROOT) && bower install $(BOWER_OPTIONS)

# NOTE: controlled via env vars from Docker.
$(BOWER_COMPONENTS): $(BOWER_COMPONENTS_ROOT)/bower.json
	$(MY_MAKE) bower_install
	touch $@

static: $(BOWER_COMPONENTS) scss collectstatic

# Collect static files from DJANGO_STATICFILES etc to STATIC_ROOT.
collectstatic: $(BOWER_COMPONENTS)
	@echo "Collecting static files..."
	python manage.py collectstatic -v0 --noinput --ignore *.scss --ignore bower.json

migrate:
	python manage.py migrate

migrate_deploy:
	python manage.py migrate --noinput

TOX_BIN=$(shell command -v tox || true)
install_testing_req:
	pip install -r requirements/testing.txt

# Default test target: install reqs, and call test_psql/test_sqlite.
test: $(if $(TOX_BIN),,install_testing_req)
# look at $(DATABASE_URL) to use py34-psql/py34-sqlite.
test: $(if $(findstring postgresql:,$(DATABASE_URL)),test_psql,test_sqlite)

test_sqlite:
	tox -e py34-sqlite

test_psql:
	tox -e py34-psql

test_heroku:
	@# tox fails to build Pillow on Heroku.
	@# Fails, because it cannot connect to "postgres"; https://code.djangoproject.com/ticket/16969
	@# DATABASE_URL=$(HEROKU_POSTGRESQL_MAUVE_URL) py.test --strict -r fEsxXw tests
	DATABASE_URL=sqlite:///:memory: py.test --strict -r fEsxXw --create-db tests

checkqa:
	tox -e checkqa

check: check_migrated
	python manage.py check
	# python manage.py check --deploy

check_migrated:
	# Check that there are no DB changes (missing migrations).
	@# Exits with 1 if there are no changes.
	@# --noinput works with 1.9+ only.
	python manage.py makemigrations --exit --dry-run --noinput; \
		ret=$$?; \
		if [ $$ret != 1 ]; then \
			echo 'There are DB changes that need a migration!'; \
			exit 1; \
		fi

deploy_check: check test

deploy: deploy_check static migrate

# Run via bin/post_compile for Heroku.
heroku_post_compile: check static test_heroku migrate_deploy


# Requirements files. {{{
# Define different requirements files.
PIP_REQUIREMENTS_DIR=$(PROJECT_ROOT)/requirements
PIP_REQUIREMENTS_BASE:=$(PIP_REQUIREMENTS_DIR)/base.txt
PIP_REQUIREMENTS_DEV:=$(PIP_REQUIREMENTS_DIR)/dev.txt
PIP_REQUIREMENTS_PRODUCTION:=$(PIP_REQUIREMENTS_DIR)/production.txt
PIP_REQUIREMENTS_HEROKU:=$(PIP_REQUIREMENTS_DIR)/heroku.txt
PIP_REQUIREMENTS_TESTING:=$(PIP_REQUIREMENTS_DIR)/testing.txt

# Inner-dependencies / includes.
$(PIP_REQUIREMENTS_DEV): $(PIP_REQUIREMENTS_BASE)
$(PIP_REQUIREMENTS_TESTING): $(PIP_REQUIREMENTS_DEV)
$(PIP_REQUIREMENTS_PRODUCTION): $(PIP_REQUIREMENTS_BASE)
$(PIP_REQUIREMENTS_HEROKU): $(PIP_REQUIREMENTS_PRODUCTION)

PIP_REQUIREMENTS_ALL:=$(PIP_REQUIREMENTS_BASE) $(PIP_REQUIREMENTS_DEV) $(PIP_REQUIREMENTS_TESTING) $(PIP_REQUIREMENTS_PRODUCTION) $(PIP_REQUIREMENTS_HEROKU)
requirements: $(PIP_REQUIREMENTS_ALL)
requirements_rebuild:
	$(RM) $(PIP_REQUIREMENTS_ALL)
	$(MY_MAKE) requirements

# Compile/build requirements.txt files from .in files, using pip-compile.
$(PIP_REQUIREMENTS_DIR)/%.txt: $(PIP_REQUIREMENTS_DIR)/%.in
	pip-compile $< > $@

.PHONY: requirements requirements_rebuild
# }}}
