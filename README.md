# Graph database management systems benchmark
Repository contains scripts for testing performance of following DBMS:
- Neo4j
- RedisGraph

# Architecture
System bases on a docker containers managed with ``docker-compose``.
``redis``, ``neo4j`` subdirectories contains definition of testing environment
(Dockerfile, bash scripts). All interaction with images should be made through
docker-compose utility.

The unified interface was introduced for each tested service (DBMS case).
Each service (may be more than one service per tested DBMS) exposes following
commands to be run with ``docker-compose exec SERVICE COMMAND``:
1. ``import``: Imports data from files in specified directory. Import directory
can be given by setting ``IMPORT_DIR`` env variable or by passing path as
positional parameter. If none is given, then import dir defaults to ``/import``.
Note: name of dir will be used as name of new database
1. ``query_all``: launches all queries defined for this service, outputs
   name of query file and execution time **in milliseconds**,

