import pytest
import A_GIS.Text.split_first_sentence


def test_split_with_clear_first_sentence():
    text = "This is the first sentence. This is the second sentence."
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "This is the first sentence."
    assert remaining_text == " This is the second sentence."
    assert first_sentence + remaining_text == text


def test_split_with_no_sentences():
    text = "       "
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "       "
    assert remaining_text == ""
    assert first_sentence + remaining_text == text


def test_split_with_abbreviation_in_first_sentence():
    text = "Dr. Smith visited Washington, D.C. yesterday. This is the second sentence."
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "Dr. Smith visited Washington, D.C. yesterday."
    assert remaining_text == " This is the second sentence."
    assert first_sentence + remaining_text == text


def test_split_with_no_first_sentence():
    text = "This is the only sentence."
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "This is the only sentence."
    assert remaining_text == ""
    assert first_sentence + remaining_text == text


def test_split_with_multiple_periods_in_first_sentence():
    text = "This... is the first sentence. And this is the second one."
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "This... is the first sentence."
    assert remaining_text == " And this is the second one."
    assert first_sentence + remaining_text == text


# This test ensures that the function gracefully handles an empty string
def test_split_with_empty_string():
    text = ""
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == ""
    assert remaining_text == ""
    assert first_sentence + remaining_text == text


def test_split_with_indented_first_sentence():
    text = "    This is the first sentence. This is the second sentence."
    first_sentence, remaining_text = A_GIS.Text.split_first_sentence(text=text)
    assert first_sentence == "    This is the first sentence."
    assert remaining_text == " This is the second sentence."
    assert first_sentence + remaining_text == text
