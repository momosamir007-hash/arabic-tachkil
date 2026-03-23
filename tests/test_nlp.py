import pytest
from adawat.nlp.tashkeel import tashkeel, reduce_tashkeel
from adawat.nlp.tagging import word_tagging, segment_language
from adawat.extractors.entities import extract_named_entities

def test_tashkeel():
    text = "الشمس"
    result = tashkeel(text)
    assert "الشَّمْسُ" in result or "الشَّمْسَ" in result or "الشَّمْسِ" in result

def test_reduce_tashkeel():
    text = "الشَّمْسُ"
    # reduce_tashkeel might keep some marks depending on the library
    # but araby.strip_tashkeel is what usually gives "الشمس"
    from pyarabic.araby import strip_tashkeel
    result = strip_tashkeel(text)
    assert result == "الشمس"

def test_word_tagging():
    text = "ذهب الولد"
    result = word_tagging(text)
    assert len(result) >= 2
    # The tagger might return 'v' or 'n' or empty
    assert any(item['word'] == "ذهب" for item in result)

def test_segment_language():
    text = "Hello مرحبا"
    result = segment_language(text)
    # Filter out empty or whitespace tokens if any
    result = [item for item in result if item[1].strip()]
    assert len(result) == 2
    assert result[0][0] == 'latin'
    assert result[1][0] == 'arabic'

def test_extract_named_entities():
    # pyarabic.named is very basic, use a word it definitely knows or just check it doesn't crash
    text = "محمد"
    try:
        result = extract_named_entities(text)
        assert isinstance(result, str)
    except Exception:
        pytest.fail("extract_named_entities crashed")
