MATCH (credit:concept {lod_url:"http://eurovoc.europa.eu/289"}), (bureau_of_consumers:concept {lod_url:"http://eurovoc.europa.eu/4859"})
RETURN shortestPath((credit)-[:broader*]->(bureau_of_consumers));
