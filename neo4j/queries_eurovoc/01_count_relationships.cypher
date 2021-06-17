MATCH (c:concept)-[r:prefLabel]-(l:label)
RETURN count(r);
