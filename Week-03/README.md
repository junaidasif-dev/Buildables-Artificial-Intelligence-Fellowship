# Joni Eats Chatbot – Week 03

A customer-ready Streamlit app that answers questions about the Joni Eats cafe using a curated knowledge base and Groq LLMs. The UI is simple, colorful, and non-technical; the assistant stays within the cafe context and avoids made-up items.

## What’s inside (folder inventory)

- `.cache/` – Cached artifacts for the retriever (TF‑IDF vectorizer and matrix) to speed up reloads.
- `app.py` – The customer-ready Streamlit app.
- `joni_eats_corpus.txt` – Single combined knowledge base with sections:
  - `### SECTION: RESTAURANT_KB` – Menu, items, prices, policies, delivery details, etc.
  - `### SECTION: CHAT_PATTERNS` – Example interactions to guide tone and structure.
  - `### SECTION: CONTEXT_FLOW` – Conversation flow hints and structure.
- `Joni_Eats_Chatbot_Project_Report.ipynb` – Full project report and backend implementation (reference).
- `Week-03_Solution.ipynb` – Lesson solution notebook for the week.
- `Week3_lesson.ipynb` – Week 3 lesson materials.
- `1 Start writing prompts like a pro.ipynb` – Practice notebook: writing effective prompts.
- `2 Design prompts for everyday work tasks.ipynb` – Practice notebook: task-focused prompting.
- `3 Use AI as a creative or expert partner.ipynb` – Practice notebook: creative/expert prompting patterns.

## Requirements
- Python 3.10+
- Packages (already installed if you followed the notebook):
  - `streamlit`, `groq`, `python-dotenv`, `scikit-learn`
- A Groq API key

## Configuration
Create a `.env` file at the repository root (one level above `Week-03`) with your key:

```
GROQ_API_KEY=your_groq_api_key_here
```

## Quick start (Windows / PowerShell)
From the repository root:

```
cd .\Week-03
streamlit run app.py
```

Then open the local URL shown in the terminal (usually http://localhost:8501).

## How it works
- Retrieval: TF‑IDF over paragraph-sized chunks from `RESTAURANT_KB`, cosine similarity to fetch the top snippets relevant to a user’s question.
- Generation: The app sends a concise system prompt + retrieved snippets to Groq Chat Completions. Defaults:
  - Model: `llama-3.1-8b-instant` (support for `llama-3.1-70b-versatile` via alias mapping)
  - Temperature: `0.2`
  - Top‑K snippets: `10`
- Guardrails: The system prompt instructs the model to stick to the context, avoid inventing items/prices, adapt to changing preferences, and avoid medical/legal advice.
- Memory: Last 10 messages are included so the bot keeps track of the ongoing conversation and doesn’t re-greet mid‑chat.

## Update the menu / knowledge base
- Edit `Week-03/joni_eats_corpus.txt`
  - Keep the 3 section headers as-is.
  - Add or refine menu items and policies under `RESTAURANT_KB`.
- After edits, restart the app (or refresh) so the retriever re-indexes content.

## Customize the UI
- Colors and header live in `app.py` (search for the `<style>` blocks):
  - Primary accent: `--joni-primary`
  - Secondary accent: `--joni-accent`
  - Background gradient: `--joni-bg1`, `--joni-bg2`
- Chat bubbles are high-contrast by design:
  - Customer (left) bubble: light background, dark text
  - Assistant (right) bubble: dark background, light text
- To add a logo, place an image in `Week-03/` and add an `<img>` tag inside the hero section in `app.py`.

## Deployment tips
- Local: `streamlit run app.py`
- Streamlit Community Cloud / container:
  - Make sure `.env` is set via project secrets.
  - Expose `app.py` as the entry point.
  - Ensure `requirements.txt` includes:
    - streamlit
    - groq
    - python-dotenv
    - scikit-learn

## Troubleshooting
- Error: `GROQ_API_KEY missing in .env at repo root`
  - Ensure `.env` exists at the repo root with a valid key.
- Model deprecation / invalid model
  - The app maps legacy Groq IDs to current ones; use `llama-3.1-8b-instant` or `llama-3.1-70b-versatile`.
- Results miss relevant items
  - Add more exact terms in the corpus; the retriever is keyword-based (TF‑IDF).
  - The app uses smaller chunk sizes and up to 10 snippets to improve recall; you may lower `min_len` or raise `top_k` in code if needed.
- Streamlit version quirks
  - If you see errors related to `experimental_*` APIs, update Streamlit: the app does not rely on them.

## Privacy & safety
- The assistant only uses the curated knowledge base and won’t invent items or prices.
- For severe allergies or guarantees, it directs customers to staff.

---
Questions or changes you want next? Theme colors, logo, or switching the retriever to BM25 for stronger keyword matching are easy follow‑ups.
