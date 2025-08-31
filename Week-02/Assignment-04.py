"""📝 Assignment 4: Preprocessing Function

* Write a function to clean user input:

  * Lowercase text.
  * Remove punctuation.
  * Strip extra spaces.

"""
import re
import string
import sys

def clean_text(text):
    text = text or ""
    text = text.lower()
    text = text.translate(str.maketrans('', '', string.punctuation))
    text = re.sub(r"\s+", " ", text).strip()
    return text

if len(sys.argv) > 1:
    raw = " ".join(sys.argv[1:])
else:
    raw = input("Enter text: ")

print("Cleaned:", clean_text(raw))