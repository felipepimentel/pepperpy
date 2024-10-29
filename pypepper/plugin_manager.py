# pypepper/plugin_manager.py
registered_plugins = {}


def register_plugin(name, plugin):
    """Register a plugin dynamically."""
    registered_plugins[name] = plugin


def get_plugin(name):
    """Retrieve a registered plugin by name."""
    return registered_plugins.get(name, None)
