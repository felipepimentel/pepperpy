# pypepper/config.py
import json


class Config:
    """Centralized configuration manager for pypepper."""

    def __init__(self, config_file="config.json"):
        self.config = self.load_config(config_file)

    def load_config(self, config_file):
        """Load configuration from a JSON file."""
        with open(config_file, "r") as file:
            return json.load(file)

    def get(self, key, default=None):
        """Retrieve a configuration value by key."""
        return self.config.get(key, default)


# Example usage
# config = Config().get("db_host", "localhost")
