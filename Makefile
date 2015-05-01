# Root of the project (Git repository).
# This gets determined via the Makefile, which can be a symlink.
PROJECT_ROOT?=$(dir $(or $(shell readlink $(firstword $(MAKEFILE_LIST))), $(firstword $(MAKEFILE_LIST))))
# Remove trailing slash.
PROJECT_ROOT:=$(PROJECT_ROOT:%/=%)
PROJECT_ROOT_SRC=$(PROJECT_ROOT)/src

export DJANGO_DEBUG?=1
export DJANGO_SETTINGS_MODULE?=config.settings

run:
	python manage.py runserver

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
