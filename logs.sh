#!/bin/bash
usage="Debe ingresar el numero de instancias"

if [ $# -eq 0 ]; then
  echo "$usage"
  exit 1    
fi

INSTANCES=$1
LOGS_DIR="logs"

docker logs client >& "$LOGS_DIR/client.log"

for i in $( seq 1 $INSTANCES )
do
    docker logs "ingestion_service_$i" >& "$LOGS_DIR/ingestion_service_$i.log"
    docker logs "like_filter_$i" >& "$LOGS_DIR/like_filter_$i.log"
    docker logs "trending_filter_$i" >& "$LOGS_DIR/trending_filter_$i.log"
    docker logs "funny_filter_$i" >& "$LOGS_DIR/funny_filter_$i.log"
    docker logs "day_grouper_$i" >& "$LOGS_DIR/day_grouper_$i.log"
done

docker logs "max" >& "$LOGS_DIR/max.log"
docker logs "reporting_service_1" >& "$LOGS_DIR/reporting_service.log"