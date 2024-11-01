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

The new architecture provides:
- Better format support
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

### Features

* feat(logging): implement structured logging for better traceability and debugging ([`812407b`](https://github.com/felipepimentel/pepperpy/commit/812407b23dda5237e123cd522ee27a15fa626391))

* feat(modules): add initial implementation of LLM and data processing modules with examples ([`e8119fe`](https://github.com/felipepimentel/pepperpy/commit/e8119fef79c1bd9fec921e79fe960031586eaf45))


## v0.0.0 (2024-10-30)

### Bug Fixes

* fix: set initial version in pyproject.toml ([`192d55f`](https://github.com/felipepimentel/pepperpy/commit/192d55f57d6e2a38fdd08932b61f506050f3248a))

* fix: remove version placeholder from pyproject.toml ([`a521df5`](https://github.com/felipepimentel/pepperpy/commit/a521df5963b2ad74aad8cf1db14b4b0e63f0c695))

* fix: remove GitHub release and asset upload steps from publish workflow ([`efc6e66`](https://github.com/felipepimentel/pepperpy/commit/efc6e66d11a707bac9e38d03eadf7eda068cdb17))

* fix: add step to set initial version tag if missing in publish workflow ([`a972070`](https://github.com/felipepimentel/pepperpy/commit/a972070ab6098ffa8f96242ec1fc4d21233d68e0))

* fix: add version_source to pyproject.toml for semantic versioning ([`29ea200`](https://github.com/felipepimentel/pepperpy/commit/29ea200719478c3e652917f0c6fff3be29703e80))

* fix: streamline semantic release setup in workflow and update build command in pyproject.toml ([`ff7acb7`](https://github.com/felipepimentel/pepperpy/commit/ff7acb71074d8b18a2e5318caeddaef14cd48aec))

* fix(ci): update Python version to 3.10 in publish workflow ([`ed01440`](https://github.com/felipepimentel/pepperpy/commit/ed014401bbec917de908b2dbfd0835d217346e03))

* fix: update semantic release dependency and adjust publish workflow for Python ([`e78845d`](https://github.com/felipepimentel/pepperpy/commit/e78845d7be5db273412f185aba60ae862b4ca1b8))

* fix: update version variable path in pyproject.toml for semantic release ([`4390900`](https://github.com/felipepimentel/pepperpy/commit/4390900c491dd0aafa955f108ad630d3dbb1e52a))

* fix(ci): add semantic-release-python to installation in publish workflow ([`3567acc`](https://github.com/felipepimentel/pepperpy/commit/3567acc6053927843dabda0ea7888348bc590ce6))

* fix(ci): add Node.js setup step in publish workflow ([`8b285a5`](https://github.com/felipepimentel/pepperpy/commit/8b285a57d781e164013099ab222b8967e0bfb235))

* fix: add project description and set initial version in pyproject.toml ([`c9b025f`](https://github.com/felipepimentel/pepperpy/commit/c9b025f798fab664568c90adadcbfd53238d8934))

* fix(ci): update version variable in pyproject.toml for semantic release ([`15d82fc`](https://github.com/felipepimentel/pepperpy/commit/15d82fcd2ba104d4d2ce165f38a9f7086171115f))

* fix(ci): update repository name in release workflow condition ([`169a3ca`](https://github.com/felipepimentel/pepperpy/commit/169a3cabab23e49461bd19c0811de4823a626714))

* fix(ci): update GitHub release step identifiers for consistency ([`0f91b29`](https://github.com/felipepimentel/pepperpy/commit/0f91b298497b9f014d9848416131f74b204366d6))

* fix(ci): update workflow for semantic release and adjust repository permissions ([`7c8ca02`](https://github.com/felipepimentel/pepperpy/commit/7c8ca0259961e0bd79e3cc3eae2f58010454571c))

* fix(ci): update create-release action to v1.1.0 ([`7cae6c8`](https://github.com/felipepimentel/pepperpy/commit/7cae6c8330f50139cf65a885fdfec73f95bab5dc))


## v0.1.4 (2024-10-29)

### Chores

* chore: bump version to 0.1.3 ([`b147279`](https://github.com/felipepimentel/pepperpy/commit/b1472799ad2314097485c4dab8c229edd27fa1fc))

### Unknown

* Bump version to 0.1.4 ([`f1e227f`](https://github.com/felipepimentel/pepperpy/commit/f1e227fea9e5aae82d2969a12ac7f2682e7b0e33))


## v0.1.3 (2024-10-29)

### Bug Fixes

* fix(ci): add error handling for release asset upload step ([`91d8aa4`](https://github.com/felipepimentel/pepperpy/commit/91d8aa455e5fb5c5830595abc8b5530bb6550648))

* fix(ci): downgrade upload-release-asset action to v1 for compatibility ([`0ad6a4c`](https://github.com/felipepimentel/pepperpy/commit/0ad6a4c89b167c7980ccb214d337908307b334b5))

* fix(ci): update release action versions in publish workflow ([`8de7f38`](https://github.com/felipepimentel/pepperpy/commit/8de7f385ec17782ac0de51f225931ca9616a28aa))

### Unknown

* Bump version to 0.1.3 ([`ec717bd`](https://github.com/felipepimentel/pepperpy/commit/ec717bd5a49535daacd35d18a3a6fbc6d88865e6))


## v0.1.2 (2024-10-29)

### Unknown

* Bump version to 0.1.2 ([`c1e1a40`](https://github.com/felipepimentel/pepperpy/commit/c1e1a40838a88bf22679efdd675b75251fcaf3fb))

* Merge branch 'main' of github.com:felipepimentel/pepperpy ([`d8d268c`](https://github.com/felipepimentel/pepperpy/commit/d8d268c6794ad23cc01f013b4da494e5210dad37))


## v0.1.1 (2024-10-29)

### Bug Fixes

* fix(ci): correct upload URL in publish workflow for release assets ([`af9a962`](https://github.com/felipepimentel/pepperpy/commit/af9a9628d25521eff9a66176ae3495cd7c9e28e1))

* fix(ci): enhance publish workflow to retry on failure and bump version ([`3385969`](https://github.com/felipepimentel/pepperpy/commit/338596961bb3e99216e8c7aa74718c471db94b0d))

* fix(ci): add error handling for missing PYPI_TOKEN in publish workflow ([`166ee95`](https://github.com/felipepimentel/pepperpy/commit/166ee953491fd167b443c35770cb5fefcd2aed06))

* fix(ci): replace bump2version with poetry version command in publish workflow ([`9bbe304`](https://github.com/felipepimentel/pepperpy/commit/9bbe304cd03c31b4bf358d33616fc457132c89d5))

* fix(dependencies): remove bumpversion and bump2version from poetry.lock and pyproject.toml ([`8fab7d4`](https://github.com/felipepimentel/pepperpy/commit/8fab7d4981a43504f56023556353efd1c65cfd8a))

* fix(pyproject): remove bumpversion configuration from pyproject.toml ([`421e80b`](https://github.com/felipepimentel/pepperpy/commit/421e80bee8574a8935e27eabe469e77555ac2652))

* fix(ci): update workflow name and actions versions in publish.yml ([`37662f0`](https://github.com/felipepimentel/pepperpy/commit/37662f0a424c94bb389a7f0b95f738202c4ce5cb))

### Continuous Integration

* ci: implement automated release workflow

- Add GitHub Actions workflow for automated releases on version tags
- Configure Poetry for package building and PyPI publishing
- Set up automatic release notes generation
- Include artifact publishing to GitHub releases ([`9453796`](https://github.com/felipepimentel/pepperpy/commit/9453796b1a918bdfafa17619a32b40c4200895c0))

### Features

* feat(ci): add version check before bumping in publish workflow ([`8f894bb`](https://github.com/felipepimentel/pepperpy/commit/8f894bbd2d88cb270b301c06734197614832d116))

* feat(ci): add GITHUB_TOKEN environment variable for secure asset uploads in publish workflow ([`2b7b5c6`](https://github.com/felipepimentel/pepperpy/commit/2b7b5c6c52f9cf4fe594ae829ae4ed343422b115))

* feat(ci): enhance publish workflow with GitHub repository condition and improved asset upload ([`355e4c4`](https://github.com/felipepimentel/pepperpy/commit/355e4c4b53f00329f27386cb9fd2b508ecbbcc0b))

* feat(ci): update publish workflow to create GitHub releases and upload assets ([`2c592ed`](https://github.com/felipepimentel/pepperpy/commit/2c592ed28c67696aed3902f4c606f337d0d7dac3))

* feat(ci): streamline publish workflow by bumping version and tagging before build ([`ce1f8c2`](https://github.com/felipepimentel/pepperpy/commit/ce1f8c2d6ba62ed2cb8d5ba6c21d0e9400db67c0))

* feat(ci): add tagging step in publish workflow for versioning releases ([`ebe119b`](https://github.com/felipepimentel/pepperpy/commit/ebe119b54a578321fc3387303b5b65aaaff86775))

* feat(ci): update publish workflow to trigger on main branch and add version bumping step ([`44f454c`](https://github.com/felipepimentel/pepperpy/commit/44f454c94e7a1238ecb681fb0b311af59845daaa))

* feat(ci): add automated release workflow

- Configure GitHub Actions workflow for automated releases
- Set up Poetry for package building and PyPI publishing
- Enable automatic release notes generation
- Add artifact upload to GitHub releases ([`e314656`](https://github.com/felipepimentel/pepperpy/commit/e314656de8d42df78576e85e155246a0c0fa4a2a))

* feat: initialize pypepper project structure

- Configure Poetry project with basic dependencies
- Set up bumpversion configuration
- Add project description in README.md ([`345be7b`](https://github.com/felipepimentel/pepperpy/commit/345be7b933a7398f96709a0ce44632fad53d649a))

### Refactoring

* refactor: migrate pypepper module to pepperpy and restructure codebase ([`a739bc3`](https://github.com/felipepimentel/pepperpy/commit/a739bc318fd9fd7723cd9bd0e8f8baef9d0d6448))

### Unknown

* Bump version to 0.1.1 ([`9834bd4`](https://github.com/felipepimentel/pepperpy/commit/9834bd4be1cfacd4fde29e332003f53749c78470))

* Merge branch 'main' of github.com:felipepimentel/pypepper ([`762cea3`](https://github.com/felipepimentel/pepperpy/commit/762cea3049cad16f41e1746a83e8b3672d89a676))

* Create publish.yml ([`54705c3`](https://github.com/felipepimentel/pepperpy/commit/54705c3bc632462e55ff5699055ebe76ae8665ad))

* Initial commit ([`2cf6f84`](https://github.com/felipepimentel/pepperpy/commit/2cf6f8486021ecd5e43455c0b720fc69da36440a))
