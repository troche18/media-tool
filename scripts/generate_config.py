import os
import json
from media_tool.config import CONFIG_PATH, DEFAULT_CONFIG

if not os.path.exists(CONFIG_PATH):
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(DEFAULT_CONFIG, f, indent=2)
    print(f"Created config.json at {CONFIG_PATH}")
else:
    print("config.json already exists.")