"""Assignment 3: Minimal Chatbot with Last-5 Message Memory

Usage:
  python .\Week-02\Assignment-03.py

Type 'quit' to exit. Stores only the last 5 messages (user + assistant combined).

Set GROQ_API_KEY in a .env file or environment for security. Falls back to placeholder.
"""
import os, sys

try:
    from dotenv import load_dotenv; load_dotenv()
except Exception:
    pass

try:
    from groq import Groq
except ImportError:
    print("Missing dependency: groq. Install with 'pip install groq'", file=sys.stderr)
    sys.exit(1)

api_key = os.getenv("GROQ_API_KEY")

client = Groq(api_key=api_key)
memory = []  # list of {role, content}

print("Chatbot ready. Type 'quit' to exit.\n")
while True:
    try:
        user_input = input("You: ")
    except (EOFError, KeyboardInterrupt):
        print("\nExiting.")
        break

    if not user_input.strip():
        continue
    if user_input.lower() in {"quit", "exit", "q"}:
        print("Goodbye!")
        break

    # Add new user message
    memory.append({"role": "user", "content": user_input})
    memory = memory[-5:]  # keep only last 5 items (user/assistant mixed)

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=memory,
        )
        reply = response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error: {e}")
        continue

    print("Bot:", reply)
    memory.append({"role": "assistant", "content": reply})
    memory = memory[-5:]
