import os
from pathlib import Path

import yaml
from loguru import logger


def get_from_env_or_config(config, param, default=None, param_type=None):
    if default and not param_type:
        param_type = type(default)
    elif not default and not param_type:
        param_type = str

    return param_type(os.environ.get(param.upper(), config.get(param, default)))


class Config(object):
    conf_file = None

    kafka_host = None
    kafka_port = None
    kafka_topic = None
    kafka_consumer_group = None

    kafka_security_protocol = None
    kafka_cafile = None
    kafka_certfile = None
    kafka_keyfile = None

    psql_host = None
    psql_port = None
    psql_user = None
    psql_password = None
    psql_schema = None

    def __init__(self):
        Config.load()

    @staticmethod
    def load():

        Config.conf_file = os.environ.get("CONFIG_FILE", "config.yml")

        try:
            with open(Config.conf_file, "r") as stream:
                config = yaml.load(stream, Loader=yaml.Loader)
        except Exception as e:
            logger.warning(f"Unable to read config from file: {Config.conf_file} {e}")
            config = dict()

        Config.kafka_host = get_from_env_or_config(config, "kafka_host", "localhost")
        Config.kafka_port = get_from_env_or_config(config, "kafka_port", "9092")
        Config.kafka_topic = get_from_env_or_config(config, "kafka_topic", "events")
        Config.kafka_consumer_group = get_from_env_or_config(
            config, "kafka_consumer_group", "events"
        )

        Config.psql_host = get_from_env_or_config(config, "psql_host", "localhost")
        Config.psql_port = get_from_env_or_config(config, "psql_port", "5432")
        Config.psql_user = get_from_env_or_config(config, "psql_user", "postgres")
        Config.psql_password = get_from_env_or_config(
            config, "psql_password", "postgres"
        )
        Config.psql_schema = get_from_env_or_config(config, "psql_schema", "events")

        Config.kafka_security_protocol = get_from_env_or_config(
            config, "kafka_security_protocol", None
        )

        Config.kafka_cafile = get_from_env_or_config(config, "kafka_cafile", None)
        if Config.kafka_cafile:
            Config.kafka_cafile = str(Path(Config.kafka_cafile).absolute())

        Config.kafka_certfile = get_from_env_or_config(config, "kafka_certfile", None)
        if Config.kafka_certfile:
            Config.kafka_certfile = str(Path(Config.kafka_certfile).absolute())

        Config.kafka_keyfile = get_from_env_or_config(config, "kafka_keyfile", None)
        if Config.kafka_keyfile:
            Config.kafka_keyfile = str(Path(Config.kafka_keyfile).absolute())
