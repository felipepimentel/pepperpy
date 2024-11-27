# Set default command interpreter
SHELL := /bin/bash

# Variables
PACKAGES_DIR := packages
PYTHON := python3
POETRY := poetry

# Find all packages in specified directory
PACKAGES := $(wildcard $(PACKAGES_DIR)/*)

# Reusable variables
RUN_POETRY = cd $$package && $(POETRY) run

# Install dependencies for all monorepo packages
.PHONY: install
install:
	@for package in $(PACKAGES); do \
		echo "Installing dependencies for $$package..."; \
		cd $$package && if [ ! -d ".venv" ]; then $(POETRY) install; fi; \
	done
	@echo "All dependencies installed!"

# Run tests for all packages
.PHONY: test
test:
	@for package in $(PACKAGES); do \
		echo "Running tests for $$package..."; \
		$(RUN_POETRY) pytest --cov; \
	done
	@echo "All tests completed!"

# Run tests only for modified packages
.PHONY: test-modified
test-modified:
	@for package in $(PACKAGES); do \
		if git diff --quiet HEAD $$package; then \
			echo "No changes in $$package. Skipping..."; \
		else \
			echo "Running tests for $$package..."; \
			$(RUN_POETRY) pytest --cov; \
		fi; \
	done
	@echo "Tests for modified packages completed!"

# Run linters (ruff) for all packages
.PHONY: lint
lint:
	@echo "Running linter for all packages..."
	@echo $(PACKAGES) | xargs -n 1 -P 4 -I {} bash -c "cd {} && $(POETRY) run ruff check ."
	@echo "Linting completed!"

# Format code with Black
.PHONY: format
format:
	@for package in $(PACKAGES); do \
		echo "Formatting code in $$package..."; \
		$(RUN_POETRY) black .; \
	done
	@echo "Formatting completed!"

# Create virtual environments in each package
.PHONY: create-envs
create-envs:
	@$(POETRY) config virtualenvs.in-project true
	@for package in $(PACKAGES); do \
		echo "Creating virtual environment for $$package..."; \
		cd $$package && $(POETRY) env use $(PYTHON) && $(POETRY) install; \
	done
	@echo "Virtual environments created for all packages!"

# Check for dependency updates
.PHONY: check-updates
check-updates:
	@for package in $(PACKAGES); do \
		echo "Checking updates for $$package..."; \
		cd $$package && $(POETRY) update --dry-run; \
	done
	@echo "Update check completed!"

# Generate consolidated coverage report
.PHONY: coverage
coverage:
	@for package in $(PACKAGES); do \
		echo "Running coverage for $$package..."; \
		$(RUN_POETRY) pytest --cov=. --cov-append --cov-report=; \
	done
	@echo "Consolidating coverage reports..."
	@$(PYTHON) -m coverage combine $(PACKAGES) && $(PYTHON) -m coverage report

# Generate documentation (using MkDocs as example)
.PHONY: docs
docs:
	@echo "Generating documentation..."
	@mkdocs build
	@echo "Documentation generated successfully!"

# Clean generated files and caches
.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type f -name ".coverage" -exec rm -f {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name ".venv" -exec rm -rf {} +
	@find . -type d -name "dist" -exec rm -rf {} +
	@find . -type d -name "build" -exec rm -rf {} +
	@echo "All temporary files cleaned!"

# Run all tasks in sequence
.PHONY: all
all: install lint test format
	@echo "All tasks completed successfully!"

# Help
.PHONY: help
help:
	@echo "Available commands:"
	@echo "  install         - Install dependencies for all packages"
	@echo "  test            - Run tests for all packages"
	@echo "  test-modified   - Run tests only for modified packages"
	@echo "  lint            - Run linters (ruff) for all packages"
	@echo "  format          - Format code with Black"
	@echo "  create-envs     - Create virtual environments for all packages"
	@echo "  check-updates   - Check for outdated dependencies"
	@echo "  coverage        - Generate consolidated coverage report"
	@echo "  docs            - Generate documentation"
	@echo "  clean           - Clean generated files and caches"
	@echo "  all             - Run install, lint, tests and formatting"
