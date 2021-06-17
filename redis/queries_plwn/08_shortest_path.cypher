MATCH (dog:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/295622"}), (bone:concept {lod_url:"http://plwordnet.pwr.wroc.pl/wordnet/synset/6476"})
RETURN shortestPath((dog)-[*..5]->(bone));
