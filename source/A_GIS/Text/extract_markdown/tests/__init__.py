# test_extract_markdown.py
import pytest
import A_GIS.Text.extract_markdown 
import textwrap

def test_extract_simple_block():
    text = """
    Hello
    
    ```python
    def hello_world():
        print("Hello, world!")
    ```
    
    That was good python.

    """
    expected_content = """
```python
def hello_world():
    print("Hello, world!")
```
""".strip("\n")
    content = A_GIS.Text.extract_markdown(text=text, block_name="python",dedent_result=True,content_only=False)
    assert content == expected_content

def test_missing_closing():
    text = """
    ```python
    def hello_world():
        print("Hello, world!")
    """
    expected_content = ""
    content = A_GIS.Text.extract_markdown(text=text, block_name="python")
    assert content == expected_content

def test_no_matching_block():
    text = """
    Some random text
    without any code blocks.
    """
    content = A_GIS.Text.extract_markdown(text=text, block_name="python")
    assert content == ""

def test_wrong_block_name():
    text = """
    ```X
    def hello_world():
        print("Hello, world!")
    ```
    """
    content = A_GIS.Text.extract_markdown(text=text, block_name="python",content_only=False)
    assert content==""

def test_regex_block_name():
    text = """
    ```X
    def hello_world():
        print("Hello, world!")
    ```
    """
    content = A_GIS.Text.extract_markdown(text=text, block_name=r"\S*",content_only=False)
    expected_content='    ```X\n    def hello_world():\n        print("Hello, world!")\n    ```'
    assert content==expected_content
