#!/bin/bash

python3 -m venv warehouse_env
source warehouse_env/bin/activate
pip install Flask Flask-WTF
