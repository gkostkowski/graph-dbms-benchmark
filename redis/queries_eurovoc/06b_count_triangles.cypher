MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
WITH c1, c2
MATCH p=(c1)-[r*1..2]-(c2)
RETURN count(relationships(p));