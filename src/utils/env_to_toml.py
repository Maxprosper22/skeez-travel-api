import toml
import os
from dotenv import load_dotenv

# Interpolate environment variables
def interpolate_env_vars(config):
    if isinstance(config, dict):
        for key, value in config.items():
            if isinstance(value, str) and value.startswith("${") and value.endswith("}"):
                env_var = value[2:-1]
                if env_var in os.environ:
                    config[key] = os.environ[env_var]
            elif isinstance(value, dict):
                interpolate_env_vars(value)
            elif isinstance(value, list):
                for item in value:
                    interpolate_env_vars(item)
