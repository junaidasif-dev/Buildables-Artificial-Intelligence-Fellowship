"""Assignment 3: Simple Chatbot with Short-Term Memory (last 5 messages)

Usage (PowerShell):
  python .\Week-02\Assignment-03.py

Type your message and press Enter.
Type 'quit' (or 'exit' / 'q') to end the session.

Requirements:
- GROQ_API_KEY must be set in environment or in a .env file like:
    GROQ_API_KEY=your_key_here

Optional: install dependencies
  pip install groq python-dotenv
"""
from __future__ import annotations
import os
import sys
from collections import deque
from dataclasses import dataclass
from typing import Deque, List, Dict

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    # dotenv is optional; continue if not installed
    pass

try:
    from groq import Groq  # type: ignore
except ImportError:
    print("Missing dependency: groq. Install with 'pip install groq'", file=sys.stderr)
    sys.exit(1)

SYSTEM_PROMPT = "You are a concise, friendly tutor. Keep answers clear and on-topic."  # You can customize
MAX_MEMORY_MESSAGES = 5  # store last N user+assistant messages total (not counting system)

@dataclass
class ChatMessage:
    role: str  # 'user' or 'assistant'
    content: str

class MemoryChatbot:
    def __init__(self, api_key: str, model: str = "llama-3.1-8b-instant", max_memory: int = MAX_MEMORY_MESSAGES):
        self.client = Groq(api_key=api_key)
        self.model = model
        self.memory: Deque[ChatMessage] = deque(maxlen=max_memory)

    def build_messages(self, user_input: str) -> List[Dict[str, str]]:
        # Start with a system instruction
        messages: List[Dict[str, str]] = [{"role": "system", "content": SYSTEM_PROMPT}]
        # Add prior memory (already alternating user/assistant)
        for m in self.memory:
            messages.append({"role": m.role, "content": m.content})
        # Add current user message
        messages.append({"role": "user", "content": user_input})
        return messages

    def reply(self, user_input: str) -> str:
        messages = self.build_messages(user_input)
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
        )
        assistant_text = response.choices[0].message.content.strip()
        # Update memory with the new user + assistant exchange
        self.memory.append(ChatMessage(role="user", content=user_input))
        self.memory.append(ChatMessage(role="assistant", content=assistant_text))
        return assistant_text

def get_api_key() -> str:
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        print("Error: GROQ_API_KEY not set. Put it in a .env file or export the variable.", file=sys.stderr)
        sys.exit(2)
    return api_key

def main() -> None:
    api_key = get_api_key()
    bot = MemoryChatbot(api_key=api_key)

    print("Chatbot ready. Type your questions. Type 'quit' to exit.\n")
    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nExiting.")
            break

        if not user_input:
            continue  # ignore empty lines
        if user_input.lower() in {"quit", "exit", "q"}:
            print("Goodbye!")
            break

        try:
            answer = bot.reply(user_input)
            print(f"Bot: {answer}\n")
        except Exception as e:
            print(f"Error contacting model: {e}", file=sys.stderr)
            # Optionally continue or break; we'll continue

if __name__ == "__main__":
    main()
