#!/bin/bash

# docker run -it --network intuit_default --rm mysql:lts mysql -h intuit-mysql-1 -p

docker exec -it homelife-mongo-1 mongosh "mongodb://root:password@localhost:27017"