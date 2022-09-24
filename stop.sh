#!/bin/bash
docker compose -f docker-compose-client.yaml stop
docker compose -f docker-compose-client.yaml down
docker compose -f docker-compose-system.yaml stop
docker compose -f docker-compose-system.yaml down