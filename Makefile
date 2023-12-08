APP_DIR = dayone_to_obsidian
PROJECT_NAME = dayone-to-obsidian

pyenv:
	echo $(PROJECT_NAME) > .python-version && pyenv install -s 3.11.4 && pyenv virtualenv -f 3.11.4 $(PROJECT_NAME)

delete-pyenv:
	pyenv virtualenv-delete -f $(PROJECT_NAME)

install-dev:
	pip install --upgrade pip
	pip install -U -r requirements-dev.txt

test:
	pytest -vv --cov=$(APP_DIR)

build:
	python -m build

pre-commit:
	pre-commit run --all-files

pre-commit-update:
	pre-commit autoupdate

mypy:
	mypy ${APP_DIR}

vulture:
	vulture ${APP_DIR}

lint: pre-commit mypy

bump-version-major:
	hatchling version major

bump-version-minor:
	hatchling version minor

bump-version-fix:
	hatchling version fix

commit-version:
	git add $(APP_DIR)/__init__.py
	git commit -m "Bump version to \`$(shell hatchling version)\`"

.PHONY: install-dev test pre-commit pre-commit-update mypy vulture lint bump-version-major bump-version-minor bump-version-fix
