#HOST
RABBITMQ_HOST = "rabbitmq"

#QUEUES
MIDDLEWARE_QUEUE = "middleware"
INGESTION_SERVICE_QUEUE = "ingestion_service_queue"
LIKE_FILTER_QUEUE = "like_filter_queue"
FUNNY_FILTER_QUEUE = "funny_filter_queue"
REPORTING_SERVICE_QUEUE = "reporting_service_queue"

#MESSAGE IDS
CLIENT_MESSAGE_ID = 0
SERVICE_MESSAGE_ID = 1
MIDDLEWARE_MESSAGE_ID = 2

#CLIENT OPERATION IDS
START_PROCESS_OP_ID = 0
PROCESS_DATA_OP_ID = 1
END_PROCESS_OP_ID = 2
SEND_RESULTS_OP_ID = 3

#SYSTEM OPERATION IDS
INGEST_DATA_OP_ID = 100
LIKE_FILTER_OP_ID = 101
FUNNY_FILTER_OP_ID = 102
STORAGE_DATA_OP_ID = 200