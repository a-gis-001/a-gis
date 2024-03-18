import A_GIS.Code.distill
import pytest

def test_distill_removes_docstrings():
    test_code = '\ndef example_function(param1, param2):\n    """This is a docstring."""\n    return (param1, param2)\n'
    expected_result = "\ndef example_function(param1, param2):\n    return (param1, param2)\n"
    assert A_GIS.Code.distill(code=test_code) == expected_result

def test_distill_removes_multiline_string_literals():
    ds = '"' * 3 + "I am a docstring!" + '"' * 3
    test_code = f"\ndef example_function(param1, param2):\n    {ds}\n    return (param1, param2)\n"
    expected_result = "\ndef example_function(param1, param2):\n    return (param1, param2)\n"
    assert A_GIS.Code.distill(code=test_code) == expected_result

def test_distill_removes_comments():
    test_code = "\ndef example_function(param1, param2):\n    # This is a comment.\n    return (param1, param2)\n"
    expected_result = "\ndef example_function(param1, param2):\n    return (param1, param2)\n"
    assert A_GIS.Code.distill(code=test_code) == expected_result

def test_distill_removes_all_three():
    ds = '"' * 3 + "I am a docstring!" + '"' * 3
    test_code = f'\ndef example_function(param1, param2):\n    """This is a docstring."""\n    {ds}\n    # This is a comment.\n    return (param1, param2)\n'
    expected_result = "\ndef example_function(param1, param2):\n    return (param1, param2)\n"
    print(test_code)
    print(expected_result)
    distilled_code = A_GIS.Code.distill(code=test_code)
    print(distilled_code)
    assert distilled_code == expected_result

