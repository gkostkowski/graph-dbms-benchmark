MATCH (n1:concept {lod_url:"http://regions.example.org/NorthHemisphere"}), (n2:concept {lod_url:"http://regions.example.org/France"})
RETURN shortestPath((n1)<-[:broader*1..3]-(n2));
