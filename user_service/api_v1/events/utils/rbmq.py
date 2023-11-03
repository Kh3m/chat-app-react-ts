import json
import pika
import dotenv
import inspect
import logging
from os import getenv
from datetime import datetime
from django.core.serializers.json import DjangoJSONEncoder


dotenv.load_dotenv()
logger = logging.getLogger("api_v1_events")


class RBMQ:
    def __init__(self, exchange_name, exchange_type):
        self.exchange_name = exchange_name
        self.exchange_type = exchange_type
        self.port = getenv("RBMQ_PORT", 5672)
        self.host = getenv("RBMQ_HOST", "localhost")

    def establish_connection(self):
        parameters = pika.ConnectionParameters(host=self.host, port=self.port)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.exchange_declare(
            exchange=self.exchange_name, exchange_type=self.exchange_type)
        return connection, channel

    def publish_event(self, event_data: dict, routing_key: str):
        calling_file = inspect.stack()[2].filename.split('/')[-1]
        try:
            _, channel = self.establish_connection()
            event_data["timestamp"] = str(datetime.now())

            channel.basic_publish(
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

    def create_event_data(self, model_instance, event_type):
        # Create a generic event dictionary
        event_data = {
            'event_type': event_type,
            'timestamp': datetime.now(),
        }

        # Update the event_data with model-specific fields
        event_data.update(model_instance.to_event_dict())

        return event_data
