FROM arangodb/arangodb:3.7.10

RUN apk add --no-cache bash
COPY ./container_scripts /benchmark
ENV PATH /benchmark:$PATH
ENV LC_ALL C.UTF-8
