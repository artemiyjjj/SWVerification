FROM ubuntu:24.04

RUN apt-get update -y && \
    apt-get install -y openjdk-21-jdk curl unzip

WORKDIR app/joern
RUN curl -L "https://github.com/joernio/joern/releases/latest/download/joern-install.sh" -o joern-install.sh && \
    chmod u+x joern-install.sh && \
    ./joern-install.sh

# CMD ["joern/joern-cli"]