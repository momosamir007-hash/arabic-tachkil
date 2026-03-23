from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, Dict, Any
from adawat.config import resolve_action, COMMAND_TABLE
from adawat.extractors.numbers import number_to_words, extract_numbered_phrases
from adawat.extractors.entities import extract_named_entities, show_collocations
from adawat.nlp.tashkeel import tashkeel, tashkeel_suggest
from adawat.nlp.stemming import light_stemmer, full_stemmer
from adawat.nlp.tagging import word_tagging, chunk_split, get_bigrams, inverse_rhyme_sort, segment_language
from adawat.formatters.latex import itemize, tabulize, tabbing
from adawat.formatters.data import csv_to_python_table
from adawat.generators.affixation import generate_affixes
from adawat.generators.randtext import random_text
import pyarabic.araby as araby

app = FastAPI(title="Adawat API", description="Modern Arabic NLP API", version="0.2.0")

class ProcessRequest(BaseModel):
    action: str
    text: Optional[str] = "" 
    options: Optional[Dict[str, Any]] = Field(default={})

@app.get("/")
def read_root():
    return {"message": "مرحباً بك في واجهة أدوات (Adawat API)", "docs_url": "/docs"}

@app.post("/api/v1/process")
def process_text(request: ProcessRequest):
    action_name = resolve_action(request.action)
    text = request.text or ""
    try:
        if action_name == "NumberToLetters": result = number_to_words(text)
        elif action_name == "extractNumbered": result = extract_numbered_phrases(text)
        elif action_name == "extractNamed": result = extract_named_entities(text)
        elif action_name == "showCollocations": result = show_collocations(text)
        elif action_name == "TashkeelText": result = tashkeel(text, request.options.get('lastmark', True))
        elif action_name == "Tashkeel2": result = tashkeel_suggest(text, request.options.get('lastmark', True))
        elif action_name == "LightStemmer": result = full_stemmer(text, request.options.get('lastmark', True))
        elif action_name == "Wordtag": result = word_tagging(text)
        elif action_name == "chunk": result = chunk_split(text)
        elif action_name == "bigrams": result = get_bigrams(text)
        elif action_name == "Inverse": result = inverse_rhyme_sort(text)
        elif action_name == "Language": result = segment_language(text)
        elif action_name == "Itemize": result = itemize(text)
        elif action_name == "Tabulize": result = tabulize(text)
        elif action_name == "Tabbing": result = tabbing(text)
        elif action_name == "CsvToData": result = csv_to_python_table(text)
        elif action_name == "Affixate": result = generate_affixes(text)
        elif action_name == "StripHarakat": result = araby.strip_tashkeel(text)
        elif action_name == "Tokenize": result = araby.tokenize(text)
        elif action_name == "RandomText": result = random_text() 
        else: result = text
        
        return {"action_executed": action_name, "result": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
