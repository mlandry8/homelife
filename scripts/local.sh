#!/bin/bash

source scripts/env.sh local

# Activate the virtual environment
source "$VIRTUAL_ENV/bin/activate"

# Generate the SSL certificate
python -m homelife.scripts.cert_init 

# Run intuit module
python -m flask --app homelife.api run --cert=etc/cert.pem --key=etc/key.pem --host=0.0.0.0
