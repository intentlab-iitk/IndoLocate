import yaml
import os

def load_config(default_config, user_config=None):
    """
    Load configuration from a user provided YAML file or use a default YAML file.

    Parameters:
        default_config (str): Path to a default configuration file.
        user_config (str, optional): Path to a user-provided configuration file.

    Returns:
        dict: Loaded configuration dictionary (with a fallback to defaults).
    """
    config = user_config or default_config

    if os.path.isfile(config):
        try:
            with open(config, 'r') as file:
                print(f"[*] Loading configuration from {config}")
                config = yaml.safe_load(file) or {}
        except yaml.YAMLError as e:
            print(f"[!] Error parsing YAML file '{user_config}': {e}. Falling back to default config.")
    else:
        config = {}

    return config
