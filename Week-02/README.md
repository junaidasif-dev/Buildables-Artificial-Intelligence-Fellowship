# Week 02 – Conversational AI Foundations

This week focuses on core concepts and practical building blocks for a simple conversational AI system: understanding model types, speech interfaces, API usage, memory, and text preprocessing.

## Contents
- `Week2_lesson.ipynb` – Narrative lesson + Q&A + assignments + Groq API example.
- `Assignment-03.py` – Chatbot with rolling memory (last 5 exchanges) using Groq API.
- `Assignment-04.py` – Minimal text cleaning (lowercase, remove punctuation, collapse spaces).
- `Assignment-05.py` – Advanced preprocessing (lowercase, remove punctuation/numbers, stopwords, POS filter (nouns/verbs/adjectives), lemmatize or stem, length filter, optional annotated output).

## Quick Start
1. Create / activate the virtual environment if not already:
   ```powershell
   python -m venv .venv; .\.venv\Scripts\Activate.ps1
   ```
2. Install dependencies (if you add a `requirements.txt`, include `groq`, `python-dotenv`, `nltk`). For now:
   ```powershell
   pip install groq python-dotenv nltk
   python -c "import nltk; [nltk.download(r, quiet=True) for r in ['stopwords','wordnet','punkt','averaged_perceptron_tagger']]"
   ```
3. Set your Groq API key in a `.env` file at repo root:
   ```
   GROQ_API_KEY=your_key_here
   ```

## Running the Chatbot (Assignment 03)
```powershell
python .\Week-02\Assignment-03.py
```
Type messages; use `quit`, `exit`, or `q` to stop.

## Text Cleaning (Assignment 04)
```powershell
python .\Week-02\Assignment-04.py "  HELLo!!!  How ARE you?? "
```
Or run without args to be prompted.

## Preprocessing (Assignment 05)
Example usage inside Python:
```python
from Week_02.Assignment_05 import preprocess, preprocess_with_pos
print(preprocess("The quick brown foxes are jumping over lazy dogs."))
print(preprocess_with_pos("The quick brown foxes are jumping over lazy dogs."))
```
Or run it directly and follow the input prompt:
```powershell
python .\Week-02\Assignment-05.py
```

## Notes
- `preprocess_with_pos` returns items like `word->noun` after filtering.
- Memory size in chatbot is fixed at 5 recent user/assistant turns for simplicity.
- Keep prompts concise to manage token usage and cost.