#!/usr/bin/env python3
"""
configurable_app.py
Demonstrates 12-Factor App configuration via environment variables.
"""

import json
import os
import sys

def main():
    config = {
        "app_mode": os.environ.get("APP_MODE", "production"),
        "log_level": os.environ.get("LOG_LEVEL", "INFO"),
        "database_url": os.environ.get("DATABASE_URL", "sqlite:///default.db"),
        "max_connections": int(os.environ.get("MAX_CONNECTIONS", 10)),
        "debug": os.environ.get("DEBUG", "false").lower() in ("true", "1", "yes"),
    }
    
    print(f"=== Application Config Bootstrapped ===")
    print(json.dumps(config, indent=2))
    
    if config["debug"]:
        print("\n[DEBUG ACTIVE] Verbose diagnostic output enabled.")

if __name__ == "__main__":
    main()
