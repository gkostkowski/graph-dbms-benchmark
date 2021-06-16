import pickle
import rdflib


def save(graph, filename, fmt=None):
    '''
    Small function to facilitate writing graph to file.

    Args:
        graph: rdflib.graph.Graph
        filename: basestring
        fmt: basestring
    '''
    if not fmt:
        fmt = filename.split('.')[-1]
    rdflib.plugin.register('xml', rdflib.plugin.Serializer,
             'rdflib.plugins.serializers.rdfxml', 'XMLSerializer')
    graph.serialize(destination=filename, format=fmt)


def unpickle_object(path):
    with open(path, 'rb') as f:
        return pickle.load(f)
