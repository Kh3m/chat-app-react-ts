import json
import pika
import time
import dotenv
import inspect
import logging
from os import getenv
from datetime import datetime


dotenv.load_dotenv()
logger = logging.getLogger("api_v1")


class RBMQ:
    def __init__(self, exchange_name, exchange_type):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.port = getenv("RBMQ_PORT", 5672)
        self.host = getenv("RBMQ_HOST", "localhost")

        # Establish the initial connection and channel
        self.connection, self.channel = self.establish_connection()

    def establish_connection(self):
        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type)

        return connection, channel

    def publish_event(self, event_data: dict, routing_key: str):
        """
        Publishes the provided event data to the RabbitMQ exchange using
        the specified routing key.
        """
        calling_file = inspect.stack()[2].filename.split('/')[-1]
        try:
            event_data["timestamp"] = str(datetime.now())

            self.channel.basic_publish(
                exchange=self.exchange_name,
                routing_key=routing_key,
                body=json.dumps(event_data)
            )
            print(
                f'{calling_file}: Successufully published event for "{routing_key}"')
            logger.info(
                f'{calling_file}: Successufully published event for "{routing_key}"')
            return True

        except pika.exceptions.AMQPConnectionError as e:
            print(
                f'{calling_file}: Failed to publish event for "{routing_key}": {e}')
            logger.error(
                f'{calling_file}: Failed to publish event for "{routing_key}": {e}')
            return False

        except Exception as e:
            print(f'Failed to publish event for "{routing_key}": {e}')
            logger.error(f'Failed to publish event for "{routing_key}": {e}')
            return False

    def consume_event(self, exchange, routing_key, on_message_callback):
        """
        Subscribes to the specified RabbitMQ exchange and routing key, and it
        invokes the provided callback function whenever a message is received.

        Args:
            exchange: The name of the exchange to subscribe to.
            routing_key: The routing key to subscribe to.
            on_message_callback: The callback function to be called when a message is received.
        """
        queue_name = f'{routing_key}_queue'
        try:
            self.channel.queue_declare(queue_name)
            self.channel.exchange_declare(exchange, self.exchange_type)
            self.channel.queue_bind(queue_name, exchange, routing_key)
            self.channel.basic_consume(queue_name, on_message_callback)

            self.channel.start_consuming()
        except pika.exceptions.ConnectionClosed as e:
            logger.log(f"Connection to RabbitMQ closed: {e}")
            time.sleep(5)
        except KeyboardInterrupt:
            # Close the channel and connection
            self.close_connection()

    def close_connection(self):
        # Close the channel and connection gracefully
        self.channel.stop_consuming()
        self.connection.close()
        logger.info("RabbitMQ connection closed gracefully")
