#ENCODING
UTF8_ENCODING = "utf-8"

#MESSAGE FORMAT
MESSAGE_ID_REGEX = r'MESSAGE_ID\[(.*?)\]'
MESSAGE_REQUEST_ID_REGEX=r'REQUEST_ID\[(.*?)\]'
MESSAGE_SOURCE_ID_REGEX=r'SOURCE_ID\[(.*?)\]'
MESSAGE_OPERATION_ID_REGEX=r'OPERATION_ID\[(.*?)\]'
MESSAGE_DESTINATION_ID_REGEX=r'DESTINATION_ID\[(.*?)\]'
MESSAGE_BODY_REGEX=r'BODY(?:\[+)(.*)(?:\]+)'

#HOST
RABBITMQ_HOST = "rabbitmq"

#QUEUES
MIDDLEWARE_QUEUE = "middleware"
INGESTION_SERVICE_QUEUE = "ingestion_service_queue"
LIKE_FILTER_QUEUE = "like_filter_queue"
FUNNY_FILTER_QUEUE = "funny_filter_queue"
REPORTING_SERVICE_QUEUE = "reporting_service_queue"

#EXCHANGUES
DAY_GROUPER_EXCHANGE = "day_group"

#MESSAGE IDS
CLIENT_MESSAGE_ID = 0
SERVICE_MESSAGE_ID = 1
MIDDLEWARE_MESSAGE_ID = 2

#CLIENT OPERATION IDS
START_PROCESS_OP_ID = 0
PROCESS_DATA_OP_ID = 1
END_PROCESS_OP_ID = 2
SEND_RESULTS_OP_ID = 3

#SYSTEM WORKERS IDS
MIDDLEWARE_ID = "middleware"
INGEST_DATA_WORKER_ID = "ingestion_service"
LIKE_FILTER_WORKER_ID = "like_filter"
FUNNY_FILTER_WORKER_ID = "funny_filter"
DAY_GROUPER_WORKER_ID = "day_group"
STORAGE_DATA_WORKER_ID = "reporting_service"