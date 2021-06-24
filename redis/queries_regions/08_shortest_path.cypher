MATCH (n1:concept {lod_url:"http://regions.example.org/NorthHemisphere"}), (n2:concept {lod_url:"http://regions.example.org/France"})
RETURN [n IN nodes(shortestPath((n1)<-[:broader*1..3]-(n2))) | n.lod_url];
