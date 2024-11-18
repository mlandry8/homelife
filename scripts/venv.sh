#!/bin/bash

source scripts/env.sh $1

# Create the virtual environment if it doesn't exist
if [ ! -d "$VIRTUAL_ENV" ]; then
    python3 -m venv "$VIRTUAL_ENV"
    echo "Virtual environment created at $VIRTUAL_ENV"
else
    echo "Virtual environment already exists at $VIRTUAL_ENV"
fi

# Activate the virtual environment
source "$VIRTUAL_ENV/bin/activate"

python3 -m pip install --upgrade pip

if [ -f "requirements/$1.txt" ]; then
    python3 -m pip install -r requirements/$1.txt
else
    echo "requirements/$1.txt file not found!"
    exit 1
fi

python3 -m pip install -e .

echo "Virtual environment activated"
