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

.PHONY: clean
clean:
	rm -rf .pytest_cache
	rm -rf .coverage
	rm -rf htmlcov
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".eggs" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".coverage" -exec rm -rf {} +
	find . -type d -name "htmlcov" -exec rm -rf {} +

.PHONY: setup
setup: clean
	poetry install --all-extras

# Linting
.PHONY: lint
lint:
	poetry run ruff check .
	poetry run black --check .
	poetry run mypy .

# Formatting
.PHONY: format
format:
	poetry run ruff check . --fix
	poetry run black .

# Testing
.PHONY: test
test:
	poetry run pytest --verbose

# Documentation
.PHONY: docs
docs:
	@mkdocs serve

# Build
.PHONY: build
build:
	@python -m tools.build.poetry
