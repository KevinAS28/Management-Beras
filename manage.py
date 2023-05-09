#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import updater
from threading import Thread

def try_update():
    print('Running...')
    try:
        updater.updater(False)
        print('Run OK')
    except:
        pass

def main():
    """Run administrative tasks."""
    Thread(target=try_update, args=[]).start()
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'beraspakde.settings')
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
