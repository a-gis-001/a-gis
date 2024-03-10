import pytest
import A_GIS.Code.Docstring.clean


def test_clean_with_triple_quotes():
    input_string = '''"""
    Some content here.
    """'''
    expected_output = "\n    Some content here.\n    "
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_code_block():
    input_string = """
    ```python
    Some Python code here.
    ```
    """
    expected_output = "    Some Python code here.\n    "
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_mixed_markers():
    input_string = '''
    ```python
    Mixed content with different end marker.
    """
    '''
    expected_output = "    Mixed content with different end marker."
    print(A_GIS.Code.Docstring.clean(docstring=input_string))
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_without_markers():
    input_string = "No special markers here."
    expected_output = "No special markers here."
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_nested_markers():
    input_string = '''
    ```python
    """
    Nested markers should be stripped.
    """
    ```
    '''
    expected_output = """    Nested markers should be stripped."""
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_empty_string():
    input_string = ""
    expected_output = ""
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output
