MATCH (n:concept)-[*1..5]->(m)
WHERE n.lod_url = "http://regions.example.org/Europe"
RETURN count(m);
