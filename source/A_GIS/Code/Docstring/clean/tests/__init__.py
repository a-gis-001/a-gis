"""Test suite for A_GIS.Code.Docstring.clean module.

This module contains all tests for the clean function, including:
- Basic unit tests for core functionality
- Edge case tests for special scenarios
- Integration tests for complex use cases
"""
import pytest
import A_GIS.Code.Docstring.clean
import A_GIS.Text.diff


def test_clean_with_code_block():
    """Test cleaning docstrings containing code blocks."""
    input_string = """
    ```python
    Some Python code here.
    ```
    """
    expected_output = "    Some Python code here.\n    "
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_triple_quotes():
    """Test cleaning docstrings with standard triple quotes."""
    input_string = '''"""
    Some content here.
    """'''
    expected_output = "\n    Some content here.\n    "
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_raises_section():
    """Test cleaning docstrings containing a Raises section."""
    input_string = '''
    """
    Main description here.

    Raises:
        ValueError: When something goes wrong
    """
    '''
    expected_output = """
    Main description here.

"""
    output = A_GIS.Code.Docstring.clean(docstring=input_string)
    if output != expected_output:
        r = A_GIS.Text.diff(initial=expected_output, final=output)
        raise AssertionError("Mismatch:\n" + str(r.diffs))

def test_clean_with_unicode():
    """Test cleaning docstrings containing Unicode characters."""
    input_string = '''
    """
    Unicode content: 🐍 Python
    Special chars: © ® ™
    """
    '''
    expected_output = """
    Unicode content: 🐍 Python
    Special chars: © ® ™
    """
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_indented_raises():
    """Test cleaning docstrings with indented Raises sections."""
    input_string = '''
    """
    Main description.

        Raises:
            ValueError: Indented error
    """
    '''
    expected_output = """
    Main description.

"""
    assert A_GIS.Code.Docstring.clean(docstring=input_string) == expected_output


def test_clean_with_complex_docstring():
    """Test cleaning a complex docstring with multiple sections and nested content."""
    input_string = '''
    """
    Process and analyze data.

    This function takes input data and performs various operations
    to analyze and process it.

    Args:
        data (dict): Input data dictionary
        options (dict, optional): Processing options

    Example:
        ```python
        >>> data = {"key": "value"}
        >>> result = process_data(data)
        >>> print(result)
        Processed: value
        ```

    Note:
        This is a note about the function.

        ```python
        # Additional code example
        def helper():
            return True
        ```

    Raises:
        ValueError: If data is invalid
        TypeError: If options are wrong type
    """
    '''
    expected_output = """
    Process and analyze data.

    This function takes input data and performs various operations
    to analyze and process it.

    Args:
        data (dict): Input data dictionary
        options (dict, optional): Processing options

    Example:
        ```python
        >>> data = {"key": "value"}
        >>> result = process_data(data)
        >>> print(result)
        Processed: value
        ```

    Note:
        This is a note about the function.

        ```python
        # Additional code example
        def helper():
            return True
        ```

"""
    actual_output = A_GIS.Code.Docstring.clean(docstring=input_string)
    print("\nExpected output:")
    print(repr(expected_output))
    print("\nActual output:")
    print(repr(actual_output))
    assert actual_output == expected_output


