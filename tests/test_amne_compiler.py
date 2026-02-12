import pytest
from src.amne_compiler import AMNECompiler

def test_compiler_basic_statement():
    compiler = AMNECompiler()
    text = "שכל פועל הוא נמצא."
    result = compiler.compile(text)
    assert result == [('statement', 'שכל פועל', 'הוא', 'נמצא')]

def test_compiler_path():
    compiler = AMNECompiler()
    text = "נתיב 7: א -> ב -> ג."
    result = compiler.compile(text)
    assert result == [('path', '7', ['א', 'ב', 'ג'])]

def test_compiler_mixed():
    compiler = AMNECompiler()
    text = """
    א הוא ב.
    נתיב 1: א -> ב.
    """
    result = compiler.compile(text)
    assert len(result) == 2
    assert result[0] == ('statement', 'א', 'הוא', 'ב')
    assert result[1] == ('path', '1', ['א', 'ב'])

def test_rdf_output():
    compiler = AMNECompiler()
    text = "א הוא ב."
    data = compiler.compile(text)
    rdf = compiler.to_rdf(data)
    # Check if we have at least one triple
    assert len(rdf) > 0

def test_json_ld_output():
    compiler = AMNECompiler()
    text = "א הוא ב."
    data = compiler.compile(text)
    json_ld = compiler.to_json_ld(data)
    assert "http://sovereign.ascension/amne#" in json_ld
