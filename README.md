# Graph database management systems benchmark
Repository contains scripts for testing performance of following Graph DBMS:
- [ArangoDB](https://www.arangodb.com/)
- [Neo4j](https://neo4j.com/)
- [RedisGraph](http://redisgraph.io)

# Data
Following data have been used (included in [data directory](./data)) in this benchmark:
- [EUROVOC](https://op.europa.eu/pl/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/eurovoc) (CC-BY 4.0)
- [PlWN](http://plwordnet.pwr.wroc.pl/wordnet/) (Wordnet licence)

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
Note: name of dir will be used as name of new database,
1. ``setup``: Launches scripts needed to be run **before** querying the database,
1. ``query_all``: launches all queries defined for this service, outputs
   name of query file and execution time **in milliseconds**,


Note: for now you have to manually run (first time) ``docker-compose up neo4j-loader``
and wait for the end before starting neo4j with ``docker-compose up neo4j``

# launching
**Note: this benchmarking system is not fully automated, so you must wait for**
**finishing each of phases mentioned below before executing next one**

In below commands, ``NEO4J_SRV``, ``NEO4J_SRV_LOADER``, ``REDIS_SRV`` represents
name of docker-compose service.

## data
Before starting test, extract archive stored in [data](data) into every db directory
wchich will be tested.

## Neo4j
1. ``docker-compose up NEO4J_SRV_LOADER``
1. ``docker-compose up NEO4J_SRV``
1. ``docker-compose exec NEO4J_SRV setup``
1. ``docker-compose exec NEO4J_SRV query_all``

## Redis
1. ``docker-compose up REDIS_SRV``
1. ``docker-compose exec REDIS_SRV import``
1. ``docker-compose exec REDIS_SRV setup``
1. ``docker-compose exec REDIS_SRV query_all``

## ArangoDB
_Note: setting index and querying not automated with scripts_

1. ``docker-compose up ARANGODB_SRV``
1. ``docker-compose exec REDIS_SRV import``


## Volumes
Data stored by containers are stored in docker volumes:
- graph-dbms-benchmark_neo4j_data_eurovoc
- graph-dbms-benchmark_neo4j_data_plwn
- graph-dbms-benchmark_redis_data_eurovoc
- graph-dbms-benchmark_redis_data_plwn
- graph-dbms-benchmark_arangodb_data_eurovoc
- graph-dbms-benchmark_redis_data_plwn

# Available test cases and relevant services
_Note: original data has been converted (with [tool included in this repo](tools/make_nodes_rels_files))_
_and thus data size may be different than specified in official sources_
1. testing on [EUROVOC](https://op.europa.eu/pl/web/eu-vocabularies/dataset/-/resource?uri=http://publications.europa.eu/resource/dataset/eurovoc), with indexing for ``concept`` on ``lod_url`` property
  - data size:
  	- 953 710 nodes
  	- 469 462 relationships
  - services
  	- **RedisGraph**: ``redis-eurovoc``
  	- **Neo4j**: ``neo4j-eurovoc`` and ``neo4j-loader-eurovoc``
1. testing on [PlWN](http://plwordnet.pwr.wroc.pl/wordnet/), with indexing for ``concept`` on ``lod_url`` property
  - data size:
    - 5 851 624 nodes
    - 2 925 804 relationships
  - services
   	- **RedisGraph**: ``redis-plwn``
   	- **Neo4j**: ``neo4j-plwn`` and ``neo4j-loader-plwn``

# Queries
## Cypher
Queries used in benchmark:

* [01_count_relationships](neo4j/queries_eurovoc/01_count_relationships.cypher)
```
MATCH (c:concept)-[r:prefLabel]-(l:label)
RETURN count(r);
```

* [02b_count_context_nodes_nonexistent](neo4j/queries_eurovoc/02b_count_context_nodes_nonexistent.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/dummy_id"
RETURN count(m);
```

* [02_count_context_nodes:eurovoc](neo4j/queries_eurovoc/02_count_context_nodes.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/5522"
RETURN count(m);
```

* [02_count_context_nodes:plwn](neo4j/queries_plwn/02_count_context_nodes.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"
RETURN count(m);
```

* [03_substring_check_simple](neo4j/queries_eurovoc/03_substring_check_simple.cypher)
```
MATCH (n:concept)--(l:label {lang:"en"})
WHERE l.text CONTAINS 'car'
RETURN n, l
```

* [04_substring_check_complex](neo4j/queries_eurovoc/04_substring_check_complex.cypher)
```
MATCH (l1:label {lang:"en"})--(n1:concept)-[:broader|:narrower]-(n2:concept)--(l2:label {lang:"en"})
WHERE l1.text CONTAINS l2.text
RETURN n1, l1, n2, l2
```

* [05_labels_equivalence](neo4j/queries_eurovoc/05_labels_equivalence.cypher)
```
MATCH (l_pl:label {lang:"pl"})--(n:concept)--(l_en:label {lang:"en"})
WHERE l_pl.text = l_en.text
RETURN n, l_pl, l_en;
```

* [06a_count_triangles](neo4j/queries_eurovoc/06a_count_triangles.cypher)
```
MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
MATCH (c1)-[r*1..2]-(c2)
RETURN count(r);
```

* [06b_count_triangles](neo4j/queries_eurovoc/06b_count_triangles.cypher)
```
MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
WITH c1, c2 (c1)-[r*1..2]-(c2)
RETURN count(r);
```

* [07a_shortest_path:eurovoc](neo4j/queries_eurovoc/07a_shortest_path.cypher)
```
MATCH (credit:concept {lod_url:"http://eurovoc.europa.eu/289"}), (bureau_of_consumers:concept {lod_url:"http://eurovoc.europa.eu/4859"})
RETURN shortestPath((credit)-[*..5]->(bureau_of_consumers));
```

* [07a_shortest_path:plwn](neo4j/queries_plwn/07a_shortest_path.cypher)
```
MATCH (dog:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"}), (bone:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/6476"})
RETURN shortestPath((dog)-[*..5]->(bone));

```

* [08_get_sorted_labels](neo4j/queries_eurovoc/08_get_sorted_labels.cypher)
```
MATCH (c:concept)-[r:prefLabel]-(l:label {lang:"en"})
RETURN l.text
ORDER BY l.text
LIMIT 50;
```

## AQL

* [01_count_relationships](arangodb/queries_eurovoc/01_count_relationships.aql)
```
RETURN LENGTH(prefLabel)
```

* [02_count_context_nodes](arangodb/queries_eurovoc/02_count_context_nodes.aql)
```
let startNodeId = FIRST(FOR c in concept
  FILTER c.lod_url == "http://eurovoc.europa.eu/5522"
  LIMIT 1
  RETURN c._id)

FOR v, e, p in 1..5 OUTBOUND startNodeId
  broader, related, prefLabel, altLabel, definition,
  editorialNote, inScheme, topConceptOf, scopeNote
  COLLECT WITH COUNT INTO ctx_size
  RETURN ctx_size
```

* [03_substring_check_simple](arangodb/queries_eurovoc/03_substring_check_simple.aql)
```
FOR l in label
  FILTER l.lang == "en"
  FILTER CONTAINS(l.text, "car")
  FOR v, e in INBOUND l._id
    prefLabel, altLabel
    RETURN {
        lod_url: v.lod_url,
        text: l.text
    }
```

* [04_substring_check_complex](arangodb/queries_eurovoc/04_substring_check_complex.aql)
```
FOR l1 in label
  FILTER l1.lang == "en"
  FOR l2 in label
    FILTER l2.lang == "en"
    FILTER CONTAINS(l1.text, l2.text)
  FOR v1, e1 in OUTBOUND l1._id
    prefLabel, altLabel
    FOR v2, e2 in OUTBOUND l2._id
      prefLabel, altLabel
      FOR v3, e3 in OUTBOUND v1._id
      broader
      FILTER e3._from == v1._id AND e3._to == v2._id
RETURN {
    text1: l1.text,
    lod_url1: v1.lod_url,
    lod_url2: v2.lod_url,
    text2: l2.text
}
```

* [05b_labels_equivalence](arangodb/queries_eurovoc/05b_labels_equivalence.aql)
```
LET en_labels = (FOR l in label
  FILTER l.lang == "en"
  RETURN l)

LET substr_labels = (
  FOR l1 IN en_labels
    FOR l2 IN en_labels
      FILTER CONTAINS(l1.text, l2.text)
      RETURN {
        "longer": l1,
        "shorter": l2
      }
)

FOR lbls in substr_labels
  FOR v1, e1 in OUTBOUND lbls.longer._id
    prefLabel, altLabel
    FOR v2, e2 in OUTBOUND lbls.shorter._id
      prefLabel, altLabel
      FOR v3, e3 in OUTBOUND v1._id
      broader
      FILTER e3._from == v1._id AND e3._to == v2._id
RETURN {
    text1: lbls.longer.text,
    lod_url1: v1.lod_url,
    lod_url2: v2.lod_url,
    text2: lbls.shorter.text
}
```

* [05_labels_equivalence](arangodb/queries_eurovoc/05_labels_equivalence.aql)
```
LET en_labels = (FOR l1 in label
  FILTER l1.lang == "en"
  RETURN l1.text)

LET pl_labels = (FOR l2 in label
  FILTER l2.lang == "pl"
  RETURN l2.text)

LET eq_labels = (INTERSECTION(pl_labels, en_labels))

FOR l in label
  FILTER POSITION(eq_labels, l.text)
  FOR v, e in 1..1 INBOUND l._id
  prefLabel, altLabel
  RETURN {
    text: l.text,
    lod_url: v.lod_url
  }
```

* [07_get_sorted_labels](arangodb/queries_eurovoc/07_get_sorted_labels.aql)
```
FOR l in label
  FILTER l.lang == "en"
  FOR v, e in INBOUND l._id
    prefLabel
    SORT l.text
    LIMIT 50
    RETURN {
        text: l.text
    }
```

* [08_shortest_path](arangodb/queries_eurovoc/08_shortest_path.aql)
```
let creditId = FIRST(FOR c in concept
  FILTER c.lod_url == "http://eurovoc.europa.eu/289"
  LIMIT 1
  RETURN c._id)

let bureauOfConsumersId = FIRST(FOR c in concept
  FILTER c.lod_url == "http://eurovoc.europa.eu/4859"
  LIMIT 1
  RETURN c._id)

FOR v, e
  IN OUTBOUND SHORTEST_PATH
  creditId TO bureauOfConsumersId
  broader, related, prefLabel, altLabel, definition,
  editorialNote, inScheme, topConceptOf, scopeNote
  return e
```
