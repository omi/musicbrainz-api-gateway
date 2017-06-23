#!/bin/sh
rm -fr venv
virtualenv venv
. venv/bin/activate
pip install -r requirements.txt

