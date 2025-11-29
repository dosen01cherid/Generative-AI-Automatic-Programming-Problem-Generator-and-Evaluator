"""
Ollama KV Cache Client (Auto-Context Preload with Progress)
---------------------------------------------------------
Automatically preloads context.txt into KV cache at startup WITH PROGRESS.
All questions (including first) are fast using cached context.
"""

import requests
import json
import math
import time
from pathlib import Path
from typing import Optional, Dict, Any
import sys
import io

# Fix encoding for Windows console to support emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://unpatented-saylor-nonirate.ngrok-free.dev"
GEN_MODEL = "qwen2.5:14b"
TIMEOUT = 600
CONTEXT_FILE = "context.txt"
MODEL_CONTEXT_SIZE = 128_000  # in tokens
AVG_CHARS_PER_TOKEN = 4.0
KEEP_ALIVE = "60m"  # Keep model loaded for 10 minutes
# =======================================================

class OllamaKVCacheClient:
    """Client that properly manages Ollama's KV cache."""

    def __init__(self, base_url: str, model: str, keep_alive: str = "10m"):
        self.base_url = base_url.rstrip('/')
        self.model = model
        self.keep_alive = keep_alive
        self.kv_cache_context = None  # Stores Ollama's context field (KV cache)
        self.base_context = ""
        self.conversation_history = []  # For display purposes

    def load_base_context(self, filepath: str) -> str:
        """Load base context from file."""
        path = Path(filepath)
        if not path.exists():
            raise FileNotFoundError(f"Context file not found: {filepath}")
        text = path.read_text(encoding="utf-8").strip()
        self.base_context = text
        print(f"📄 Loaded base context from: {filepath}")
        print(f"   Words: {len(text.split()):,} | Estimated tokens: {self.estimate_tokens(text):,}")
        return text

    def preload_context_to_cache(self):
        """
        Pre-send context to Ollama to warm up KV cache BEFORE user asks questions.
        Shows STREAMING PROGRESS so user knows something is happening.
        """
        if not self.base_context:
            print("⚠️ No base context loaded!")
            return False

        print("\n" + "="*60)
        print("🔥 PRE-WARMING KV CACHE...")
        print("="*60)
        print("📤 Sending base context to Ollama...")

        # Create a system prompt that loads context without asking a question
        preload_prompt = (
            f"You are an AI assistant. The following is your knowledge base context. "
            f"Read and remember it. Just respond with 'Ready.'\n\n"
            f"Context:\n{self.base_context}\n\n"
            f"Respond with: 'Ready.'"
        )

        context_tokens = self.estimate_tokens(self.base_context)
        print(f"📊 Loading {context_tokens:,} tokens into KV cache...")
        print("⏳ Processing", end='', flush=True)

        start_time = time.time()
        response_text = ""
        new_context = None

        try:
            # Send context WITH STREAMING to show progress
            payload = {
                "model": self.model,
                "prompt": preload_prompt,
                "stream": True,  # ← STREAMING for progress!
                "keep_alive": self.keep_alive
            }

            with requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=TIMEOUT
            ) as response:
                response.raise_for_status()

                dot_count = 0
                for line in response.iter_lines(decode_unicode=True):
                    if not line or not line.strip():
                        continue

                    try:
                        data = json.loads(line)

                        # Show progress dots
                        if "response" in data:
                            chunk = data["response"]
                            response_text += chunk

                            # Print a dot every few chunks for visual feedback
                            dot_count += 1
                            if dot_count % 3 == 0:
                                print(".", end='', flush=True)

                        # Capture the context field (KV cache) from final response
                        if data.get("done", False):
                            if "context" in data:
                                new_context = data["context"]
                            break

                    except json.JSONDecodeError:
                        continue

            elapsed = time.time() - start_time
            print()  # New line after dots

            if new_context:
                self.kv_cache_context = new_context
                print(f"⏱️  Pre-load time: {elapsed:.2f}s")
                print(f"💾 KV cache created: {len(self.kv_cache_context):,} elements")
                print(f"✅ Context successfully loaded into KV cache!")
                print(f"🚀 All questions will now be FAST (using cached context)")
                print("="*60)
                return True
            else:
                print("⚠️ No context field returned")
                return False

        except Exception as e:
            print(f"\n❌ Error pre-loading context: {e}")
            return False

    def estimate_tokens(self, text: str) -> int:
        """Rough estimate of token count."""
        return math.ceil(len(text) / AVG_CHARS_PER_TOKEN)

    def is_model_loaded(self) -> bool:
        """Check if model is currently loaded (KV cache exists)."""
        try:
            response = requests.get(f"{self.base_url}/api/ps", timeout=5)
            models = response.json().get('models', [])
            return any(m['name'].startswith(self.model) for m in models)
        except:
            return False

    def get_cache_status(self) -> Dict[str, Any]:
        """Get detailed cache status."""
        status = {
            'has_kv_cache': self.kv_cache_context is not None,
            'model_loaded': self.is_model_loaded(),
            'conversation_turns': len(self.conversation_history),
        }

        if self.kv_cache_context:
            status['cache_tokens_estimate'] = len(self.kv_cache_context)

        return status

    def clear_kv_cache(self):
        """Clear KV cache and unload model."""
        print("\n🧹 Clearing KV cache and unloading model...")
        try:
            requests.post(
                f"{self.base_url}/api/generate",
                json={
                    "model": self.model,
                    "prompt": "",
                    "keep_alive": 0  # Immediately unload
                },
                timeout=10
            )
            self.kv_cache_context = None
            self.conversation_history = []
            print("✅ KV cache cleared and model unloaded")
        except Exception as e:
            print(f"⚠️ Error clearing cache: {e}")

    def generate_with_cache(
        self,
        prompt: str,
        use_kv_cache: bool = True
    ) -> tuple[str, float]:
        """Generate response, optionally using KV cache."""
        cache_status = "🟢 WARM (using KV cache)" if (use_kv_cache and self.kv_cache_context) else "🔴 COLD (no cache)"
        print(f"\n[{cache_status}]")

        # Prepare request payload
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": True,
            "keep_alive": self.keep_alive
        }

        # Include KV cache context if using cache
        if use_kv_cache and self.kv_cache_context is not None:
            payload["context"] = self.kv_cache_context
            print(f"📦 Using cached context ({len(self.kv_cache_context):,} elements)")

        # Estimate token usage
        new_tokens = self.estimate_tokens(prompt)
        print(f"📊 New tokens to process: ~{new_tokens:,}")

        print("🚀 Generating answer...\n")

        # Stream response
        response_text = ""
        start_time = time.time()
        new_context = None

        try:
            with requests.post(
                f"{self.base_url}/api/generate",
                json=payload,
                stream=True,
                timeout=TIMEOUT,
            ) as r:
                r.raise_for_status()

                for line in r.iter_lines(decode_unicode=True):
                    if not line or not line.strip():
                        continue

                    try:
                        data = json.loads(line)

                        # Collect response text
                        if "response" in data:
                            chunk = data["response"]
                            print(chunk, end='', flush=True)
                            response_text += chunk

                        # Capture the context field (KV cache)
                        if data.get("done", False) and "context" in data:
                            new_context = data["context"]

                    except json.JSONDecodeError:
                        continue

        except Exception as e:
            print(f"\n❌ Error during generation: {e}")
            return "", 0

        elapsed_time = time.time() - start_time
        print(f"\n\n⏱️  Response time: {elapsed_time:.2f}s")

        # Update KV cache context
        if new_context is not None:
            self.kv_cache_context = new_context
            print(f"💾 KV cache updated ({len(new_context):,} elements)")

        return response_text.strip(), elapsed_time

    def ask_question(
        self,
        question: str,
        keep_cache: bool = True
    ) -> str:
        """Ask a question using the cached context."""

        # If not keeping cache, clear and reload
        if not keep_cache:
            if self.kv_cache_context is not None:
                self.clear_kv_cache()

            # Pre-load context again
            print("\n🔄 Reloading base context into fresh KV cache...")
            self.preload_context_to_cache()

        # Build question prompt (context is already in cache)
        question_prompt = (
            f"Based on the context you have, please answer this question:\n\n"
            f"IMPORTANT: Use ONLY modern C++ syntax (C++11 and later). DO NOT use old C-style code:\n"
            f"- Use new/delete or smart pointers (std::unique_ptr, std::shared_ptr) - NEVER malloc/free\n"
            f"- Use std::string - NEVER char* or char arrays for strings\n"
            f"- Use std::cout/std::cin - NEVER printf/scanf\n"
            f"- Use std::vector, std::array - prefer over raw arrays\n"
            f"- Use nullptr - NEVER NULL or 0 for pointers\n"
            f"- Use modern C++ features: auto, range-based for loops, etc.\n\n"
            f"Question: {question}\n\n"
            f"Answer clearly and concisely. Generate ONLY modern C++ code, NO old C-style constructs."
        )

        # Generate response using cached context
        answer, response_time = self.generate_with_cache(
            question_prompt,
            use_kv_cache=True
        )

        # Track conversation history
        self.conversation_history.append({
            'question': question,
            'answer': answer,
            'response_time': response_time,
            'used_cache': self.kv_cache_context is not None
        })

        return answer

    def show_statistics(self):
        """Show conversation statistics."""
        if not self.conversation_history:
            print("\n📊 No questions asked yet.")
            return

        print("\n" + "="*60)
        print("📊 SESSION STATISTICS")
        print("="*60)

        total_time = sum(turn['response_time'] for turn in self.conversation_history)

        print(f"Total questions: {len(self.conversation_history)}")
        print(f"Total response time: {total_time:.2f}s")
        print(f"Average response time: {total_time / len(self.conversation_history):.2f}s")

        # Show individual question times
        print(f"\nQuestion breakdown:")
        for i, turn in enumerate(self.conversation_history, 1):
            cache_icon = "🟢" if turn['used_cache'] else "🔴"
            print(f"  {cache_icon} Q{i}: {turn['response_time']:.2f}s - {turn['question'][:50]}...")

        print("="*60)


def main():
    print("="*60)
    print("🧠 Ollama KV Cache Client (Auto Pre-Load)")
    print("="*60)
    print("\nThis client pre-loads context.txt into KV cache at startup.")
    print("ALL questions (including first) will be FAST!\n")

    # Initialize client
    client = OllamaKVCacheClient(
        base_url=OLLAMA_URL,
        model=GEN_MODEL,
        keep_alive=KEEP_ALIVE
    )

    # Load base context from file
    try:
        client.load_base_context(CONTEXT_FILE)
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print("❗ Please create a file named 'context.txt' in the same folder.")
        return

    # PRE-LOAD context into KV cache BEFORE user asks anything
    print("\n💡 Pre-loading context into KV cache before you ask questions...")
    print("   This makes ALL questions fast, including the first one!\n")

    success = client.preload_context_to_cache()

    if not success:
        print("\n⚠️ Failed to pre-load context. Continuing anyway...")

    print("\n" + "-"*60)
    print("💡 Context is now cached! All questions will be fast.")
    print("💡 Choose 'y' to keep using cache or 'n' to reload fresh.")
    print("-"*60)

    # Main interaction loop
    while True:
        print("\n" + "="*60)
        question = input("❓ Enter your question (or 'exit'/'stats'):\n> ").strip()

        if question.lower() in {"exit", "quit"}:
            client.show_statistics()
            client.clear_kv_cache()
            print("\n👋 Goodbye!")
            break

        if question.lower() == "stats":
            client.show_statistics()
            continue

        if not question:
            print("⚠️ Please enter a question.")
            continue

        # Ask user about cache preference
        print("\n🧠 Cache Options:")
        print("  [y] Keep KV cache (FAST - use existing cached context)")
        print("  [n] Drop & reload KV cache (SLOW - fresh context reload)")

        cache_choice = input("Your choice (y/n): ").strip().lower()
        keep_cache = cache_choice.startswith('y')

        # Show current cache status
        cache_status = client.get_cache_status()
        if cache_status['has_kv_cache']:
            print(f"📦 Current cache: {cache_status['cache_tokens_estimate']:,} elements")
        else:
            print("📦 No cache (will reload)")

        # Ask question
        answer = client.ask_question(question, keep_cache=keep_cache)

        if answer:
            print(f"\n{'='*60}")
            if keep_cache:
                print("✅ Answer received using cached context")
            else:
                print("✅ Answer received with fresh context reload")
            print(f"{'='*60}")


if __name__ == "__main__":
    main()