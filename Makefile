# Makefile for Django commands

PYTHON = python
MANAGE_PY = $(PYTHON) manage.py

# Define targets
makemigrations:
	$(MANAGE_PY) makemigrations

migrate:
	$(MANAGE_PY) migrate

runserver:
	$(MANAGE_PY) runserver

test:
	export DJANGO_SETTINGS_MODULE=flags_game_site.settings
	pytest

# Shortcut aliases
mm: makemigrations
m: migrate
rs: runserver
