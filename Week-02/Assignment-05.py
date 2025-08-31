"""📝 Assignment 5: Text Preprocessing

* Write a function that:

    * Converts text to lowercase.
    * Removes punctuation & numbers.
    * Removes stopwords (`the, is, and...`).
    * Applies stemming or lemmatization.
    * Removes words shorter than 3 characters.
    * Keeps only nouns, verbs, and adjectives (using POS tagging).
"""
import re, string
from typing import List

try:
    import nltk
    from nltk import word_tokenize, pos_tag
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer, PorterStemmer
except ImportError as e:
    raise SystemExit("Install NLTK: pip install nltk") from e

for r in ["stopwords","wordnet","punkt","averaged_perceptron_tagger"]:
    try:
        nltk.data.find(f"corpora/{r}")
    except LookupError:
        try: nltk.download(r, quiet=True)
        except Exception: pass

STOP = set(stopwords.words("english"))
KEEP = ("NN","VB","JJ")  # noun, verb, adjective prefixes
lemmatizer = WordNetLemmatizer()
stemmer = PorterStemmer()

PUNCT_NUM = re.compile(rf"[\d{re.escape(string.punctuation)}]+")

def preprocess(text: str, use_stem: bool = False) -> List[str]:
    if not text:
        return []
    text = text.lower()
    text = PUNCT_NUM.sub(" ", text)
    tokens = [t for t in word_tokenize(text) if t.isalpha()]
    tokens = [t for t in tokens if t not in STOP]
    if not tokens:
        return []
    tagged = pos_tag(tokens)
    out: List[str] = []
    for word, tag in tagged:
        if not any(tag.startswith(pref) for pref in KEEP):
            continue
        pos = 'n'
        if tag.startswith('V'): pos = 'v'
        elif tag.startswith('J'): pos = 'a'
        base = stemmer.stem(word) if use_stem else lemmatizer.lemmatize(word, pos)
        if len(base) < 3 or base in STOP:
            continue
        out.append(base)
    return out

def preprocess_string(text: str) -> str:
    return " ".join(preprocess(text))

def preprocess_with_pos(text: str, use_stem: bool = False) -> List[str]:
    """Return list like ['cat->noun','run->verb'] after full pipeline.

    Keeps same filtering rules as preprocess().
    """
    if not text:
        return []
    text = text.lower()
    text = PUNCT_NUM.sub(" ", text)
    tokens = [t for t in word_tokenize(text) if t.isalpha() and t not in STOP]
    if not tokens:
        return []
    tagged = pos_tag(tokens)
    annotated: List[str] = []
    for word, tag in tagged:
        if not any(tag.startswith(pref) for pref in KEEP):
            continue
        pos = 'n'
        label = 'noun'
        if tag.startswith('V'):
            pos = 'v'; label = 'verb'
        elif tag.startswith('J'):
            pos = 'a'; label = 'adj'
        base = stemmer.stem(word) if use_stem else lemmatizer.lemmatize(word, pos)
        if len(base) < 3 or base in STOP:
            continue
        annotated.append(f"{base}->{label}")
    return annotated

if __name__ == "__main__":
    txt = input("Enter text: ")
    print("Original:", txt)
    print("Tokens (lemma):", preprocess(txt))
    print("Tokens (stem):", preprocess(txt, use_stem=True))
    print("String:", preprocess_string(txt))
    anno = preprocess_with_pos(txt)
    print("Annotated:", '[' + ', '.join(anno) + ']')