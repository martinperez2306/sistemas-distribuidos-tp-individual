#!/bin/bash
docker build -f python-rabbitmq.dockerfile -t python-rabbitmq .
docker build -f middleware_client/middleware_client.dockerfile -t middleware_client ./middleware_client/