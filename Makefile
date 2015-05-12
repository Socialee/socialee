# Root of the project (Git repository).
# This gets determined via the Makefile, which can be a symlink.
PROJECT_ROOT?=$(dir $(or $(shell readlink $(firstword $(MAKEFILE_LIST))), $(firstword $(MAKEFILE_LIST))))
# Remove trailing slash.
PROJECT_ROOT:=$(PROJECT_ROOT:%/=%)
PROJECT_ROOT_SRC=$(PROJECT_ROOT)/socialee

# Django settings.
export DJANGO_DEBUG?=1
export DJANGO_SETTINGS_MODULE?=config.settings

# Control the make process.
# Set to 1 for more verbose output, and call `make` with `--debug=v`.
DEBUG:=0
override DEBUG:=$(filter-out 0,$(DEBUG))

# Uncomment this to get more info during the make process,
MY_MAKE_ARGS?=$(if $(DEBUG), --debug=v,)
# Allow to pass on global options for all sub-makes.
MY_MAKE=$(MAKE)$(MY_MAKE_ARGS)

# TODO: $(filter Dev,$(DJANGO_CONFIGURATION))
SCSS_SOURCEMAPS:=1

BUILD_DIR:=$(PROJECT_ROOT)/build
CACHE_DIR=$(BUILD_DIR)/cache
BUNDLER_DIR:=$(CACHE_DIR)/bundler

# Install sass via bundler (Gemfile).
export GEM_HOME:=$(CACHE_DIR)/gems
BUNDLER_BIN:=$(GEM_HOME)/bin/bundle
SCSS_BIN:=$(BUNDLER_DIR)/bin/scss

$(SCSS_BIN): $(BUNDLER_BIN)
	$(BUNDLER_BIN) install --path $(BUNDLER_DIR) --binstubs $(BUNDLER_DIR)/bin

$(BUNDLER_BIN):
	gem install bundler

BOWER_COMPONENTS_ROOT:=socialee/static
BOWER_COMPONENTS:=$(BOWER_COMPONENTS_ROOT)/bower_components

MAIN_SCSS:=socialee.scss

SCSS_DIR=$(PROJECT_ROOT_SRC)/static/scss
CSS_DIR=$(PROJECT_ROOT_SRC)/static/css
SCSS_FILES=$(addprefix $(SCSS_DIR)/, $(MAIN_SCSS))
CSS_FILES=$(patsubst $(SCSS_DIR)/%.scss,$(CSS_DIR)/%.css,$(SCSS_FILES))
SCSS_COMPONENTS:=$(wildcard $(BOWER_COMPONENTS)/foundation/scss/foundation/components/*.scss)
SCSS_RUN_NO_SOURCEMAP:=$(SCSS_BIN) --quiet --cache-location /tmp/sass-cache \
	 -I $(BOWER_COMPONENTS)
SCSS_RUN:=$(SCSS_RUN_NO_SOURCEMAP) \
	 $(if $(SCSS_SOURCEMAPS),--sourcemap,)

NOTIFY_SEND:=$(shell which notify-send >/dev/null 2>&1 && echo notify-send || true)
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
	&& sed -i.bak '$$ s/\.tmp\.map/.map/' $@.tmp \
	&& mv $@.tmp $@ \
	&& mv $@.tmp.map $@.map \
	&& $(RM) $@.tmp.bak
$(SCSS_DIR)/$(MAIN_SCSS): $(SCSS_DIR)/_settings.scss $(SCSS_COMPONENTS)
	touch $@

run:
	python manage.py runserver

# Install bower components.
bower_install:
	@# Create the bower_components folder manually. "bower install" does not respect umask/acl!
	@# NOTE: messed up because of umask not being effective from /.bashrc (in Docker)?
	mkdir -p -m 775 $(BOWER_COMPONENTS)
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

TOX_BIN=$(command -v tox)
install_testing_req:
	pip install -r requirements/testing.txt

# TODO: look at $(DATABASE_URL) to use py34-psql/py34-sqlite.
test: $(if $(TOX_BIN),,install_testing_req)
	tox -e py34-psql
	@# tox -e py34

test_heroku:
	@# tox fails to build Pillow on Heroku.
	@# Fails, because it cannot connect to "postgres"; https://code.djangoproject.com/ticket/16969
	@# DATABASE_URL=$(HEROKU_POSTGRESQL_MAUVE_URL) py.test --strict -r fEsxXw tests
	DATABASE_URL=sqlite:///:memory: py.test --strict -r fEsxXw tests

test_sqlite:
	tox -e py34-sqlite

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
heroku_post_compile: check test_heroku static migrate


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
