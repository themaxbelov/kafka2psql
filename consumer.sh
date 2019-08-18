#!/usr/bin/env bash

export PYTHONPATH=.
export CONFIG_FILE=config.yml
#export CONFIG_FILE=aiven_config.yml

python kafka2psql/consumer.py