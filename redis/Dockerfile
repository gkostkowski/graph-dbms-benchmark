# FROM ubuntu:16.04
FROM redislabs/redisgraph:2.4.6

RUN apt update && \
    apt install -y \
    python3 \
    python3-pip
    
# RUN apt update && \
    # apt install -y software-properties-common \
    # gpg-agent && \
    # apt install -y python3 \
    # python3-pip \
    # apt-transport-https \
    # wget

RUN pip install redisgraph-bulk-loader
RUN echo "t1"
COPY ./container_scripts /benchmark
ENV PATH /benchmark:$PATH
ENV LC_ALL C.UTF-8
