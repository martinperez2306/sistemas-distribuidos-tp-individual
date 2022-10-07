#!/bin/bash
usage="Debe ingresar el numero de clientes"

if [ $# -eq 0 ]; then
  echo "$usage"
  exit 1    
fi

INSTANCES=$1
BASE_TEMPLATE="create_compose/base_template.yaml"
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

cat /dev/null > $OUTPUT
cat $BASE_TEMPLATE >> $OUTPUT
echo -e "\n" >> $OUTPUT

SERVICES_INSTANCES="SERV_INSTANCES"
SERV_INSTANCES="$INSTANCES"
cat $MIDDLEWARE_TEMPLATE | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
echo -e "\n" >> $OUTPUT

INGESTION_SERVICE="INGESTION_SERVICE"
CONTAINER_NAME="CONTAINER_NAME"
INGESTION_NAME="ingestion_service_1"
SERVICE_ID="SERV_ID"
cat $INGESTION_TEMPLATE | sed -r "s/$INGESTION_SERVICE/$INGESTION_NAME/g" | sed -r "s/$CONTAINER_NAME/$INGESTION_NAME/g" | sed -r "s/$SERVICE_ID/$INGESTION_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
echo -e "\n" >> $OUTPUT

for i in $( seq 1 $INSTANCES )
do
    LIKE_FILTER="LIKE_FILTER"
    CONTAINER_NAME="CONTAINER_NAME"
    LIKE_NAME="like_filter_$i"
    SERVICE_ID="SERV_ID"
    cat $LIKE_TEMPLATE | sed -r "s/$LIKE_FILTER/$LIKE_NAME/g" | sed -r "s/$CONTAINER_NAME/$LIKE_NAME/g" | sed -r "s/$SERVICE_ID/$LIKE_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
    echo -e "\n" >> $OUTPUT

    TRENDING_FILTER="TRENDING_FILTER"
    CONTAINER_NAME="CONTAINER_NAME"
    TRENDING_NAME="trending_filter_$i"
    SERVICE_ID="SERV_ID"
    cat $TRENDING_TEMPLATE | sed -r "s/$TRENDING_FILTER/$TRENDING_NAME/g" | sed -r "s/$CONTAINER_NAME/$TRENDING_NAME/g" | sed -r "s/$SERVICE_ID/$TRENDING_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
    echo -e "\n" >> $OUTPUT

    FUNNY_FILTER="FUNNY_FILTER"
    CONTAINER_NAME="CONTAINER_NAME"
    FUNNY_NAME="funny_filter_$i"
    SERVICE_ID="SERV_ID"
    cat $FUNNY_TEMPLATE | sed -r "s/$FUNNY_FILTER/$FUNNY_NAME/g" | sed -r "s/$CONTAINER_NAME/$FUNNY_NAME/g" | sed -r "s/$SERVICE_ID/$FUNNY_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
    echo -e "\n" >> $OUTPUT

    DAY_GROUPER="DAY_GROUPER"
    CONTAINER_NAME="CONTAINER_NAME"
    DAY_NAME="day_grouper_$i"
    SERVICE_ID="SERV_ID"
    cat $DAY_TEMPLATE | sed -r "s/$DAY_GROUPER/$DAY_NAME/g" | sed -r "s/$CONTAINER_NAME/$DAY_NAME/g" | sed -r "s/$SERVICE_ID/$DAY_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
    echo -e "\n" >> $OUTPUT
done

MAX="MAX"
CONTAINER_NAME="CONTAINER_NAME"
MAX_NAME="max_1"
SERVICE_ID="SERV_ID"
cat $MAX_TEMPLATE | sed -r "s/$MAX/$MAX_NAME/g" | sed -r "s/$CONTAINER_NAME/$MAX_NAME/g" | sed -r "s/$SERVICE_ID/$MAX_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
echo -e "\n" >> $OUTPUT

REPORTING_SERVICE="REPORTING_SERVICE"
CONTAINER_NAME="CONTAINER_NAME"
REPORTING_NAME="reporting_service_1"
SERVICE_ID="SERV_ID"
cat $REPORTING_TEMPLATE | sed -r "s/$REPORTING_SERVICE/$REPORTING_NAME/g" | sed -r "s/$CONTAINER_NAME/$REPORTING_NAME/g" | sed -r "s/$SERVICE_ID/$REPORTING_NAME/g" | sed -r "s/$SERVICES_INSTANCES/$SERV_INSTANCES/g" >> $OUTPUT
echo -e "\n" >> $OUTPUT

cat $NETWORK_TEMPLATE >> $OUTPUT