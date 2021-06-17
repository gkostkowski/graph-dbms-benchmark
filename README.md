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
Note: name of dir will be used as name of new database,
1. ``setup``: Launches scripts needed to be run **before** querying the database,
1. ``query_all``: launches all queries defined for this service, outputs
   name of query file and execution time **in milliseconds**,


Note: for now you have to manually run (first time) ``docker-compose up neo4j-loader``
and wait for the end before starting neo4j with ``docker-compose up neo4j``

# Queries
Queries used in benchmark:

1. [01_count_relationships](neo4j/queries_eurovoc/01_count_relationships.cypher)
```
MATCH (c:concept)-[r:prefLabel]-(l:label)
RETURN count(r);
```

1. [02b_count_context_nodes_nonexistent](neo4j/queries_eurovoc/02b_count_context_nodes_nonexistent.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/dummy_id"
RETURN count(m);
```

1. [02_count_context_nodes:eurovoc](neo4j/queries_eurovoc/02_count_context_nodes.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/5522"
RETURN count(m);
```

1. [02_count_context_nodes:plwn](neo4j/queries_plwn/02_count_context_nodes.cypher)
```
MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"
RETURN count(m);
```

1. [03_substring_check_simple](neo4j/queries_eurovoc/03_substring_check_simple.cypher)
```
MATCH (n:concept)--(l:label {lang:"en"})
WHERE l.text CONTAINS 'car'
RETURN n, l
```

1. [04_substring_check_complex](neo4j/queries_eurovoc/04_substring_check_complex.cypher)
```
MATCH (l1:label {lang:"en"})--(n1:concept)-[:broader|:narrower]-(n2:concept)--(l2:label {lang:"en"})
WHERE l1.text CONTAINS l2.text
RETURN n1, l1, n2, l2
```

1. [05_labels_equivalence](neo4j/queries_eurovoc/05_labels_equivalence.cypher)
```
MATCH (l_pl:label {lang:"pl"})--(n:concept)--(l_en:label {lang:"en"})
WHERE l_pl.text = l_en.text
RETURN n, l_pl, l_en;
```

1. [06a_count_triangles](neo4j/queries_eurovoc/06a_count_triangles.cypher)
```
MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
MATCH (c1)-[r*1..2]-(c2)
RETURN count(r);
```

1. [06b_count_triangles](neo4j/queries_eurovoc/06b_count_triangles.cypher)
```
MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
WITH c1, c2 (c1)-[r*1..2]-(c2)
RETURN count(r);
```

1. [07a_shortest_path:eurovoc](neo4j/queries_eurovoc/07a_shortest_path.cypher)
```
MATCH (credit:concept {lod_url:"http://eurovoc.europa.eu/289"}), (bureau_of_consumers:concept {lod_url:"http://eurovoc.europa.eu/4859"})
RETURN shortestPath((credit)-[*..5]->(bureau_of_consumers));
```

1. [07a_shortest_path:plwn](neo4j/queries_plwn/07a_shortest_path.cypher)
```
MATCH (dog:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"}), (bone:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/6476"})
RETURN shortestPath((dog)-[*..5]->(bone));

```

1. [08_get_sorted_labels](neo4j/queries_eurovoc/08_get_sorted_labels.cypher)
```
MATCH (c:concept)-[r:prefLabel]-(l:label {lang:"en"})
RETURN l.text
ORDER BY l.text
LIMIT 50;
```
