include tools/make/common.mk
include tools/make/examples.mk

# Find all package directories
PACKAGES := $(notdir $(wildcard packages/*))

# Package management targets
.PHONY: list-packages
list-packages:
	$(call log,"Available packages:")
	@for pkg in $(PACKAGES); do \
		echo "  $$pkg"; \
	done

# Setup targets for each package
define make-setup-target
.PHONY: setup-$(1)
setup-$(1):
	$$(call log,"Setting up $(1)...")
	@cd packages/$(1) && $$(POETRY) lock --no-update && $$(POETRY) install
endef

$(foreach pkg,$(PACKAGES),$(eval $(call make-setup-target,$(pkg))))

# Clean target
.PHONY: clean
clean:
	$(call log,"Cleaning project...")
	$(call clean-python)
	$(call clean-build)

# Setup target
.PHONY: setup
setup:
	@echo ">>> Setting up development environment..."
	@bash scripts/install.sh

setup-%:
	@echo ">>> Setting up $*..."
	@cd packages/$* && poetry install

# Update locks target
.PHONY: update-locks
update-locks:
	$(call log,"Updating poetry.lock files...")
	@for pkg in $(PACKAGES); do \
		cd packages/$$pkg && $(POETRY) lock && cd ../..; \
	done

# Linting
.PHONY: lint
lint:
	$(call log,"Running linters...")
	@$(POETRY) run ruff check .
	@$(POETRY) run black --check .
	@$(POETRY) run mypy .

# Formatting
.PHONY: format
format:
	$(call log,"Formatting code...")
	@$(POETRY) run ruff check . --fix
	@$(POETRY) run black .

# Testing
.PHONY: test
test:
	$(call log,"Running tests...")
	@$(POETRY) run pytest --verbose

# Documentation
.PHONY: docs
docs:
	$(call log,"Starting documentation server...")
	@mkdocs serve

# Build
.PHONY: build
build:
	$(call log,"Building packages...")
	@python -m tools.build.poetry

# Help target
.PHONY: help
help:
	@echo "Available commands:"
	@echo ""
	@echo "Package management:"
	@echo "  list-packages    List available packages"
	@echo "  setup           Install all dependencies and packages"
	@echo "  setup-<pkg>     Setup specific package"
	@echo "  update-locks    Update poetry.lock files"
	@echo ""
	@echo "Examples:"
	@echo "  examples-core    Run pepperpy-core examples"
	@echo "  examples-console Run pepperpy-console examples"
	@echo "  examples-ai      Run pepperpy-ai examples"
	@echo "  examples-all     Run all examples"
	@echo ""
	@echo "Development:"
	@echo "  clean           Clean build artifacts"
	@echo "  lint            Run linters"
	@echo "  format          Format code"
	@echo "  test            Run tests"
	@echo "  docs            Start documentation server"
	@echo "  build           Build packages"
