import A_GIS.Text.add_indent
import pytest


def test_multiple_lines():
    """Test if spaces are added to the beginning of each line."""
    text = "Line1\nLine2\nLine3"
    expected = "    Line1\n    Line2\n    Line3"
    assert A_GIS.Text.add_indent(text) == expected


def test_multiple_lines2():
    """Test if spaces are added to the beginning of each line."""
    text = "  Line1\n  Line2\n  Line3"
    expected = "      Line1\n      Line2\n      Line3"
    assert A_GIS.Text.add_indent(text) == expected


def test_single_line():
    """Test if spaces are added to a single line string."""
    text = "Line1"
    expected = "    Line1"
    assert A_GIS.Text.add_indent(text) == expected


def test_custom_spaces():
    """Test if a custom number of spaces are correctly added."""
    text = "Line1\nLine2"
    spaces = 2
    expected = "  Line1\n  Line2"
    assert A_GIS.Text.add_indent(text, spaces) == expected


def test_empty_string():
    """Test if the function handles an empty string properly."""
    text = ""
    expected = "    "
    assert A_GIS.Text.add_indent(text) == expected


def test_no_newline():
    """Test if spaces are added when there are no newline characters."""
    text = "Line1"
    expected = "    Line1"
    assert A_GIS.Text.add_indent(text) == expected
