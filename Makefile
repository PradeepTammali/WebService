SHELL := /bin/bash

.PHONY: setup install lint lint-clean test run

setup:
	pipenv install --dev
	pipenv run pre-commit install

install:
	pipenv install

lint:
	pipenv run pre-commit run --all-files

lint-clean:
	pipenv run pre-commit clean
	pipenv run pre-commit gc

test:
	pipenv run pytest tests/*

run:
	pipenv run python run.py
