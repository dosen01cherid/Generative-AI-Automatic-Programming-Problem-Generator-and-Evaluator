"""
Ollama Context Client (DeepSeek R1–Compatible, Fixed Output)
------------------------------------------------------------
Handles DeepSeek's multi-part reasoning & response output properly.
"""

import requests
import json
import math
from pathlib import Path
from typing import Optional

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://visits-fine-deferred-predicted.trycloudflare.com"
GEN_MODEL = "deepseek-r1:7b"
TIMEOUT = 600
CONTEXT_FILE = "context.txt"
MODEL_CONTEXT_SIZE = 128_000
AVG_CHARS_PER_TOKEN = 4.0
SHOW_THINKING = True
# =======================================================

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
    """Rough token count estimate."""
    return math.ceil(len(text) / AVG_CHARS_PER_TOKEN)


def generate_full_response(prompt: str, model: str = GEN_MODEL) -> str:
    """
    Collects all responses from Ollama (DeepSeek-friendly).
    DeepSeek sends JSON lines containing both 'thinking' and 'response'.
    """
    response_text_parts = []
    thinking_text_parts = []

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
                except json.JSONDecodeError:
                    continue

                # 🧩 Handle DeepSeek 'thinking'
                if "thinking" in data and data["thinking"]:
                    thinking_text_parts.append(data["thinking"])
                    if SHOW_THINKING:
                        print(f"\r💭 {data['thinking']}", end="", flush=True)

                # 🧩 Handle DeepSeek 'response' (may come in chunks)
                if "response" in data and data["response"]:
                    response_text_parts.append(data["response"])

                # 🧩 Stop when done
                if data.get("done", False):
                    break

    except Exception as e:
        print(f"\n❌ Error while receiving: {e}")

    # 🧠 Combine outputs
    thinking_text = "".join(thinking_text_parts).strip()
    response_text = "".join(response_text_parts).strip()

    if SHOW_THINKING and thinking_text:
        print("\n\n🧠 [Thinking completed]\n")

    return response_text


def ask_with_context(base_context: str, question: str, keep_previous: bool, model: Optional[str] = GEN_MODEL):
    """Send a question with optional previous context and show context usage."""
    global memory_context

    if keep_previous and memory_context.strip():
        combined_context = memory_context + "\n\n" + base_context
        print("🧠 Keeping previous conversation context...")
    else:
        combined_context = base_context
        memory_context = ""
        print("🧹 Starting fresh...")

    # Estimate token usage
    ctx_toks = estimate_token_usage(combined_context)
    q_toks = estimate_token_usage(question)
    total = ctx_toks + q_toks + 200
    pct = (total / MODEL_CONTEXT_SIZE) * 100
    print(f"\n📊 Context usage: {total:,}/{MODEL_CONTEXT_SIZE:,} ({pct:.2f}%)\n")

    # Build prompt
    prompt = (
        f"You are an AI assistant. Use ONLY the following context to answer.\n\n"
        f"Context:\n{combined_context}\n\n"
        f"Question: {question}\n\n"
        f"Answer clearly and concisely."
    )

    print("🚀 Querying model...\n")
    answer = generate_full_response(prompt, model)

    if answer:
        print("\n✅ Final Answer:\n")
        print(answer)
        print("\n--- End ---")
    else:
        print("❌ No final response text found (model may have stopped early).")

    # Update memory
    if keep_previous:
        memory_context += f"\n\nUser: {question}\nAssistant: {answer}"
    else:
        memory_context = ""

    print(f"🧩 Memory {'kept' if keep_previous else 'cleared'}.\n")


def main():
    print("🧩 Ollama DeepSeek Client (Thinking-Aware, Full Output) 🧠")
    print("----------------------------------------------------------")

    try:
        base_context = read_context_from_file(CONTEXT_FILE)
    except FileNotFoundError as e:
        print(e)
        print("❗ Please create a file named 'context.txt'.")
        return

    while True:
        question = input("\n❓ Enter your question (or 'exit'): ").strip()
        if question.lower() in {"exit", "quit"}:
            print("👋 Goodbye!")
            break

        keep_previous = input("🧠 Keep previous context? (y/n): ").strip().lower().startswith("y")
        ask_with_context(base_context, question, keep_previous)


if __name__ == "__main__":
    main()
