#HOST
RABBITMQ_HOST = "rabbitmq"

#QUEUES
MIDDLEWARE_QUEUE = "middleware"
INGESTION_QUEUE = "ingestion_service_queue"

#MESSAGE IDS
CLIENT_MESSAGE_ID = 0
SERVICE_MESSAGE_ID = 1
MIDDLEWARE_MESSAGE_ID = 2

#CLIENT OPERATION IDS
START_PROCESS_ID = 0
PROCESS_DATA_ID = 1
END_PROCESS_ID = 2
GET_RESULTS_ID = 3

#SYSTEM OPERATION IDS
INGEST_DATA_ID = 100
LIKE_FILTER_ID = 101