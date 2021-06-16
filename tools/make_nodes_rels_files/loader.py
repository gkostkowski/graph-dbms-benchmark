import os
import codecs
import rdflib
from rdflib.plugins.parsers import ntriples
import logging

from writer import unpickle_object

logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)


def is_local_file(filepath):
     return os.path.isfile(filepath)


def download_resource(remote, local_path=None):
    return wget.download(remote, out=local_path)


class Loader(object):
    def __init__(self, filename):
        self._fname = filename
        self._graph = None

    @property
    def graph(self):
        '''Returns rdglib.graph.Graph instance. '''
        return self._graph

    @property
    def triples(self):
        '''Returns generator of rdglib.graph.Graph instance over
            subject, predicate, object. '''
        return self._graph.__iter__()

    def load(self):
        raise NotImplementedError("Method is abstract.")


class RdfLoader(Loader):
    def __init__(self, filename):
        super(RdfLoader, self).__init__(filename)
        self.fmt = 'application/rdf+xml'

    def load(self):
        log.info("Loading graph from {} file '{}' ...".format(self.fmt, self._fname))
        self._graph = rdflib.Graph()
        self._graph.load(self._fname, format=self.fmt)


class NtLoader(Loader):
    def __init__(self, filename):
        super(NtLoader, self).__init__(filename)
        self.fmt = 'nt'
        self._uriref_workaround = True  # always try this workaround if parsing fails

    def load(self):
        log.info("Loading graph from {} file '{}' ...".format(self.fmt, self._fname))
        self._graph = rdflib.Graph()
        try:
            self._graph.parse(self._fname, format=self.fmt)
        except ntriples.ParseError:
            if self._uriref_workaround:
                # this is a workaround for known issue with failing parsing in
                # case of any URIRef which is not started with 'protocol' name
                # (e.g. 'http:'). Unfortunatelly, not all thesauri follows this 
                # requirement. In order to avoid failing on such URIRefs (such as 
                # '<d-nb.info/gnd/4079553-6>'), below code modifies regex used to
                # validate URIref that 'http:' is no longer required
                log.warn("Cannot parse file '{}', disabling requirement of "
                    "'http(s):' at the beginning of the URIRef and trying "
                    "again ...".format(self._fname))
                ntriples.uriref = '<([^\s"<>]*)>'
                ntriples.r_uriref = ntriples.re.compile(ntriples.uriref)
                self._graph.parse(self._fname, format=self.fmt)
                log.info("Succesfully loaded with disabled requirement about "
                    "precedding 'http(s):'")
            else:
                raise

class N3Loader(Loader):
    def __init__(self, filename):
        super(N3Loader, self).__init__(filename)
        self.fmt = 'n3'

    def load(self):
        log.info("Loading graph from {} file '{}' ...".format(self.fmt, self._fname))
        self._graph = rdflib.Graph()
        self._graph.parse(self._fname, format=self.fmt)

class TextTriplesLoader(Loader):
    def __init__(self, filename, delimiter='\t', def_lbl_lang=None, lang_in_label=True, lang_delimiter='@', raise_err=False):
        '''
        Args: 
        -----
            def_lbl_lang: basestring
                Label of language which will be assigned for all literals in 
                file.
            lang_in_label: boolean
                If enabled and def_lbl_lang not given, then language label with
                language separator (e.g. '@pl') will be expected at the end of 
                the literal.
            lang_delimiter: basestring
                Applicable only if lang_in_label enabled. Character which will 
                be used to separate label part and language part in literal.
                Default: '@'
            raise_err: bool
                Determines whether exception should be thrown when parsing error
                occurs. Alternatively, malformed line can be skipped.
        '''
        super(TextTriplesLoader, self).__init__(filename)
        self._filename = filename
        self._delimiter = delimiter
        self.fmt = 'text'
        self.def_lbl_lang = def_lbl_lang
        self.lang_in_label = lang_in_label
        self.lang_delimiter = lang_delimiter
        self._raise_error = raise_err
        self._triples_reader = TriplesReader(filename, delimiter, raise_err)

    def load(self):
        log.info("Loading graph from plain text file '{}' ...".format(self._fname))
        g = rdflib.Graph()
        lines = self._read_triples()
        if not lines:
            raise ValueError("File '{}' is empty".format(self._filename))
        idx = 1
        for s_str, p_str, o_str in lines:
            try:
                s = self._as_rdf_entity(s_str)
                p = self._as_rdf_entity(p_str)
                o = self._as_rdf_entity(o_str)
            except ValueError:
                if self._raise_error:
                    raise
                else:
                    log.warn(f"Cannot parse line {idx}: ({(s_str, p_str, o_str)})", 
                        exc_info=True)
            g.add((s, p, o))
            idx += 1
        self._graph = g

    def _read_triples(self):
        return self._triples_reader.read_triples()

    def _as_rdf_entity(self, text, lang=None):
        if text.startswith('http'):
            return rdflib.URIRef(text)
        else:
            if lang:
                return rdflib.Literal(text, lang=lang)
            elif self.def_lbl_lang:
                return rdflib.Literal(text, lang=self.def_lbl_lang)
            else:
                # searching for the lang label at the end of the string
                if not self.lang_delimiter in text:
                    raise ValueError("Language not specified and expected language label separator '{}' not found for literal: '{}'."
                        .format(self.lang_delimiter, text))
                literal, lang = text.split(self.lang_delimiter)
                if not lang.isalpha():
                    raise ValueError("Invalid language label: '{}'".format(lang))
                return rdflib.Literal(literal, lang=lang)

    # def register_namespace(self, name, uri):
    #     self._namespaces[name] = uri


class PickleLoader(Loader):
    def __init__(self, filename):
        super(PickleLoader, self).__init__(filename)
        self.fmt = 'bin'

    def load(self):
        log.info("Loading graph from pickled binary '{}' ...".format(self._fname))
        self._graph = unpickle_object(self._fname)


class TriplesReader(object):
    def __init__(self, filename, delimiter='\t', raise_err=False, unique=False):
        '''
        Args:
        -----
            lang_delimiter: basestring
                Applicable only if lang_in_label enabled. Character which will
                be used to separate label part and language part in literal.
                Default: '@'
            raise_err: bool
                Determines whether exception should be thrown when parsing error
                occurs. Alternatively, malformed line can be skipped.
        '''
        self._filename = filename
        self._delimiter = delimiter
        self.fmt = 'text'
        self._raise_error = raise_err
        self._unique = unique

    def read_triples(self):
        lines = []
        with codecs.open(self._filename, 'r', encoding='utf8') as ifile:
            for i, l in enumerate(ifile):
                l = l.rstrip()
                parts = l.split(self._delimiter)
                if self._has_valid_fields(parts):
                    lines.append(tuple(parts))
                else:
                    msg = "Malformed line ({}): {}" \
                        .format(str(i + 1), l.encode("utf8"))
                    if self._raise_error:
                        raise ValueError(msg)
                    else:
                        log.warn(msg)
        if self._unique:
            return list(set(lines))
        return lines

    def _has_valid_fields(self, parts):
        return len(parts) == 3 and all(f.strip() for f in parts)


ext_loader_dict = {
    'rdf': RdfLoader, 'nt': NtLoader, 'n3': N3Loader, 'txt':TextTriplesLoader,
    'tsv':TextTriplesLoader, 'bin': PickleLoader
    }

def get_loader(filename, ext=None):
    '''
    Factory method to produce certain Loader class, depending on extension.
    All loaders use rdflib, but reading file is slightly different for certain
    formats. If 'ext' skipped, then format will be guessed from path extension.

    Args:
        filename: basestring
        ext: basestring, optional

    Returns:
        instance of Loader subclass
    '''
    if not ext:
        ext = filename.split('.')[-1]
    if ext in ext_loader_dict:
        return ext_loader_dict[ext](filename)
    else:
        raise ValueError("Cannot found loader for extension: '{}'".format(ext))

def load_graph(rdf_path):
    loader_ = get_loader(rdf_path)
    loader_.load()
    return loader_.graph
