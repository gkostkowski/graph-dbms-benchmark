import os
import sys
from loader import load_graph
from handler import Handler

descr = """
Reads LOD graph (with skos, owl schemas) in one of supported formats (nt, n3,
tsv, rdf) and generates TSV which can be passed to graph db importing tools.
"""


if __name__ == "__main__":
    graph_path = sys.argv[1]
    out_files_dir = sys.argv[2]
    sep = '\t'
    graph = load_graph(graph_path)
    # prop_predicates = {'prop:source'}
    prop_predicates = None
    handler = Handler(
        label_key='text@lang',
        concept_key='lod_url',
        out_dir=out_files_dir,
        prop_predicates=prop_predicates,
        sep=sep)
    for s, p, o in graph:
        handler(s, p, o)
    handler.write()
