include tools/make/common.mk

# Setup targets for each package
.PHONY: setup-core
setup-core:
	cd packages/pepperpy-core && poetry lock --no-update && poetry install

.PHONY: setup-db
setup-db:
	cd packages/pepperpy-db && poetry lock --no-update && poetry install

.PHONY: setup-console
setup-console:
	cd packages/pepperpy-console && poetry lock --no-update && poetry install

.PHONY: setup-codebase
setup-codebase:
	cd packages/pepperpy-codebase && poetry lock --no-update && poetry install

.PHONY: setup-files
setup-files:
	cd packages/pepperpy-files && poetry lock --no-update && poetry install

.PHONY: setup-ai
setup-ai:
	cd packages/pepperpy-ai && poetry lock --no-update && poetry install

.PHONY: setup-tools
setup-tools:
	cd tools && poetry lock && poetry install

# Target para atualizar todos os locks
.PHONY: update-locks
update-locks:
	@echo "Updating poetry.lock files..."
	cd packages/pepperpy-core && poetry lock
	cd packages/pepperpy-db && poetry lock
	cd packages/pepperpy-console && poetry lock
	cd packages/pepperpy-codebase && poetry lock
	cd packages/pepperpy-files && poetry lock
	cd packages/pepperpy-ai && poetry lock
	cd tools && poetry lock

.PHONY: setup
setup: update-locks setup-core setup-db setup-console setup-codebase setup-files setup-ai setup-tools

# Linting
.PHONY: lint
lint:
	@ruff check . --config=ruff.toml
	@black --check . --config=.black.toml
	@mypy .

# Formatting
.PHONY: format
format:
	@ruff check . --fix --config=ruff.toml
	@black . --config=.black.toml

# Testing
.PHONY: test
test:
	@pytest

# Documentation
.PHONY: docs
docs:
	@mkdocs serve

# Build
.PHONY: build
build:
	@python -m tools.build.poetry
