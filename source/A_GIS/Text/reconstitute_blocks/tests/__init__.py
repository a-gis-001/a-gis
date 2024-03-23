import pytest
import A_GIS.Text.reconstitute_blocks
import A_GIS.Text.insert_block_placeholders

def test_reconstitute_different_indents():
	text="""
Hello

```python
def a():
  return 2
```

    There's indentation here.

    ```python
    def b():
      return 1
    ```
    
    And after this

"""
	subs,ntext = A_GIS.Text.insert_block_placeholders(text=text)
	rtext = A_GIS.Text.reconstitute_blocks(text=ntext,subs=subs)
	assert rtext==text
