"""
Ollama Stateless Context Client (from .txt file, fixed)
-------------------------------------------------------
Each run:
  1. Reads context from a text file
  2. Embeds context via /api/embeddings
  3. Sends a question to /api/generate
  4. Combines streaming JSON lines into a single response
  5. Clears context afterward (stateless)
"""

import requests
import json
import numpy as np
from typing import Optional
from pathlib import Path

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://shark-terrorist-achievements-lit.trycloudflare.com"
EMBED_MODEL = "llama3.1:8b"   # or "nomic-embed-text"
GEN_MODEL = "llama3.1:8b"
TIMEOUT = 600
CONTEXT_FILE = "context.txt"  # must exist in same folder
# =======================================================


def read_context_from_file(filepath: str) -> str:
    """Read text context from a .txt file."""
    path = Path(filepath)
    if not path.exists():
        raise FileNotFoundError(f"Context file not found: {filepath}")
    text = path.read_text(encoding="utf-8").strip()
    print(f"📄 Loaded context from: {filepath} ({len(text.split())} words)")
    return text


def get_embedding(text: str, model: str = EMBED_MODEL) -> np.ndarray:
    """Return the embedding vector for a given text."""
    payload = {"model": model, "prompt": text}
    try:
        res = requests.post(f"{OLLAMA_URL}/api/embeddings", json=payload, timeout=TIMEOUT)
        res.raise_for_status()
        data = res.json()
        vector = np.array(data["embedding"], dtype=np.float32)
        return vector
    except Exception as e:
        print(f"❌ Error generating embedding: {e}")
        return np.array([])


def generate_full_response(prompt: str, model: str = GEN_MODEL) -> str:
    """Collects all streaming JSON lines from Ollama into one combined string."""
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
                if not line.strip():
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


def ask_with_context(context: str, question: str, model: Optional[str] = GEN_MODEL):
    """Embed the new context, send the question, display answer, then clear context."""
    print("📚 Creating embedding for new context ...")
    context_vec = get_embedding(context)
    if context_vec.size == 0:
        print("⚠️ Embedding failed. Proceeding without context.")
    else:
        print(f"✅ Context embedded successfully (vector dim={len(context_vec)})")

    augmented_prompt = (
        f"You are an AI assistant. Use ONLY the following context to answer.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer clearly and concisely."
    )

    print("\n🚀 Sending prompt to Ollama...\n")
    answer = generate_full_response(augmented_prompt, model)

    if answer:
        print("🧠 Model output:\n")
        print(answer)
        print("\n--- Generation complete ---")
    else:
        print("❌ No response received from Ollama.")

    # Clear context for statelessness
    del context_vec
    context = ""
    print("🧹 Context cleared — next run will start fresh.\n")


def main():
    print("🧩 Ollama Stateless Context Runner (from .txt file, fixed) 🧠")
    print("Each run embeds context from a text file, then forgets it.\n")
    print("-----------------------------------------------------")

    try:
        context = read_context_from_file(CONTEXT_FILE)
    except FileNotFoundError as e:
        print(e)
        print("\n❗ Please create a file named 'context.txt' in the same folder.")
        return

    question = input("\n❓ Enter your question about the context:\n> ")
    ask_with_context(context, question)


if __name__ == "__main__":
    main()
