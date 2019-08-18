FROM python:3.7

ADD kafka2psql /kafka2psql
ADD docker_config.yml /config.yml
ADD requirements.txt /requirements.txt

ADD producer.sh /producer.sh
ADD consumer.sh /consumer.sh

RUN pip install -r requirements.txt

WORKDIR /
ENV PYTHONPATH /

ENTRYPOINT ["/bin/sleep", "infinity"]