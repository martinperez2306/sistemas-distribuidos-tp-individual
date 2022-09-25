#!/bin/bash
cd base_images
docker build -f python-rabbitmq.dockerfile -t python-rabbitmq .
docker build -f middleware_client/middleware_client.dockerfile -t middleware_client ./middleware_client/
docker build -f middleware_client/middlewaresys_client.dockerfile -t middlewaresys_client ./middlewaresys_client/