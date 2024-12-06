# Common variables
PYTHON := python
POETRY := poetry
PDM := pdm
PYTEST := pytest
RUFF := ruff
BLACK := black
MYPY := mypy

# Python paths
PYTHONPATH := PYTHONPATH=.

# Colors for terminal output
YELLOW := \033[1;33m
NC := \033[0m # No Color
GREEN := \033[0;32m
RED := \033[0;31m

# Helper functions
define log
	@echo "$(GREEN)>>> $(1)$(NC)"
endef

define error
	@echo "$(RED)>>> Error: $(1)$(NC)"
endef

define warn
	@echo "$(YELLOW)>>> Warning: $(1)$(NC)"
endef

# Common targets
.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type f -name "*.pyd" -delete
	@find . -type f -name ".coverage" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} +
	@find . -type d -name "*.egg" -exec rm -rf {} +
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +
	@find . -type d -name ".ruff_cache" -exec rm -rf {} +
	@find . -type d -name ".mypy_cache" -exec rm -rf {} +
	@find . -type d -name "build" -exec rm -rf {} +
	@find . -type d -name "dist" -exec rm -rf {} +
	$(call log,"Cleaned up python cache and build files") 