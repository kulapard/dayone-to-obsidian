APP_DIR = dayone_to_obsidian
PROJECT_NAME = dayone-to-obsidian

pyenv:
	echo $(PROJECT_NAME) > .python-version && pyenv install -s 3.11.4 && pyenv virtualenv -f 3.11.4 $(PROJECT_NAME)

delete-pyenv:
	pyenv virtualenv-delete -f $(PROJECT_NAME)

install:
	pip install --upgrade pip
	pip install -U -r requirements.txt

install-dev: install
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

requirements:
	@echo "Generating requirements.txt"
	@pip-compile --resolver=backtracking -r -U --no-emit-index-url -o requirements.txt requirements.in
	@echo "Generating requirements-dev.txt"
	@pip-compile --resolver=backtracking -r -U --no-emit-index-url -o requirements-dev.txt requirements-dev.in

.PHONY: install install-dev test pre-commit pre-commit-update mypy vulture lint requirements
