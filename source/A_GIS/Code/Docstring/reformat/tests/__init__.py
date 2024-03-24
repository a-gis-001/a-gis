import pytest
import A_GIS.Code.Docstring.reformat  
import A_GIS.Code.Docstring.init

def _assert(test_result,expected):

    assert str(test_result) == expected,'\ntest{\n'+str(test_result).replace(' ','_')+'\n}\n'+'expected{\n'+str(expected.replace(' ','_'))+'\n}\n'

def test_reformat_multiple_sentences():
    docstring = A_GIS.Code.Docstring.init(
        text="This is the first sentence. This is the second sentence. "
        "This is the third sentence."
    )
    expected = """This is the first sentence.

    This is the second sentence. This is the third sentence."""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_with_leading_trailing_spaces():
    docstring = A_GIS.Code.Docstring.init(text="    This is the first sentence. This is the second sentence.      ")
    expected = """This is the first sentence.

    This is the second sentence."""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_already_compliant():
    docstring = A_GIS.Code.Docstring.init(text="""This is a compliant docstring.

    It already adheres to PEP 257 conventions. There is no need to
    change its format significantly.
    """)
    
    # Expect the function to recognize and not alter the compliant structure
    expected = """This is a compliant docstring.

    It already adheres to PEP 257 conventions. There is no need to
    change its format significantly."""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_empty_docstring():
    docstring = A_GIS.Code.Docstring.init(text="")
    expected = ""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_with_complex_punctuation():
    docstring = A_GIS.Code.Docstring.init(text="Dr. Smith visited Washington, D.C. yesterday. This is additional text.")
    expected = """Dr. Smith visited Washington, D.C. yesterday.

    This is additional text."""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_single_sentence_with_newline():
    docstring = A_GIS.Code.Docstring.init(text="This is a single sentence with a newline character.\n")
    expected = "This is a single sentence with a newline character."
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_multiline_with_blank_lines():
    docstring = A_GIS.Code.Docstring.init(text="""This is the first sentence.

    This is a second sentence, followed by a blank line.

    This should be a new paragraph.
    """)
    expected = """This is the first sentence.

    This is a second sentence, followed by a blank line.

    This should be a new paragraph."""
    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)

def test_reformat_with_code_block():
    docstring = A_GIS.Code.Docstring.init(text="""This is the first sentence. Here is a code block:

    ```python
    def example_function():
        pass
    ```

    The code block should remain untouched.
    """)
    expected = """This is the first sentence.

    Here is a code block:

    ```python
    def example_function():
        pass
    ```

    The code block should remain untouched."""

    test_result = A_GIS.Code.Docstring.reformat(docstring=docstring)

    _assert(test_result,expected)