from uuid import uuid4
from time import sleep
from random import random

from kafka import KafkaProducer
from loguru import logger

from kafka2psql.config import Config

config = Config()


def serializer(value):
    return value.encode()


def get_producer():
    return KafkaProducer(
        bootstrap_servers=f"{config.kafka_host}:{config.kafka_port}",
        value_serializer=serializer,
    )


def get_kafka_producer():
    producer_kwargs = dict(
        bootstrap_servers=[f"{config.kafka_host}:{config.kafka_port}"],
        value_serializer=serializer,
    )
    if config.kafka_security_protocol == "SSL":
        producer_kwargs.update(
            dict(
                security_protocol=config.kafka_security_protocol,
                ssl_cafile=config.kafka_cafile,
                ssl_certfile=config.kafka_certfile,
                ssl_keyfile=config.kafka_keyfile,
            )
        )
    return KafkaProducer(**producer_kwargs)


def send(producer, value):
    producer.send(config.kafka_topic, value)
    producer.flush()


def main():
    producer = get_kafka_producer()
    logger.info("Producer ready")
    try:
        while True:
            value = uuid4().hex
            send(producer, value)
            logger.info(f"Sent {value}...")
            sleep(random())
    except KeyboardInterrupt:
        producer.close()
        logger.info("Producer shut down")


if __name__ == "__main__":
    main()
