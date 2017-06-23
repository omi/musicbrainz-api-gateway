#!/bin/sh
. venv/bin/activate
export PYTHONPATH=.:$PYTHONPATH
python omi/app.py

