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


pull request suggestions:
1. if there is only one commit, the PR will take the first line as title and rest as description
2. If there are multiple commits, the PR will take branch name as title leaving the description is empty

These two approches are good:
Small changes with single commits
and a little bit big change with multiple commits

Don't make a PR with lot of changes in a single PR, it will be hard to review.
