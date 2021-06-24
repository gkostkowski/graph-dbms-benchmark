FROM redislabs/redisgraph:2.6.0
# FROM redislabs/redisgraph:2.4.6
# FROM redislabs/redisgraph:edge

RUN apt update && \
    apt install -y \
    python3 \
    python3-pip

RUN pip install redisgraph-bulk-loader
# fix redis warning
RUN echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf
COPY ./container_scripts /benchmark
ENV PATH /benchmark:$PATH
ENV LC_ALL C.UTF-8
