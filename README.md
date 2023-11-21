# WebService

## Setup

### Development

Install

python
pip

and install pipenv using this with the command

pip install pipenv


pipenv install

pre-commit install

pre-commit run --all-files - for first time.

push will be successfull even if there are failed checks for the unstaged changes(non commited files).
https://github.com/pre-commit/pre-commit/issues/2486

pre-commit clean (rm -rf ~/.cache/pre-commit)  --- clean pre-commit cache
pre-commit gc - clean unused cached repos
pre-commit uninstall - uninstall pre-commit hooks
rm -rf .git/hooks/* -- remove existing hooks
