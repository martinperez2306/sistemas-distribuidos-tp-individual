#!/bin/bash
docker logs middleware >& logs/middleware.log
docker logs client >& logs/clieng.log