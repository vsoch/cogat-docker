FROM python:2.7.9
MAINTAINER vsochat@stanford.edu

RUN pip install --upgrade pip
RUN pip install -U docker-compose

# Uses docker-compose to create a multi-container deployment from app/docker-compose.yml
ADD ./app/ /app/

ENTRYPOINT ["/usr/local/bin/docker-compose"]

WORKDIR /app
