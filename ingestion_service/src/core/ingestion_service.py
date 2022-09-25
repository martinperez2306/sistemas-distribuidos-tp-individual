import logging
import pika

RABBITMQ_HOST = "rabbitmq"
INGESTION_QUEUE_NAME = "ingestion_service_queue"

class IngestionService:
    def __init__(self):
        self.connection = None
        self.channel = None

    def run(self):
        self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
        self.channel = self.connection.channel()
        self.channel.queue_declare(queue=INGESTION_QUEUE_NAME, durable=True)

        def handle_message(ch, method, properties, body):
            logging.info("Received {}".format(body))
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self.channel.basic_qos(prefetch_count=1)
        self.channel.basic_consume(queue=INGESTION_QUEUE_NAME, on_message_callback=handle_message)

        logging.info('Waiting for messages. To exit press CTRL+C')
        self.channel.start_consuming()