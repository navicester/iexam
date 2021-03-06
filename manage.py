#!/usr/bin/env python
import os
import sys

if __name__ == "__main__":
    # root = os.path.dirname(__file__)
    root = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, os.path.join(root, 'site-packages'))
    print sys.path
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "iexam.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
