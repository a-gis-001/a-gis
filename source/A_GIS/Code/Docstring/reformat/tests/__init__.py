import pytest
import A_GIS.Code.Docstring.reformat  # Adjust the import as necessary

def test_reformat_multiple_sentences():
    docstring = (
        "This is the first sentence. This is the second sentence. "
        "This is the third sentence."
    )
    expected = """This is the first sentence.

    This is the second sentence. This is the third sentence.
    """
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)
    assert test_result == expected

def test_reformat_with_leading_trailing_spaces():
    docstring = "    This is the first sentence. This is the second sentence.      "
    expected = """This is the first sentence.

    This is the second sentence.
    """
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_already_compliant():
    docstring = """This is a compliant docstring.

    It already adheres to PEP 257 conventions. There is no need to
    change its format significantly.
    """
    
    # Expect the function to recognize and not alter the compliant structure
    expected = docstring
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_empty_docstring():
    docstring = ""
    expected = ""
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_with_complex_punctuation():
    docstring = "Dr. Smith visited Washington, D.C. yesterday. This is additional text."
    expected = """Dr. Smith visited Washington, D.C. yesterday.

    This is additional text.
    """
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_single_sentence_with_newline():
    docstring = "This is a single sentence with a newline character.\n"
    expected = "This is a single sentence with a newline character."
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_multiline_with_blank_lines():
    docstring = """This is the first sentence.

    This is a second sentence, followed by a blank line.

    This should be a new paragraph.
    """
    expected = """This is the first sentence.

    This is a second sentence, followed by a blank line.

    This should be a new paragraph.
    """
    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected

def test_reformat_with_code_block():
    docstring = """This is the first sentence. Here is a code block:

    ```python
    def example_function():
        pass
    ```

    The code block should remain untouched.
    """
    expected = """This is the first sentence.

    Here is a code block:

    ```python
    def example_function():
        pass
    ```

    The code block should remain untouched.
    """

    assert A_GIS.Code.Docstring.reformat(docstring=docstring) == expected
