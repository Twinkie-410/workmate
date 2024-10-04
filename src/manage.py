#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""

import os
import sys

from dotenv import load_dotenv


def main():
    """Run administrative tasks."""
    load_dotenv()
    try:
        if os.getenv("DJANGO_DEVELOPMENT") == "true":
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.development")
        else:
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.production")
    except KeyError as ke:
        raise KeyError(f"Env key {ke} not found, add this parameter in env file")

    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
