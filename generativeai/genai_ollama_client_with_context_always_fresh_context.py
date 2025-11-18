"""
Ollama Stateless Context Client (from .txt file)
------------------------------------------------
Each run:
  1. Reads a context text file
  2. Embeds the context using Ollama's /api/embeddings endpoint
  3. Asks a question using that context
  4. Clears the context (stateless)

Author: ChatGPT (GPT-5)
"""

import requests
import json
import numpy as np
from typing import Optional
from pathlib import Path

# =======================================================
# 🔧 CONFIGURATION
# Replace this with your Cloudflare Tunnel URL
# Example: https://bright-deer-123abc.trycloudflare.com
# =======================================================
OLLAMA_URL = "https://favors-mic-bedding-maps.trycloudflare.com/"

# Models
EMBED_MODEL = "llama3.1:8b"  # or "nomic-embed-text" if available
GEN_MODEL = "llama3.1:8b"

# Timeouts
TIMEOUT = 600  # seconds

# Context file path
CONTEXT_FILE = "context.txt"  # 📝 Path to your .txt file
# =======================================================


def read_context_from_file(filepath: str) -> str:
    """Read the text context from a .txt file."""
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


def ask_with_context(context: str, question: str, model: Optional[str] = GEN_MODEL):
    """Send a prompt that uses the embedded context to generate an answer."""
    # 1️⃣ Create embedding for the new context (stateless)
    print("📚 Creating embedding for new context ...")
    context_vec = get_embedding(context)
    if context_vec.size == 0:
        print("⚠️ Embedding failed. Proceeding without context.")
    else:
        print(f"✅ Context embedded successfully (vector dim={len(context_vec)})")

    # 2️⃣ Build augmented prompt
    augmented_prompt = (
        f"You are an AI assistant. Use ONLY the following context to answer.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {question}\n\n"
        f"Answer clearly and concisely."
    )

    # 3️⃣ Send prompt to Ollama (non-streaming)
    print("\n🚀 Sending prompt to Ollama...\n")
    try:
        response = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={"model": model, "prompt": augmented_prompt},
            timeout=TIMEOUT
        )
        response.raise_for_status()
        data = response.json()
        answer = data.get("response", "")
        print("🧠 Model output:\n")
        print(answer)
        print("\n--- Generation complete ---")

    except Exception as e:
        print(f"❌ Error generating answer: {e}")

    # 4️⃣ Clear context (stateless)
    del context_vec
    context = ""
    print("🧹 Context cleared — next run will start fresh.\n")


def main():
    print("🧩 Ollama Stateless Context Runner (from .txt file) 🧠")
    print("Each run embeds context from a text file, then forgets it.\n")
    print("-----------------------------------------------------")

    try:
        # Read context from file
        context = read_context_from_file(CONTEXT_FILE)
    except FileNotFoundError as e:
        print(e)
        print("\n❗ Please create a file named 'context.txt' in the same folder.")
        return

    # Ask question
    question = input("\n❓ Enter your question about the context:\n> ")

    ask_with_context(context, question)


if __name__ == "__main__":
    main()
