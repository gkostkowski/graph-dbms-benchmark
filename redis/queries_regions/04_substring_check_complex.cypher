MATCH (l1:label {lang:"pl"})--(n1:concept)-[:broader|:narrower]-(n2:concept)--(l2:label {lang:"pl"})
WHERE l1.text CONTAINS l2.text
RETURN n1, l1, n2, l2
