MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/dummy_id"
RETURN count(m);