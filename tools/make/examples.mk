# Example targets

# Core examples
.PHONY: examples-core
examples-core:
	$(call log,"Running pepperpy-core examples...")
	@cd packages/pepperpy-core && $(POETRY) run python -m examples.config_example
	@cd packages/pepperpy-core && $(POETRY) run python -m examples.cache_example
	@cd packages/pepperpy-core && $(POETRY) run python -m examples.validation_example

# Console examples
.PHONY: examples-console
examples-console:
	$(call log,"Running pepperpy-console examples...")
	@cd packages/pepperpy-console && $(POETRY) run python examples/chat_interface.py
	@cd packages/pepperpy-console && $(POETRY) run python examples/progress_tracker.py

# AI examples
.PHONY: examples-ai
examples-ai:
	$(call log,"Running pepperpy-ai examples...")
	@cd packages/pepperpy-ai && $(POETRY) run python examples/agent_example.py

# Run all examples
.PHONY: examples-all
examples-all: examples-core examples-console examples-ai
	$(call log,"All examples completed!") 