# kafka2psql

This project contains a simple producer that pushes dummy messages 
into Kafka and a simple consumer that receives these  messages and 
stores them in a PostgreSQL database.

This is deliberately kept basic, e.g. no pypi package, CI, unit tests,
retry on failure, recovery logic, built-in scaling options, etc.

## Running locally in docker

Run `docker-compose up`, then to start producer: `docker exec -it kafka2psql /producer.sh`

To start consumer: `docker exec -it kafka2psql /consumer.sh`

`CTRL+C` to stop either of them.

## Running locally on host

Create a virtual env with Python 3.6+ and install packages from `requirements.txt`

If you want to use kafka and psql in docker remove the  `kafka2psql` 
container from `docker-compose.yml` and change `KAFKA_ADVERTISED_HOST_NAME` 
to localhost for the `kafka` container.

Then to start the producer `python kafka2psql/producer.py`
, and `python kafka2psql/consumer.py` to start the consumer.

By default `config.yml` file is used, if you want to specify you own set the `CONFIG_FILE` environment variable.

## Running against cloud services

To run in a cloud provider like [Aiven](https://aiven.io/) you can use
the sample `aiven_config.yml` file and specify the connection details there.

