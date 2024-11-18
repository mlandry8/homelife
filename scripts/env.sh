#!/bin/bash

# Check if a parameter is provided
if [ -z "$1" ]; then
    echo "Usage: $0 <path_to_env_file>"
    exit 1
fi

# Load environment variables from the provided .env file
if [ -f "environments/$1.env" ]; then
    export $(cat "environments/$1.env" | xargs)
else
    echo "environments/$1.env file not found!"
    exit 1
fi
