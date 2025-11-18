"""
Ollama Stateless/Semi-Stateful Context Client (Optimized)
---------------------------------------------------------
Each run:
  1. Reads context from a text file
  2. Lets user choose whether to keep or clear previous context
  3. Estimates token usage (to show context consumption)
  4. Sends question + context to /api/generate
  5. Optionally clears memory afterward
"""

import requests
import json
import math
from pathlib import Path
from typing import Optional

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://crops-logging-teaches-performing.trycloudflare.com/"
GEN_MODEL = "gpt-oss:20b"  # Generation model
TIMEOUT = 600
CONTEXT_FILE = "context.txt"
MODEL_CONTEXT_SIZE = 128_000  # in tokens
AVG_CHARS_PER_TOKEN = 4.0
# =======================================================

# Persistent memory buffer (optional)
memory_context = ""


def read_context_from_file(filepath: str) -> str:
    """Read text context from a .txt file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Context file not found: {filepath}")
    text = path.read_text(encoding="utf-8").strip()
    print(f"📄 Loaded context from: {filepath} ({len(text.split())} words)")
    return text


def estimate_token_usage(text: str) -> int:
    """Rough estimate of token count for plain text."""
    return math.ceil(len(text) / AVG_CHARS_PER_TOKEN)


def generate_full_response(prompt: str, model: str = GEN_MODEL) -> str:
    """Collect all streaming JSON lines from Ollama into one combined string."""
    response_text = ""
    try:
        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": prompt},
            stream=True,
            timeout=TIMEOUT,
        ) as r:
            r.raise_for_status()
            for line in r.iter_lines(decode_unicode=True):
                if not line or not line.strip():
                    continue
                try:
                    data = json.loads(line)
                    if "response" in data:
                        response_text += data["response"]
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"❌ Error receiving data: {e}")
    return response_text.strip()


def ask_with_context(
    base_context: str,
    question: str,
    keep_previous: bool,
    model: Optional[str] = GEN_MODEL,
):
    """Send a question with optional previous context and show context usage."""
    global memory_context

    # Combine contexts depending on user choice
    if keep_previous and memory_context.strip():
        combined_context = memory_context + "\n\n" + base_context
        print("🧠 Keeping previous conversation context...")
    else:
        combined_context = base_context
        memory_context = ""  # clear memory if not keeping
        print("🧹 Starting fresh without previous context...")

    # Estimate context usage
    context_tokens = estimate_token_usage(combined_context)
    question_tokens = estimate_token_usage(question)
    total_tokens = context_tokens + question_tokens + 200  # buffer for instructions
    used_pct = (total_tokens / MODEL_CONTEXT_SIZE) * 100

    print(f"\n📊 Estimated context usage:")
    print(f"  Context tokens : {context_tokens:,}")
    print(f"  Question tokens: {question_tokens:,}")
    print(f"  Total estimated: {total_tokens:,} / {MODEL_CONTEXT_SIZE:,} tokens ({used_pct:.2f}% used)\n")

    # Build prompt
    augmented_prompt = (
        f"You are an AI assistant. Use ONLY the following context to answer.\n\n"
        f"Context:\n{combined_context}\n\n"
        f"Question: {question}\n\n"
        f"Answer clearly and concisely."
    )

    print("🚀 Sending prompt to Ollama...\n")
    answer = generate_full_response(augmented_prompt, model)

    if answer:
        print("🧠 Model output:\n")
        print(answer)
        print("\n--- Generation complete ---")
    else:
        print("❌ No response received from Ollama.")

    # Update memory depending on user's choice
    if keep_previous:
        memory_context += f"\n\nUser: {question}\nAssistant: {answer}"
    else:
        memory_context = ""  # clear

    print(f"🧩 Memory {'kept' if keep_previous else 'cleared'} for next question.\n")


def main():
    print("🧩 Ollama Context Client (Memory Optional) 🧠")
    print("Choose whether to preserve or reset context each time.\n")
    print("-----------------------------------------------------")

    try:
        base_context = read_context_from_file(CONTEXT_FILE)
    except FileNotFoundError as e:
        print(e)
        print("\n❗ Please create a file named 'context.txt' in the same folder.")
        return

    while True:
        question = input("\n❓ Enter your question about the context (or 'exit' to quit):\n> ")
        if question.lower() in {"exit", "quit"}:
            print("\n👋 Exiting. Context cleared.")
            break

        keep_input = input("🧠 Keep previous context? (y/n): ").strip().lower()
        keep_previous = keep_input.startswith("y")

        ask_with_context(base_context, question, keep_previous)


if __name__ == "__main__":
    main()
