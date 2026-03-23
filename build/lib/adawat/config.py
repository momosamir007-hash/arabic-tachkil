import os
from typing import Dict, Any

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CACHE_PATH = os.path.join(BASE_DIR, '..', 'tmp')
os.makedirs(CACHE_PATH, exist_ok=True)

COMMAND_TABLE: Dict[str, Dict[str, str]] = {
    'affixate': {'action': 'Affixate', 'help': 'generate all word forms'},
    'collocation': {'action': 'showCollocations', 'help': 'extract collocations'},
    'chunk': {'action': 'chunk', 'help': 'Extract chunks'},
    'inverse': {'action': 'Inverse', 'help': 'inverse text'},
    'language': {'action': 'Language', 'help': 'detect arabic and latin'},
    'named': {'action': 'extractNamed', 'help': 'extract named entities'},
    'normalize': {'action': 'Normalize', 'help': 'normalize arabic text'},
    'num2word': {'action': 'NumberToLetters', 'help': 'convert numbers to words'},
    'numbered': {'action': 'extractNumbered', 'help': 'extract numbered clauses'},
    'random': {'action': 'RandomText', 'help': 'get a random text'},
    'stem': {'action': 'LightStemmer', 'help': 'morphology analysis'},
    'strip': {'action': 'StripHarakat', 'help': 'remove harakat'},
    'tashkeel': {'action': 'TashkeelText', 'help': 'vocalize text'},
    'tokenize': {'action': 'Tokenize', 'help': 'tokenize text'},
    'wordtag': {'action': 'Wordtag', 'help': 'classify words'},
    'bigrams': {'action': 'bigrams', 'help': 'extract bigrams'},
    'itemize': {'action': 'Itemize', 'help': 'convert to LaTeX itemize'},
    'tabulize': {'action': 'Tabulize', 'help': 'convert to LaTeX tabular'},
    'tabbing': {'action': 'Tabbing', 'help': 'convert to LaTeX tabbing'},
    'csv2data': {'action': 'CsvToData', 'help': 'convert CSV to python data'},
}

def resolve_action(action: str) -> str:
    return COMMAND_TABLE.get(action, {}).get('action', action)
