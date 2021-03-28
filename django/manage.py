"""
Script file: manage.py
Created on: Feb 25, 2021
Last modified on: Mar 28, 2021

Comments:
    Django's command-line utility for administrative tasks.
"""

import os
import sys


def main():
    """
    Main method to start Django administrative tasks
    :param: none
    :return: none
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
