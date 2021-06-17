MATCH (n:concept)--(l:label {lang:"en"})
WHERE l.text CONTAINS 'car'
RETURN n, l
