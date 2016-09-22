# Root of the project (Git repository).
# This gets determined via the Makefile, which can be a symlink.
PROJECT_ROOT?=$(dir $(or $(shell readlink $(firstword $(MAKEFILE_LIST))), $(firstword $(MAKEFILE_LIST))))
# Remove trailing slash.
PROJECT_ROOT:=$(PROJECT_ROOT:%/=%)
PROJECT_ROOT_SRC=$(PROJECT_ROOT)/socialee

PROJECT_APPS:=socialee

# Django settings.
export DJANGO_DEBUG?=1
override DJANGO_DEBUG:=$(filter-out 0,$(DJANGO_DEBUG))
export DJANGO_SETTINGS_MODULE?=config.settings

# Control the make process.
# Set to 1 for more verbose output, and call `make` with `--debug=v`.
DEBUG:=0
override DEBUG:=$(filter-out 0,$(DEBUG))

# This is required for "exit 1" to work in the sassc rule (with missing sassc).
SHELL=/bin/bash -o pipefail

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

BOWER_COMPONENTS_ROOT:=socialee/static
BOWER_COMPONENTS:=$(BOWER_COMPONENTS_ROOT)/bower_components
STAMP_BOWER_COMPONENTS_INSTALLED:=$(BOWER_COMPONENTS)/.installed_stamp

MAIN_SCSS:=socialee_global.scss

SCSS_DIR=$(PROJECT_ROOT_SRC)/static/scss
CSS_DIR=$(PROJECT_ROOT_SRC)/static/css
SCSS_FILES=$(filter-out $(wildcard $(SCSS_DIR)/_*.scss),$(wildcard $(SCSS_DIR)/*.scss))
CSS_FILES=$(patsubst $(SCSS_DIR)/%.scss,$(CSS_DIR)/%.css,$(SCSS_FILES))

define info-debug-var
$(info => $(if $(2),$(2),$(1)): '$($(1))'  (from $(origin $(1)), $(flavor $(1))))
endef
$(if $(DEBUG),$(call info-debug-var,CSS_DIR)\
  $(call info-debug-var,CSS_FILES)\
  $(call info-debug-var,SCSS_DIR)\
  $(call info-debug-var,SCSS_FILES)\
  $(call info-debug-var,PROJECT_ROOT)\
  $(call info-debug-var,CURDIR),)

# SCSS dependencies/includes for main scss.
FOUNDATION_ROOT:=$(BOWER_COMPONENTS)/foundation-sites
SCSS_COMPONENTS=$(wildcard $(FOUNDATION_ROOT)/scss/*/*.scss)
# Known scss files that are expected to exist after "bower_install".
SCSS_COMPONENTS+=$(addprefix $(BOWER_COMPONENTS)/,\
	slick.js/slick/slick.scss \
	fullpage.js/jquery.fullPage.scss \
	foundation-icon-fonts/_foundation-icons.scss \
	)

SCSS_RUN_NO_SOURCEMAP:=sassc -I $(BOWER_COMPONENTS) -I $(FOUNDATION_ROOT)/scss
SCSS_RUN:=$(SCSS_RUN_NO_SOURCEMAP) $(if $(USE_SCSS_SOURCEMAPS),--sourcemap,)

NOTIFY_SEND:=$(shell command -v notify-send >/dev/null 2>&1 && echo notify-send || true)
define func-notify-send
$(if $(NOTIFY_SEND),$(NOTIFY_SEND) $(1),:)
endef


# Build sass/scss files.
# They get written to a tmp file first, and only moved on success.
# The sourcemap reference gets fixed, and "@charset" gets added (for
# consistency across different Ruby versions).  My "scss" keeps removing
# them, while another one might add add them again.
SASSC_LOCKFILE=/tmp/scss.lock
scss: $(CSS_FILES)
$(CSS_DIR)/%.css: $(SCSS_DIR)/%.scss $(STAMP_BOWER_COMPONENTS_INSTALLED)
	@echo "SCSS: building $@"
	@mkdir -p $(CSS_DIR)
	$(if $(DEBUG),,@)\
		while [ -e $(SASSC_LOCKFILE) ] && kill -0 $$(cat $(SASSC_LOCKFILE)); do \
			echo "Waiting for lock.."; sleep 1; done; \
		trap "rm -f $(SASSC_LOCKFILE); exit" INT TERM EXIT; echo $$$$ > $(SASSC_LOCKFILE); \
		r=$$($(SCSS_RUN) $< $@.tmp 2>&1) || { \
		$(call func-notify-send, "scss failed: $$r"); \
		echo "ERROR: scss failed: $$r" >&2; \
		echo "command: $(SCSS_RUN) $< $@.tmp" >&2; \
		exit 1; } \
	&& { head -n1 $@.tmp | grep -q "@charset" || { \
		echo '@charset "UTF-8";' | cat - $@.tmp >$@.tmp2; mv $@.tmp2 $@.tmp; };} \
	$(if $(USE_SCSS_SOURCEMAPS),\
		&& sed -i.bak '$$ s/\.tmp\.map/.map/' $@.tmp \
		&& mv $@.tmp.map $@.map,) \
	&& mv $@.tmp $@ \
	&& $(RM) $@.tmp.bak $(SASSC_LOCKFILE)
$(SCSS_DIR)/$(MAIN_SCSS): $(SCSS_DIR)/_settings.scss $(SCSS_COMPONENTS)
	touch $@

scss_force:
	for f in $(SCSS_FILES); do test -f $$f && touch $$f; done
	$(MY_MAKE) scss

scss_with_dep:
	touch $(SCSS_DIR)/$(MAIN_SCSS)
	$(MY_MAKE) scss

# Watch
watch: scss
	bin/devserver livereload_only

run: DJANGO_DEBUG=1
run:
	DJANGO_DEBUG=$(DJANGO_DEBUG) python manage.py runserver $(RUNSERVER_ARGS)

run_public: RUNSERVER_ARGS=0.0.0.0:8001
run_public: DJANGO_DEBUG=0
run_public: 
	DJANGO_DEBUG=$(DJANGO_DEBUG) python manage.py runserver $(RUNSERVER_ARGS)

run_public_debug: RUNSERVER_ARGS=0.0.0.0:8001
run_public_debug: DJANGO_DEBUG=1
run_public_debug:
	DJANGO_DEBUG=$(DJANGO_DEBUG) python manage.py runserver $(RUNSERVER_ARGS)

run_heroku:
	gunicorn config.wsgi:application_with_static

# Main target for development.
# TODO: start tmux with watch process.
dev: DJANGO_DEBUG=1
dev: install_dev_requirements migrate static run

install_dev_requirements:
	pip install -r requirements/dev.txt

# Install bower components.
bower_install: $(STAMP_BOWER_COMPONENTS_INSTALLED)
$(STAMP_BOWER_COMPONENTS_INSTALLED): $(BOWER_COMPONENTS_ROOT)/bower.json
	@# Create the bower_components folder manually. "bower install" does not respect umask/acl!
	@# NOTE: messed up because of umask not being effective from /.bashrc (in Docker)?
	mkdir -p -m 775 $(BOWER_COMPONENTS)
	@# Create registry cache for bower manually, otherwise it fails silently.
	mkdir -p $(bower_storage__registry)
	cd $(BOWER_COMPONENTS_ROOT) \
		&& bower install -f --force-latest $(BOWER_OPTIONS) \
		&& bower prune
	touch $@

static: $(STAMP_BOWER_COMPONENTS_INSTALLED) scss collectstatic

# Collect static files from DJANGO_STATICFILES etc to STATIC_ROOT.
collectstatic: $(STAMP_BOWER_COMPONENTS_INSTALLED)
	@echo "Collecting static files..."
	python manage.py collectstatic -v0 --noinput --ignore *.scss --ignore bower.json

migrations:
	python manage.py makemigrations

migrate:
	python manage.py migrate

migrate_deploy:
	python manage.py migrate --noinput

TOX_BIN=$(shell command -v tox || true)
install_testing_req:
	pip install -r requirements/testing.txt

# Default test target: install reqs, and call test_psql/test_sqlite.
test: $(if $(TOX_BIN),,install_testing_req)
# look at $(DATABASE_URL) to use py35-psql/py35-sqlite.
test: $(if $(findstring postgresql:,$(DATABASE_URL)),test_psql,test_sqlite)

test_createdb: TEST_OPTIONS:=--create-db
test_createdb: test

test_sqlite:
	tox -e py35-sqlite -- tests $(TEST_OPTIONS)

test_psql:
	tox -e py35-psql -- tests $(TEST_OPTIONS)

test_heroku:
	@# tox fails to build Pillow on Heroku.
	@# Fails, because it cannot connect to "postgres"; https://code.djangoproject.com/ticket/16969
	@# DATABASE_URL=$(HEROKU_POSTGRESQL_MAUVE_URL) py.test --strict -r fEsxXw tests
	env DATABASE_URL=sqlite:///:memory: SKIP_BROWSER_TESTS=1 \
		py.test --strict -r fEsxXw --create-db --runslow tests

checkqa:
	tox -e checkqa

check: check_migrated
	python manage.py check
	# python manage.py check --deploy

check_migrated:
	# Check that there are no DB changes (missing migrations).
	@# Exits with 1 if there are no changes.
	@# --noinput works with 1.9+ only.
	python manage.py makemigrations --exit --dry-run --noinput $(PROJECT_APPS); \
		ret=$$?; \
		if [ $$ret != 1 ]; then \
			echo 'There are DB changes that need a migration!'; \
			exit 1; \
		fi

deploy_check: check test

deploy: deploy_check static migrate

deploy_staging:
	git push staging staging:master

# Gets run via bin/post_compile for Heroku.
HEROKU_ZETTELS_MEDIA:=$(CURDIR)/.heroku/media-zettels
heroku_post_compile: check test_heroku static migrate_deploy 

# Fetch zettels media from separate repo (via https mirror (manually synced)).
heroku_fetch_zettels:
	mkdir -p $(HEROKU_ZETTELS_MEDIA) \
		&& cd $(HEROKU_ZETTELS_MEDIA) \
		&& wget -A '*.jpg' -r -nc -np --no-check-certificate \
			https://codeprobe.de/spool/i/socialee-zettels-kae6cesh7laeFah/ \
		&& mkdir -p $$BUILD_DIR/media \
		&& cd $$BUILD_DIR/media \
		&& ! test -e zettels \
		&& ln -s $(HEROKU_ZETTELS_MEDIA)/codeprobe.de/spool/i/socialee-zettels-kae6cesh7laeFah zettels

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
$(PIP_REQUIREMENTS_HEROKU): $(PIP_REQUIREMENTS_TESTING) $(PIP_REQUIREMENTS_PRODUCTION)

PIP_REQUIREMENTS_ALL:=$(PIP_REQUIREMENTS_BASE) $(PIP_REQUIREMENTS_DEV) $(PIP_REQUIREMENTS_TESTING) $(PIP_REQUIREMENTS_PRODUCTION) $(PIP_REQUIREMENTS_HEROKU)
requirements: $(PIP_REQUIREMENTS_ALL)
requirements_rebuild:
	@depcache=$$(python -c 'from piptools.cache import DependencyCache as DC; \
	             print(DC()._cache_file)'); \
	if [ -f "$$depcache" ]; then \
	  echo "Removing $$depcache"; \
	  $(RM) $$depcache; \
	fi
	$(RM) $(PIP_REQUIREMENTS_ALL)
	$(MY_MAKE) requirements

# Compile/build requirements.txt files from .in files, using pip-compile.
$(PIP_REQUIREMENTS_DIR)/%.txt: $(PIP_REQUIREMENTS_DIR)/%.in
	pip-compile --no-header --output-file "$@.tmp" "$<" >/tmp/pip-compile.out.tmp || { \
	  ret=$$?; echo "pip-compile failed:" >&2; cat /tmp/pip-compile.out.tmp >&2; \
	  $(RM) "$@.tmp" /tmp/pip-compile.out.tmp; \
	  exit $$ret; }
	@sed -n '1,10 s/# Depends on/-r/; s/\.in/.txt/p' "$<" > "$@"
	@cat "$@.tmp" >> "$@"
	@$(RM) "$@.tmp" /tmp/pip-compile.out.tmp

.PHONY: requirements requirements_rebuild
# }}}

OPEN=$(shell hash xdg-open 2>/dev/null && echo xdg-open || echo open)
models.png:
	python manage.py graph_models socialee auth | dot -Tpng > models.png
	$(OPEN) models.png
.PHONY: models.png
