# Container image that runs your code
FROM ubuntu:20.04

# Install docker
RUN apt-get update && apt-get install -y docker.io

# Copies your code file from your action repository to the filesystem path `/` of the container
COPY src /action

WORKDIR /action

# Code file to execute when the docker container starts up (`entrypoint.sh`)
ENTRYPOINT ["/usr/bin/python"]

CMD ["-e", "import os; os.system('entrypoint.sh World')"]
