import A_GIS.Code.distill
import pytest


def test_distill_removes_docstring():
    test_code = """
def example_function(param1, param2):
    '''This is a docstring.'''
    return (param1, param2)
"""
    expected_result = """
def example_function(param1, param2):
    return (param1, param2)
""".strip()
    assert A_GIS.Code.distill(code=test_code) == expected_result


def test_distill_removes_docstring2():
    ds = '"' * 3 + 'I am a docstring!' + '"' * 3
    test_code = f"""
def example_function(param1, param2):
    {ds}
    return (param1, param2)
"""
    expected_result = """
def example_function(param1, param2):
    return (param1, param2)
""".strip()
    assert A_GIS.Code.distill(code=test_code) == expected_result


def test_distill_removes_comments():
    test_code = """
def example_function(param1, param2):
    # This is a comment.
    return (param1, param2)
"""
    expected_result = """
def example_function(param1, param2):
    return (param1, param2)
""".strip()
    assert A_GIS.Code.distill(code=test_code) == expected_result

