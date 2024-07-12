# Container image that runs your code
FROM python:3.12-bookworm

# Install docker
RUN apt-get update && apt-get install -y docker.io

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY src /action

WORKDIR /action

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/usr/local/bin/python"]

CMD ["-e", "import os; os.system('./src/entrypoint.sh World')"]
