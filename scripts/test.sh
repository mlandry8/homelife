#!/bin/bash

source scripts/env.sh local

# Activate the virtual environment
source "$VIRTUAL_ENV/bin/activate"

# run tests
python -m unittest tests/*.py
