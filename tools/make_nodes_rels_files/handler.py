import os
from collections import defaultdict, Callable

from rdflib import SKOS, OWL, RDF
from rdflib import URIRef, Literal

SKOS_PREDICATES = SKOS._ClosedNamespace__uris
SAME_AS = OWL.term('sameAs')
RDF_TYPE = RDF.term('type')

skos_uri_to_name_idx = {v: k for k, v in SKOS_PREDICATES.items()}

class TermWriter(object):
    _cnt = 0
    _def_prop_type = ':STRING'
    term_index = {}
    
    def __init__(self, term_name, out_path, props, id_prop=None, rel_join_prop=None, sep='\t'):
        """
        Args:
        ----
            props(list): list of properties (names) without id property
            id_prop(str): name of property keeping the key. If not given,
                          then id will be autogenerated
            rel_join_prop(str): name of property which will be used to construct
                                index 'term_index' containing mapping between
                                old and new indices. 'term_index' is constructed
                                to be used in later steps when storing relations.
                                Skip this if such term won't be used in any type
                                of relation (which probably won't take place).
        """
        self._term_name = term_name
        self._out_path = out_path
        self._writer = open(out_path, 'w')
        self._props = props
        self._def_id_prop = ':ID'
        if id_prop:
            self._id_prop = id_prop
        else:
            self._id_prop = self._def_id_prop
        self._props.insert(0, self._id_prop)
        self._sep = sep
        self._rel_join_prop = rel_join_prop
        self._append_def_type = True  # all props will get string type, may be
                                      # changed in the future
        self._write_header()

    def _write_header(self):
        props = self._props
        if self._append_def_type:
            typed_props = []
            for p in self._props:
                if p != self._id_prop:
                    p = f"{p}{TermWriter._def_prop_type}"
                typed_props.append(p)
            props = typed_props
        line = self._sep.join(props)
        self._writer.write(line + '\n')

    def close(self):
        self._writer.close()

    def write(self, d):
        id_val = self._extract_id(d)
        d[self._id_prop] = id_val
        if self._rel_join_prop:
            TermWriter.term_index[d[self._rel_join_prop]] = id_val
        col_vals = []
        for k in d:
            if k not in self._props:
                print(f"WARN: Unsupported property found in data for term {self._term_name}: {k}")
        # note: id_prop key in self._props
        for p in self._props:
            if p not in d:
                raise ValueError(f"Value for compulosry key '{p}' not given!")
            col_vals.append(d[p])
        line = self._sep.join([str(e) for e in col_vals])
        line = line.replace('"', '\\"')
        self._writer.write(line + '\n')

    def _extract_id(self, d):
        """
        Returns value of custom id prop or looks for default ':ID' property key
        otherwise. Removes id key from dict.
        """
        if self._id_prop != self._def_id_prop:  # key id has been specified
            if self._id_prop not in d:
                raise ValueError(f"Value for key {self._id_prop} not given.")
            id_val = d.pop(self._id_prop)
        else:
            id_val = TermWriter._cnt  # assign cnt as id
            TermWriter._cnt += 1
        return id_val


class RelationWriter(object):
    _def_prop_type = ':STRING'
    
    def __init__(self, rel_name, out_path, from_key=None,
                 to_key=None, props=None, sep='\t'):
        """
        Args:
        ----
            props(list): list of properties of relation (not used currently)
        """
        self._rel_name = rel_name
        self._out_path = out_path
        self._writer = open(out_path, 'w')
        self._props = props
        self._from_key = from_key if from_key else ':START_ID'
        self._to_key = to_key if to_key else ':END_ID'
        if props:
            self._props = [f"{p}{RelationWriter._def_prop_type}" for p in props]
        else:
            self._props = []
        self._props.insert(0, self._from_key)
        self._props.insert(1, self._to_key)
        self._sep = sep
        self._append_def_type = True  # all props will get string type, may be
                                      # changed in the future
        self._write_header()

    def _write_header(self):
        props = self._props
        if self._append_def_type:
            typed_props = []
            for p in self._props:
                if p not in {self._from_key, self._to_key}:
                    p = f"{p}{TermWriter._def_prop_type}"
                typed_props.append(p)
            props = typed_props
        line = self._sep.join(props)
        self._writer.write(line + '\n')

    def close(self):
        self._writer.close()

    def write(self, d, term_index):
        # replace original ids with inner ids
        from_term_id = term_index[d[self._from_key]]
        to_term_id = term_index[d[self._to_key]]
        d[self._from_key] = from_term_id
        d[self._to_key] = to_term_id
        if any([k not in self._props for k in d]):
            print(f"WARN: Unsupported property found in data for term {self._term_name}: {k}")
        col_vals = []
        for p in self._props:
            if p not in d:
                raise ValueError(f"Value for compulosry key '{p}' not given!")
            col_vals.append(d[p])
        line = self._sep.join([str(e) for e in col_vals])
        self._writer.write(line + '\n')



class Handler(object):
    """
    Set of handlers for semantic triples.
    """
    def __init__(self, label_key, concept_key, out_dir, prop_predicates=None, sep='\t'):
        """
        Args:
        ----
            prop_predicates(seq): names of predicates present in processed triples.
                                  Such predicates will be treated as properties
                                  instead of relations (and will be stored in
                                  file definition of node)
        """
        self._labels = []
        self._concepts = []
        self._rels = defaultdict(list)
        self._label_key = label_key
        self._concept_key = concept_key
        self._out_dir = out_dir
        _create_dir(out_dir)
        self._prop_predicates = prop_predicates if prop_predicates else set()
        self._sep = sep
        self._labels_writer = TermWriter(
            'label',
            self._make_out_path('label'),
            ['text', 'lang', 'text@lang'],
            id_prop=None,  # auto-generated
            rel_join_prop=label_key,
            sep=sep)
        self._concepts_writer = TermWriter(
            'concept',
            self._make_out_path('concept'),
            ['lod_url',],
            # ['lod_url', 'source'],
            id_prop=None,  # auto-generated
            rel_join_prop=concept_key,
            sep=sep)
        self._rels_writers = {}

    def handle_concept(self, s):
        self._concepts.append({
            'lod_url': s.toPython()
        })

    def handle_label(self, o):
        text, lang, text_lang = literal_repr(o)
        self._labels.append({
            'text': text,
            'lang': lang,
            'text@lang': text_lang
        })

    def handle_rel(self, s, p, o):
        if p in skos_uri_to_name_idx:
            rel_name = skos_uri_to_name_idx[p]
            self._handle_known_rel(s, rel_name, o)
        elif p == SAME_AS:
            self._handle_known_rel(s, 'sameAs', o)
        elif p == RDF_TYPE:
            pass  # do nothing
        else:
            print(f"WARN: ignoring non-skos predicate: {p}")

    def _handle_known_rel(self, s, rel_name, o):
        self._gen_rel_writer(rel_name)
        self._rels[rel_name].append({
            ':START_ID': s,
            ':END_ID': o
        })

    def _gen_rel_writer(self, rel_name):
        if rel_name not in self._rels_writers:
            out_path = self._make_out_path(rel_name)
            self._rels_writers[rel_name] = RelationWriter(rel_name, out_path)

    def write(self):
        for d in self._labels:
            self._labels_writer.write(d)
        self._labels_writer.close()
        for d in self._concepts:
            self._concepts_writer.write(d)
        self._concepts_writer.close()
        # write rels
        term_index = TermWriter.term_index
        for rel_name, rel_dicts in self._rels.items():
            for rel_d in rel_dicts:
                self._rels_writers[rel_name].write(rel_d, term_index)

    def _make_out_path(self, name):
        ext = guess_ext_from_sep(self._sep)
        return f"{self._out_dir}/{name}.{ext}"

    def __call__(self, s, p, o):
        # add s to the concept file
        self.handle_concept(s)
        if p.toPython() in self._prop_predicates:
            raise NotImplementedError  # handle o as a property of s
        else:
            if isinstance(o, Literal):
                self.handle_label(o)
                __, __, text_lang = literal_repr(o)
                self.handle_rel(s.toPython(), p, text_lang)
            elif isinstance(o, URIRef):
                self.handle_concept(o)
                self.handle_rel(s.toPython(), p, o.toPython())
            else:
                print(f"WARN: Unsupported object: {o} (with predicate: {p})")


def literal_repr(rdf_literal):
    assert isinstance(rdf_literal, Literal)
    text, lang = rdf_literal.toPython(), rdf_literal.language
    text = str(text).replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = text.replace('\t', ' ')
    text = text.strip()
    if lang:
        text_lang = f"{text}@{lang}"
    else:
        text_lang = text
        lang = 'None'
    return text, lang, text_lang

def guess_ext_from_sep(sep):
    return {
        '\t': 'tsv',
        ',': 'csv',
        ' ': 'txt'
    }[sep]

def _create_dir(dpath):
    if not os.path.exists(dpath):
        os.mkdir(dpath)
