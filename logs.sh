#!/bin/bash
docker logs middleware >& logs/middleware.log
docker logs client >& logs/clieng.log
docker logs ingestion_service >& logs/ingestion_service.log
docker logs like_filter >& logs/like_filter.log
docker logs funny_filter >& logs/funny_filter.log
docker logs reporting_service >& logs/reporting_service.log
docker logs day_grouper >& logs/day_grouper.log
docker logs max >& logs/max.log