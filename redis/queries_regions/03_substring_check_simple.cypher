MATCH (n:concept)--(l:label {lang:"pl"})
WHERE l.text CONTAINS 'Afryka'
RETURN n, l
