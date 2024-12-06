# CHANGELOG


## v1.4.0 (2024-10-31)

### Chores

* chore(version): bump version to 1.2.2 in pyproject.toml ([`82dfa57`](https://github.com/felipepimentel/pepperpy/commit/82dfa57988d13e738af5750aa41ca36f2a564178))

### Features

* feat(config): add GitHub token to workflow and update repository URL in pyproject.toml ([`5722f08`](https://github.com/felipepimentel/pepperpy/commit/5722f0849a18502a59c8751911c6eb1707a1db82))


## v1.3.0 (2024-10-31)

### Chores

* chore(version): bump version to 1.2.1 in pyproject.toml ([`d873f68`](https://github.com/felipepimentel/pepperpy/commit/d873f6818212a9f13a8d68997d14bfe058599a2b))

### Features

* feat(config): add release configuration file for GitHub actions ([`a4b3393`](https://github.com/felipepimentel/pepperpy/commit/a4b3393078f751ff9a497c746729fd8dffef6f26))


## v1.2.0 (2024-10-31)

### Unknown

* Merge branch 'main' of github.com:felipepimentel/pepperpy ([`7228380`](https://github.com/felipepimentel/pepperpy/commit/72283805261ac32b1f558ee2ea0afdf33b89932b))


## v1.1.0 (2024-10-31)

### Features

* feat(core): implement middleware and hooks support in the application framework

feat(validation): add data validation and sanitization system

feat(rate-limiter): introduce token bucket rate limiting implementation

feat(factory): extend factory class to create additional components

chore: update version to 1.0.1 and add version retrieval logic ([`cb3ad89`](https://github.com/felipepimentel/pepperpy/commit/cb3ad89eac36fce3a47ad60569b2e60d662b7ddf))

* feat(infrastructure): add examples for distributed caching, job processing, and metrics collection ([`0f33a08`](https://github.com/felipepimentel/pepperpy/commit/0f33a08a9fb123400c7c8f2cd315061175cbac79))

* feat(api): enhance API endpoints for improved performance and scalability ([`6a87e99`](https://github.com/felipepimentel/pepperpy/commit/6a87e991f1240cd95a61390f9fced0e3f98ee1a6))


## v1.0.0 (2024-10-31)

### Breaking

* feat(serialization): replace msgspec with cattrs and msgpack

This commit updates the serialization system for Python 3.13 compatibility:

- feat(formats): implement new serialization handler
  - Add cattrs for modern type conversion
  - Add msgpack for efficient binary serialization
  - Add support for complex data types
  - Improve datetime handling

- chore(deps): update dependencies
  - Remove msgspec dependency
  - Add cattrs ^23.2.3
  - Add msgpack ^1.0.7
  - Update Python requirement to ^3.13

- feat(handlers): add binary data support
  - Add BinaryHandler for serialized data
  - Add .bin and .msg format support
  - Improve type conversion
  - Add custom serialization hooks

BREAKING CHANGE: Removes msgspec dependency in favor of cattrs + msgpack
for better Python 3.13 compatibility and improved type handling.

The changes provide:
- Full Python 3.13 compatibility
- Better type conversion support
- More efficient binary serialization
- Improved handling of complex types ([`977e2c2`](https://github.com/felipepimentel/pepperpy/commit/977e2c216496e15ce0c84821126e995f10ce0c05))

* feat(github): add comprehensive GitHub management module

This commit introduces a robust GitHub management system with the following features:

- feat(github): add core GitHub client with flexible authentication
  - Support for token and app-based auth
  - Enterprise GitHub support
  - Type-safe API interfaces

- feat(workflows): add GitHub Actions workflow management
  - Create/update workflow files
  - List workflows
  - Trigger workflow runs
  - YAML configuration support

- feat(actions): add GitHub Actions run management
  - List workflow runs with filtering
  - Cancel/rerun workflow runs
  - Access run logs
  - Status monitoring

- feat(secrets): add GitHub Secrets management
  - Set/delete repository secrets
  - List available secrets
  - Secure encryption handling
  - Visibility control

- feat(examples): add GitHub integration examples
  - Complete workflow examples
  - Authentication setup
  - Common operations demo

BREAKING CHANGE: This adds new dependencies:
- PyGithub for GitHub API
- PyNaCl for secrets encryption
- PyYAML for workflow files

The changes provide:
- Complete GitHub automation capabilities
- Secure secrets handling
- CI/CD integration
- Repository management ([`c3d2852`](https://github.com/felipepimentel/pepperpy/commit/c3d2852bb9ff8a033bd10fc3b8dcdbf29328aacd))

* feat(deps): update dependencies and modernize file handlers

This commit updates project dependencies and modernizes file handling:

- feat(deps): update core dependencies
  - Update pydantic to 2.9.2
  - Update typer to 0.12.5
  - Update rich to 13.9.3
  - Update loguru to 0.7.2

- feat(files): modernize file handlers
  - Replace python-epub3 with ebooklib for better EPUB support
  - Add polars as alternative to pandas for better performance
  - Update pypdf to 5.1.0 for improved PDF handling
  - Add msgspec for faster serialization
  - Add xmltodict for better XML handling

- refactor(formats): improve file format handlers
  - Add better type hints
  - Improve error handling
  - Add format auto-detection
  - Add metadata extraction
  - Add encoding detection

- chore(deps): update dev dependencies
  - Update pytest to 8.3.3
  - Update black to 24.10.0
  - Update ruff to 0.7.1
  - Update mypy to 1.13.0

BREAKING CHANGE: The file handling API has been updated to use newer libraries and provide better type safety.

The changes provide:
- Better performance with modern libraries
- Improved type safety
- Better error handling
- Enhanced metadata support
- More format options ([`c8c49b0`](https://github.com/felipepimentel/pepperpy/commit/c8c49b08c60e81f59d197465250261715c55d339))

* feat(core): enhance file operations and format handlers

This commit introduces significant improvements to the file handling system:

- feat(files): add comprehensive format handlers for multiple file types
  - JSON with indentation support
  - YAML with safe loading
  - TOML configuration
  - INI with section support
  - EPUB with metadata handling
  - WebVTT subtitle support
  - XML with nested structure support
  - CSV with flexible formatting

- refactor(core): improve file operations architecture
  - Add FileHandler base class for consistent interface
  - Implement FileManager for centralized operations
  - Add type hints and documentation
  - Improve error handling
  - Add format auto-detection
  - Support both sync and async operations

- feat(examples): add comprehensive file operation examples
  - Add format-specific examples
  - Demonstrate error handling
  - Show configuration options
  - Include metadata handling

BREAKING CHANGE: The file operations API has been redesigned for better consistency and type safety.



- Improved error handling
- Consistent interface across formats
- Better type safety
- Automatic format detection
- Enhanced metadata support ([`2e97e88`](https://github.com/felipepimentel/pepperpy/commit/2e97e884286359f56a4d6615610ce2034f966253))

* feat(core): implement modular architecture and enhance core capabilities

This commit introduces several major enhancements to the library's core architecture:

- feat(ai): add comprehensive AI module with LLM, RAG and agent capabilities
- feat(auth): implement secure authentication and authorization system
- feat(cache): add flexible caching system with multiple backends
- feat(config): enhance configuration management with hierarchical support
- feat(console): add rich console interface with advanced formatting
- feat(database): implement database abstraction with multiple drivers
- feat(events): add async event system for inter-module communication
- feat(files): enhance file operations with multiple format support
- feat(http): add robust HTTP client with retry and caching
- feat(logging): improve logging system with structured output
- feat(messaging): add message broker support (RabbitMQ/Kafka)
- feat(plugins): implement plugin system for extensibility
- feat(scheduler): add task scheduling and background jobs
- feat(secrets): add secure secrets management
- feat(websocket): implement WebSocket support for real-time communication

BREAKING CHANGE: This version introduces a new modular architecture that may require updates to existing code.

The new architecture provides:
- Better separation of concerns
- Improved modularity and extensibility
- Enhanced error handling
- Better type safety
- More consistent APIs
- Improved documentation
- Better testing support ([`9651c08`](https://github.com/felipepimentel/pepperpy/commit/9651c087d5ccab3ac4ce64e99e0016c4ec582c9e))

### Bug Fixes

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))


* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: add step to clean previous builds in publish workflow ([`8a0d4e5`](https://github.com/felipepimentel/pepperpy/commit/8a0d4e53dff8728cb301b5507b2f12d180397a7f))

* fix: update versioning configuration and remove unnecessary steps in publish workflow ([`c4c1085`](https://github.com/felipepimentel/pepperpy/commit/c4c10853e8c88e8b56ee7f8f185a11ef13ae2ac3))

* fix: remove initial version tagging step from publish workflow ([`863d97a`](https://github.com/felipepimentel/pepperpy/commit/863d97a89cf8d76c9e9eecf0d7543cf8e73f909a))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225f513726fb70968bd5000886))

* fix: remove logging module and related configuration ([`5685e2c`](https://github.com/felipepimentel/pepperpy/commit/5685e2cd14f31f9edd4da5596109949e5b46dbd0))

* fix: update version to 1.0.0 in __init__.py and pyproject.toml ([`190e9a2`](https://github.com/felipepimentel/pepperpy/commit/190e9a2eabc85f9733c15783e6f79d5887831288))

* fix: update version to 0.1.0 in __init__.py and pyproject.toml ([`459c7e2`](https://github.com/felipepimentel/pepperpy/commit/459c7e2f566fe8b7395f43581c82a104e2bd3e56))

* fix: ensure newline at end of file in pyproject.toml ([`f5d26fd`](https://github.com/felipepimentel/pepperpy/commit/f5d26fd84cf2f1225