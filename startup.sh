#!/bin/sh

# Run the pre-start script
$1 -m homelife.scripts.cert_init

# Start the Flask API
$1 -m flask --app homelife.api run --host=0.0.0.0 --cert=etc/cert.pem --key=etc/key.pem