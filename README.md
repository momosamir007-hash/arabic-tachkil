# Adawat (أدوات): Arabic Language Toolkit

Modernized Arabic NLP API and Web Toolkit. Adawat provides a high-level wrapper around several powerful Arabic NLP libraries, offering features from vocalization (Tashkeel) to morphological analysis and entity extraction.

## Features

- **Tashkeel (Vocalization)**: Automatic Arabic text vocalization using Mishkal.
- **Morphological Analysis**: Detailed word analysis (root, stem, type, gender, number).
- **Entity Extraction**: Identifying named entities and collocations in Arabic text.
- **Text Tools**: Number-to-words conversion, language detection, and sentence segmentation.
- **Modern Web Interface**: A premium, glassmorphism-style dashboard for interacting with all tools.

## Installation

```bash
# Clone the repository
git clone https://github.com/your-repo/adawat.git
cd adawat

# Install dependencies
pip install .
```

## Running the API

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Access the web interface at `http://127.0.0.1:8000/`.

## API Usage

### Process Text
**POST** `/api/v1/process`

Request Body:
```json
{
  "text": "الشمس مشرقة",
  "action": "stem",
  "options": {}
}
```

### Advanced AI Features Setup
To use the new "Advanced AI" features (Sentiment, Stanza, Farasa), additional setup is required:
1. **Java (JRE)**: Required for the Farasa toolkit. Download from [java.com](https://java.com).
2. **Stanza Models**: Automatically downloaded on first use (~200MB).
3. **Camel Tools**: Requires a C++ compiler (like MSVC on Windows) for full installation.

## Modernization (2026)
This toolkit has been recently updated to:
- **Python 3.10+** support.
- **Standardized Type Hinting** across the `adawat/` package.
- **Pathlib** integration for cross-platform robustness.
- **Pydantic v2** validation for API security.

## License
GPL-3.0
