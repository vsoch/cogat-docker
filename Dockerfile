FROM python:3.5
MAINTAINER vsochat@stanford.edu
RUN apt-get update && apt-get install -y netcat

RUN pip install --upgrade pip
RUN pip install -U docker-compose
ADD ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
# Uses docker-compose to create a multi-container deployment from code/docker-compose.yml
ADD ./ /code/

WORKDIR /code
