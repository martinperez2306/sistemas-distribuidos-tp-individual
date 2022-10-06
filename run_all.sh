#!/bin/bash
echo "Stopping previous environment"
./stop.sh
echo "Initialize new environment"
./up.sh
echo "Waiting for environment start up..."
sleep 10
echo "Query videos!"
./run.sh