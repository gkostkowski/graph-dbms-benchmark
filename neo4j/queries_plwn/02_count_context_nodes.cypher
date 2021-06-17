MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"
RETURN count(m);