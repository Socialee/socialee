# Root of the project (Git repository).
# This gets determined via the Makefile, which can be a symlink.
PROJECT_ROOT?=$(dir $(or $(shell readlink $(firstword $(MAKEFILE_LIST))), $(firstword $(MAKEFILE_LIST))))
# Remove trailing slash.
PROJECT_ROOT:=$(PROJECT_ROOT:%/=%)
PROJECT_ROOT_SRC=$(PROJECT_ROOT)/socialee

DEBUG:=1

export DJANGO_DEBUG?=$(DEBUG)
export DJANGO_SETTINGS_MODULE?=config.settings

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
$(if $(NOTIFY_SEND),$(NOTIFY_SEND) $(1),)
endef

scss: $(CSS_FILES)
$(CSS_DIR)/%.css: $(SCSS_DIR)/%.scss | $(BOWER_COMPONENTS) $(SCSS_BIN)
	@echo "SCSS: building $@"
	@mkdir -p $(CSS_DIR)
	$(if $(DEBUG),,@)r=$$($(SCSS_RUN) $< $@.tmp 2>&1) || { \
		$(call func-notify-send, "scss failed: $$r"); \
		echo "ERROR: scss failed: $$r"; echo "command: $(SCSS_RUN) $< $@.tmp"; exit 1; } \
	&& { head -n1 $@.tmp | grep -q "@charset" || sed -i '1 i@charset "UTF-8";' $@.tmp; } \
	&& sed -i '$ s/\.tmp\.map/.map/' $@.tmp \
	&& mv $@.tmp $@ \
	&& mv $@.tmp.map $@.map
$(SCSS_DIR)/$(MAIN_SCSS): $(SCSS_DIR)/_settings.scss $(SCSS_COMPONENTS)
	touch $@

run:
	python manage.py runserver

# Install bower components.
bower_install:
	# Create the bower_components folder manually. "bower install" does not respect umask/acl!
	# NOTE: messed up because of umask not being effective from /.bashrc (in Docker)?
	mkdir -p -m 775 $(BOWER_COMPONENTS)
	cd $(BOWER_COMPONENTS_ROOT) && bower install $(BOWER_OPTIONS)

# NOTE: controlled via env vars from Docker.
$(BOWER_COMPONENTS): $(BOWER_COMPONENTS_ROOT)/bower.json
	make bower_install
	touch $@

static: $(BOWER_COMPONENTS) scss collectstatic

# Collect static files from DJANGO_STATICFILES etc to STATIC_ROOT.
collectstatic: $(BOWER_COMPONENTS)
	@echo "Collecting static files..."
	python manage.py collectstatic -v0 --noinput --ignore *.scss --ignore bower.json

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
	$(MAKE_WITH_MAKEFILE) requirements

# Compile/build requirements.txt files from .in files, using pip-compile.
$(PIP_REQUIREMENTS_DIR)/%.txt: $(PIP_REQUIREMENTS_DIR)/%.in | $(PIP_COMPILE)
	pip-compile $< > $@

.PHONY: requirements requirements_rebuild
# }}}
