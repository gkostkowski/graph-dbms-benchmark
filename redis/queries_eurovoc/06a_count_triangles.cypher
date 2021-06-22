// Note: query for redis differs because: "RedisGraph does not support the return
// of variable-length traversal edges 'r'. Instead, use a query in the style of: 
// 'MATCH p = (a)-[r*]->(b) RETURN relationships(p)'."

 
MATCH (c1:concept)-[:prefLabel|:altLabel]-(l:label)-[:prefLabel|:altLabel]-(c2:concept)
MATCH p=(c1)-[r*1..2]-(c2)
RETURN count(relationships(p));