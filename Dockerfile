# Container image that runs your code
FROM python:3.12-bookworm

# Install docker
RUN apt-get update && apt-get install -y docker.io tree
RUN pip install yaml

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY . /action

WORKDIR /action

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/action/entrypoint.sh"]
