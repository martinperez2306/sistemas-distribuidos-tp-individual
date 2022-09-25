#!/bin/bash
docker logs middleware >& logs/middleware.log
docker logs client >& logs/clieng.log
docker logs ingestion_service >& logs/ingestion_service.log