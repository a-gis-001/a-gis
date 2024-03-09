import pytest
import A_GIS.Text.replace_block


def test_replace_single_line():
    original = "Here is a simple line. And here is another line."
    find = "a simple line."
    replace_with = "a replaced line."
    expected = "Here is a replaced line. And here is another line."
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )


def test_replace_first_occurrence_only():
    original = "This block appears twice. This block appears twice."
    find = "This block appears twice."
    replace_with = "This block is replaced."
    expected = "This block is replaced. This block appears twice."
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )


def test_no_replacement_when_not_found():
    original = "This text does not contain the find block."
    find = "nonexistent block"
    replace_with = "replacement block"
    # Expect no change since the find block is not present
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == original
    )


def test_replace_with_special_characters():
    original = "Special characters: $^&*()."
    find = "$^&*()"
    replace_with = "(replaced)"
    expected = "Special characters: (replaced)."
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )


def test_replace_multiline_block():
    original = """First paragraph.
    
Here is a block of text.
And here is another block.

Conclusion."""
    find = """Here is a block of text.
And here is another block."""
    replace_with = "This is the replaced block."
    expected = """First paragraph.
    
This is the replaced block.

Conclusion."""
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )


def test_replace_with_preserved_indentation():
    original = """First line.
    Second line is indented.
    Third line is indented."""
    find = """Second line is indented.
    Third line is indented."""
    replace_with = "Replaced line with indentation."
    expected = """First line.
    Replaced line with indentation."""
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )


def test_replace_with_preserved_indentation2():
    original = """
    A B C
    D E F
      G H
    """
    find = """G H"""
    replace_with = "X"
    expected = """
    A B C
    D E F
      X
    """
    assert (
        A_GIS.Text.replace_block(
            text=original, find_block=find, replace_with=replace_with
        )
        == expected
    )
