MATCH (l_pl:label {lang:"pl"})--(n:concept)--(l_en:label {lang:"en"})
WHERE l_pl.text = l_en.text
RETURN n, l_pl, l_en;