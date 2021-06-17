MATCH (n:concept)-[*5]->(m)
WHERE n.lod_url = "http://eurovoc.europa.eu/5522"
RETURN count(m);