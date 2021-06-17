FROM neo4j:4.3.0-community

RUN apt update && \
    apt install -y \
    python3 \
    python3-pip

RUN pip3 install neo4j
COPY ./container_scripts /benchmark
ENV PATH /benchmark:/var/lib/neo4j/bin:$PATH
ENV LC_ALL C.UTF-8
