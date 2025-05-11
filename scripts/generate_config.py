import os
import json
from media_tool.config import Config

config = Config()

if not os.path.exists(config.CONFIG_PATH):
    with open(config.CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config.get_config_dict(), f, indent=2)
    print(f"Created config.json at {config.CONFIG_PATH}")
else:
    print("config.json already exists.")