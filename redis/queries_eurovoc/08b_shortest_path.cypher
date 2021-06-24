MATCH p = (credit:concept {lod_url:"http://eurovoc.europa.eu/289"})-[*]-(bureau_of_consumers:concept {lod_url:"http://eurovoc.europa.eu/4859"})
WITH collect(p) AS paths, min(length(p)) AS min_len
RETURN [p in paths WHERE length(p) = min_len | p][0]
