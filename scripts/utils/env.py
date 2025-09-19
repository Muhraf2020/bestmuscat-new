"""
Utility for loading environment variables from a .env file into os.environ.

This module reads a file named .env at the project root and populates
environment variables that are not already set.

Note: Do not commit your .env file to version control.
"""
import os


def load_env(path: str = ".env") -> None:
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, value = line.split("=", 1)
            if key and key not in os.environ:
                os.environ[key] = value