# طبقة التوافقية للملفات والسكريبتات القديمة
from .config import COMMAND_TABLE, resolve_action
from .extractors.numbers import number_to_words, extract_numbered_phrases
from .extractors.entities import extract_named_entities, show_collocations, extract_all_entities
from .nlp.tashkeel import tashkeel, reduce_tashkeel, tashkeel_suggest, assistant_tashkeel, compare_tashkeel
from .nlp.stemming import light_stemmer, full_stemmer
from .nlp.tagging import word_tagging, chunk_split, get_bigrams, inverse_rhyme_sort, segment_language
from .formatters.latex import itemize, tabulize, tabbing
from .formatters.data import csv_to_python_table
from .generators.affixation import generate_affixes
from .generators.randtext import random_text
import pyarabic.araby as araby

numbers_to_words = number_to_words
التفقيط = number_to_words
number2letters = number_to_words
extractNumbered = extract_numbered_phrases
tashkeel_text = tashkeel
reduced_tashkeel_text = reduce_tashkeel
tashkeel2 = tashkeel_suggest
assistanttashkeel = assistant_tashkeel
compare_tashkeel = compare_tashkeel
extractNamed = extract_named_entities
extractEnteties = extract_all_entities
wordtag = word_tagging
chunksplit = chunk_split
bigrams = get_bigrams
inverse = inverse_rhyme_sort
segment_language = segment_language
csv_to_python_table = csv_to_python_table
affixate = generate_affixes
random_text = random_text
normalize = lambda t: t
tokenize = araby.tokenize
