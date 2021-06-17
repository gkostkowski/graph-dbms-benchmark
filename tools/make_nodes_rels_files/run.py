from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os

from loader import load_graph
from handler import Handler

descr = """
Reads LOD (one or more) graph (with skos, owl schemas) in one of supported
formats (nt, n3, tsv, rdf) and generates TSV which can be passed to graph db
importing tools. Output files contains auto-generated numeric indices.
"""


def parse_args():
    parser = ArgumentParser(
        description=descr, formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '-i',
        '--input-graphs',
        dest='graphs_files',
        action='store',
        nargs='+',
        help="""Path to one or more file with graph in one of graph-like formats:
            rdf/nt/n3/tsv (triples).""")
    parser.add_argument(
        '-o',
        '--output-dir',
        action='store',
        required=True,
        help='Path to dir where output files will be stored')
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    graphs_paths = args.graphs_files
    out_files_dir = args.output_dir
    sep = '\t'
    for gpath in graphs_paths:
        graph = load_graph(gpath)
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
