#!/bin/bash

COMPOSE="docker-compose.yml"
NETWORK="trader-network"
docker network create "$NETWORK" || echo "network already exists: $NETWORK"
echo "starting compose: $COMPOSE"
docker-compose -f "$COMPOSE"  up --build