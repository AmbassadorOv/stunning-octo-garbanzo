import json
from lark import Lark, Transformer
from rdflib import Graph, Literal, RDF, URIRef, Namespace
from rdflib.namespace import FOAF, RDFS

# Define the AMNE Ontological Grammar
grammar = r"""
    start: (statement | path)+

    statement: concept relationship concept "."
    path: "נתיב" NUMBER ":" concept ("->" concept)* "."

    concept: HEBREW_WORD (WS HEBREW_WORD)*
    relationship: REL_TERM

    HEBREW_WORD: /[\u0590-\u05FF]+/
    REL_TERM: "הוא" | "מוליך ל" | "יוצר" | "מחובר ל" | "נובע מ"
    NUMBER: /\d+/

    %import common.WS
    %ignore WS
"""

class AMNETransformer(Transformer):
    def concept(self, tokens):
        return " ".join([str(t) for t in tokens if not str(t).isspace()]).strip()

    def relationship(self, tokens):
        return str(tokens[0]).strip()

    def statement(self, items):
        return ("statement", items[0], items[1], items[2])

    def path(self, items):
        return ("path", str(items[0]), items[1:])

    def start(self, items):
        return items

class AMNECompiler:
    def __init__(self):
        self.parser = Lark(grammar, start='start')
        self.transformer = AMNETransformer()
        self.ns = Namespace("http://sovereign.ascension/amne#")

    def compile(self, text):
        tree = self.parser.parse(text)
        data = self.transformer.transform(tree)
        return data

    def to_rdf(self, data):
        g = Graph()
        g.bind("amne", self.ns)

        for item in data:
            if item[0] == "statement":
                _, subj, rel, obj = item
                s = URIRef(self.ns + subj.replace(" ", "_"))
                p = URIRef(self.ns + rel.replace(" ", "_"))
                o = URIRef(self.ns + obj.replace(" ", "_"))
                g.add((s, p, o))
                g.add((s, RDFS.label, Literal(subj)))
                g.add((o, RDFS.label, Literal(obj)))
            elif item[0] == "path":
                _, path_id, nodes = item
                path_uri = URIRef(self.ns + f"Path_{path_id}")
                g.add((path_uri, RDF.type, self.ns.Path))
                for i in range(len(nodes) - 1):
                    s = URIRef(self.ns + nodes[i].replace(" ", "_"))
                    o = URIRef(self.ns + nodes[i+1].replace(" ", "_"))
                    g.add((s, self.ns.leadsTo, o))

        return g

    def to_json_ld(self, data):
        g = self.to_rdf(data)
        return g.serialize(format='json-ld')

if __name__ == "__main__":
    sample_text = """
    שכל פועל הוא נמצא.
    נבואי נובע מ שכל פועל.
    צירוף יוצר שכל פועל.
    נתיב 1: צירוף -> שכל פועל -> נבואי.
    """
    compiler = AMNECompiler()
    compiled_data = compiler.compile(sample_text)
    print("Compiled Data:", compiled_data)

    rdf_output = compiler.to_rdf(compiled_data)
    print("\nRDF (Turtle):")
    print(rdf_output.serialize(format='turtle'))

    json_ld_output = compiler.to_json_ld(compiled_data)
    print("\nJSON-LD:")
    print(json_ld_output)
