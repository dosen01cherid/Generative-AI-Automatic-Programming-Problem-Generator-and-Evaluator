"""
Ollama KV Cache Client (CLI Version - Non-Interactive) - qwen2.5:1.5b
---------------------------------------------------------
Command-line version that accepts questions as arguments using qwen2.5:1.5b model.
This is a smaller, faster model compared to the 14b version.
Usage: python genai_ollama_client_with_context_kv_caches_cli_1.5b.py "Your question here"
"""

import requests
import json
import math
import time
from pathlib import Path
from typing import Optional, Dict, Any
import sys
import io
import argparse

# Fix encoding for Windows console to support emojis
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# =======================================================
# 🔧 CONFIGURATION
# =======================================================
OLLAMA_URL = "https://flows-billion-angels-soonest.trycloudflare.com"
GEN_MODEL = "qwen2.5:1.5b"  # Smaller, faster model
TIMEOUT = 600
CONTEXT_FILE = "context.txt"
MODEL_CONTEXT_SIZE = 128_000  # in tokens
AVG_CHARS_PER_TOKEN = 4.0
KEEP_ALIVE = "60m"  # Keep model loaded for 60 minutes
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

    def generate_with_cache(
        self,
        prompt: str,
        use_kv_cache: bool = True,
        verbose: bool = True
    ) -> tuple[str, float]:
        """Generate response, optionally using KV cache."""
        cache_status = "🟢 WARM (using KV cache)" if (use_kv_cache and self.kv_cache_context) else "🔴 COLD (no cache)"
        if verbose:
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
            if verbose:
                print(f"📦 Using cached context ({len(self.kv_cache_context):,} elements)")

        # Estimate token usage
        new_tokens = self.estimate_tokens(prompt)
        if verbose:
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
                            if verbose:
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
        if verbose:
            print(f"\n\n⏱️  Response time: {elapsed_time:.2f}s")

        # Update KV cache context
        if new_context is not None:
            self.kv_cache_context = new_context
            if verbose:
                print(f"💾 KV cache updated ({len(new_context):,} elements)")

        return response_text.strip(), elapsed_time

    def ask_question(
        self,
        question: str,
        keep_cache: bool = True,
        verbose: bool = True
    ) -> str:
        """Ask a question using the cached context."""

        # Build question prompt (context is already in cache)
        question_prompt = (
            f"Based on the context you have, please answer this question:\n\n"
            f"Question: {question}\n\n"
            f"Answer clearly and concisely."
        )

        # Generate response using cached context
        answer, response_time = self.generate_with_cache(
            question_prompt,
            use_kv_cache=True,
            verbose=verbose
        )

        # Track conversation history
        self.conversation_history.append({
            'question': question,
            'answer': answer,
            'response_time': response_time,
            'used_cache': self.kv_cache_context is not None
        })

        return answer


def main():
    parser = argparse.ArgumentParser(
        description='Ollama KV Cache Client - CLI Version',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python genai_ollama_client_with_context_kv_caches_cli.py "What is C++?"
  python genai_ollama_client_with_context_kv_caches_cli.py "Explain pointers" --quiet
        """
    )
    parser.add_argument('question', type=str, help='The question to ask')
    parser.add_argument('--quiet', '-q', action='store_true', help='Quiet mode - only show the answer')
    parser.add_argument('--context', '-c', type=str, default=CONTEXT_FILE, help='Path to context file')

    args = parser.parse_args()

    verbose = not args.quiet

    if verbose:
        print("="*60)
        print("🧠 Ollama KV Cache Client (CLI Mode)")
        print("="*60)
        print("\nThis client pre-loads context.txt into KV cache at startup.")
        print("ALL questions will be FAST!\n")

    # Initialize client
    client = OllamaKVCacheClient(
        base_url=OLLAMA_URL,
        model=GEN_MODEL,
        keep_alive=KEEP_ALIVE
    )

    # Load base context from file
    try:
        client.load_base_context(args.context)
    except FileNotFoundError as e:
        print(f"\n❌ {e}")
        print(f"❗ Please create a file named '{args.context}' in the same folder.")
        sys.exit(1)

    # PRE-LOAD context into KV cache
    if verbose:
        print("\n💡 Pre-loading context into KV cache...")

    success = client.preload_context_to_cache()

    if not success:
        print("\n⚠️ Failed to pre-load context.")
        sys.exit(1)

    if verbose:
        print("\n" + "-"*60)
        print("💡 Context is now cached! Answering your question...")
        print("-"*60)

    # Ask the question
    answer = client.ask_question(args.question, keep_cache=True, verbose=verbose)

    if args.quiet and answer:
        print(answer)

    if verbose and answer:
        print(f"\n{'='*60}")
        print("✅ Answer received using cached context")
        print(f"{'='*60}")


if __name__ == "__main__":
    main()
