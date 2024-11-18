#/bin/bash

source scripts/env.sh $1

docker compose --env-file environments/$ENV.env up --watch --build
