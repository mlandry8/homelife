#!/bin/sh

# Run the pre-start script
$1 -m homelife.scripts.cert_init

# Start the Flask API
$1 -m uvicorn homelife.api:app --host=0.0.0.0 --ssl-certfile=etc/cert.pem --ssl-keyfile=etc/key.pem