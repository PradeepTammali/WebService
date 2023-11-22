SHELL := /bin/bash

.PHONY: setup install lint test run clean-setup clean-lint all clean

setup:
	pipenv install --dev
	pipenv run pre-commit install
	pipenv run pre-commit install --hook-type commit-msg

install:
	pipenv install

lint:
	pipenv run pre-commit run --all-files

test:
	pipenv run pytest tests/*

run:
	pipenv run python run.py

clean-setup:
	pipenv run pre-commit uninstall --hook-type commit-msg
	pipenv run pre-commit uninstall
	pipenv clean

clean-lint:
	pipenv run pre-commit clean
	pipenv run pre-commit gc

all: setup lint run

clean: clean-lint clean-setup
