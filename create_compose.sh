#!/bin/bash
usage="Debe ingresar el numero de clientes"

if [ $# -eq 0 ]; then
  echo "$usage"
  exit 1    
fi

INSTANCES=$1
BASE_TEMPLATE="create_compose/base_template.yaml"
CLIENT_TEMPLATE="create_compose/client_template.yaml"
MIDDLEWARE_TEMPLATE="create_compose/middleware_template.yaml"
INGESTION_TEMPLATE="create_compose/ingestion_service.yaml"
LIKE_TEMPLATE="create_compose/like_filter.yaml"
TRENDING_TEMPLATE="create_compose/trending_filter.yaml"
FUNNY_TEMPLATE="create_compose/funny_filter.yaml"
DAY_TEMPLATE="create_compose/day_grouper.yaml"
MAX_TEMPLATE="create_compose/max.yaml"
REPORTING_TEMPLATE="create_compose/reporting_service.yaml"
NETWORK_TEMPLATE="create_compose/network_template.yaml"
OUTPUT="docker-compose-system.yaml"
OUTPUT_CLIENT="docker-compose-client.yaml"

cat /dev/null > $OUTPUT
cat /dev/null > $OUTPUT_CLIENT

SERVICE_ID="SERV_ID"
SERVICES_INSTANCES="SERV_INSTANCES"
SERV_INSTANCES="$INSTANCES"

cat $CLIENT_TEMPLATE | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT_CLIENT
cat $BASE_TEMPLATE >> $OUTPUT
echo -e "\n" >> $OUTPUT

cat_service() {
  TEMPLATE=$1
  SERVICE_NAME=$2
  SERV_NAME=$3
  cat $TEMPLATE | sed -r "s/$SERVICE_NAME/$SERV_NAME/g" | sed -r "s/$SERVICE_ID/$SERV_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
  echo -e "\n" >> $OUTPUT
}

for i in $( seq 1 $INSTANCES )
do

    cat_service $INGESTION_TEMPLATE "INGESTION_SERVICE" "ingestion_service_$i"
    cat_service $LIKE_TEMPLATE "LIKE_FILTER" "like_filter_$i"
    cat_service $TRENDING_TEMPLATE "TRENDING_FILTER" "trending_filter_$i"
    cat_service $FUNNY_TEMPLATE "FUNNY_FILTER" "funny_filter_$i"
    cat_service $DAY_TEMPLATE "DAY_GROUPER" "day_grouper_$i"

done

cat_service $MAX_TEMPLATE "MAX" "max"
cat_service $REPORTING_TEMPLATE "REPORTING_SERVICE" "reporting_service"

cat $NETWORK_TEMPLATE >> $OUTPUT