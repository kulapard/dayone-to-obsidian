APP_DIR = dayone_to_obsidian

install-dev:
	uv sync

test:
	uv run pytest -vv --cov=$(APP_DIR) --cov-report=term --cov-report=xml

build:
	uv build

pre-commit:
	uv run pre-commit run --all-files

pre-commit-update:
	uv run pre-commit autoupdate

mypy:
	uv run mypy ${APP_DIR}

vulture:
	uv run vulture ${APP_DIR}

lint: pre-commit mypy

.PHONY: install-dev test build pre-commit pre-commit-update mypy vulture lint
