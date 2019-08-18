from kafka import KafkaConsumer

from kafka2psql.config import Config
from sqlalchemy import create_engine, text
from loguru import logger


config = Config()


def get_db_connection():
    connection_string = (
        f"postgresql://{config.psql_user}:{config.psql_password}"
        f"@{config.psql_host}:{config.psql_port}/{config.psql_schema}"
    )
    return create_engine(connection_string).connect()


def deserializer(value):
    return value.decode()


def get_kafka_consumer():
    consumer_kwargs = dict(
        bootstrap_servers=f"{config.kafka_host}:{config.kafka_port}",
        group_id=config.kafka_consumer_group,
        value_deserializer=deserializer,
    )
    if config.kafka_security_protocol == "SSL":
        consumer_kwargs.update(
            dict(
                security_protocol=config.kafka_security_protocol,
                ssl_cafile=config.kafka_cafile,
                ssl_certfile=config.kafka_certfile,
                ssl_keyfile=config.kafka_keyfile,
            )
        )
    return KafkaConsumer(config.kafka_topic, **consumer_kwargs)


INSERT_STMT = text("INSERT INTO events (value) VALUES (:value)")


def main():
    conn = get_db_connection()
    consumer = get_kafka_consumer()
    logger.info("Consumer running")

    try:
        for message in consumer:
            conn.execute(INSERT_STMT, value=message.value)
            logger.info(f"Saved message: {message.value}")
    except KeyboardInterrupt:
        logger.info("Consumer shut down")
        consumer.close()


if __name__ == "__main__":
    main()
