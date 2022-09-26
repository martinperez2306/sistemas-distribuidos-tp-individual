#!/bin/bash
docker logs middleware >& logs/middleware.log
docker logs client >& logs/clieng.log
docker logs ingestion_service >& logs/ingestion_service.log
docker logs like_filter >& logs/like_filter.log