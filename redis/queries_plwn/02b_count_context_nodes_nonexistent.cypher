MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://plwordnet.pwr.wroc.pl/wordnet/synset/dummy_id"
RETURN count(m);