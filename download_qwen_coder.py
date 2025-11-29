#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Qwen2.5-Coder Model Downloader

This script provides multiple methods to download Qwen2.5-Coder models:
1. Via Ollama (recommended for local inference)
2. Via Hugging Face transformers (for Python/PyTorch usage)
3. Via Hugging Face Hub (download model files directly)

Usage:
    python download_qwen_coder.py --method ollama --model 1.5b
    python download_qwen_coder.py --method huggingface --model 7b
    python download_qwen_coder.py --method hub --model 1.5b --output ./models
"""

import argparse
import subprocess
import sys
import os
from pathlib import Path

# Fix Windows console encoding for emojis
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except AttributeError:
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


def download_via_ollama(model_size="1.5b"):
    """
    Download Qwen2.5-Coder via Ollama.

    Args:
        model_size: Model size (1.5b, 3b, 7b, 14b, 32b)
    """
    model_name = f"qwen2.5-coder:{model_size}"

    print(f"📥 Downloading {model_name} via Ollama...")
    print(f"⚠️  Make sure Ollama is installed: https://ollama.com")
    print()

    try:
        # Check if Ollama is installed
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            print("❌ Ollama is not installed or not in PATH")
            print("   Download from: https://ollama.com")
            return False

        print(f"✅ Ollama version: {result.stdout.strip()}")
        print()

        # Pull the model
        print(f"🚀 Pulling {model_name}...")
        print("   This may take several minutes depending on model size...")
        print()

        result = subprocess.run(
            ["ollama", "pull", model_name],
            text=True
        )

        if result.returncode == 0:
            print()
            print(f"✅ Successfully downloaded {model_name}!")
            print()
            print("Test the model with:")
            print(f'   ollama run {model_name} "Write a Python hello world"')
            return True
        else:
            print(f"❌ Failed to download {model_name}")
            return False

    except FileNotFoundError:
        print("❌ Ollama command not found")
        print("   Install Ollama from: https://ollama.com")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def download_via_huggingface(model_size="1.5b", output_dir=None):
    """
    Download Qwen2.5-Coder via Hugging Face transformers.

    Args:
        model_size: Model size (1.5b, 3b, 7b, 14b, 32b)
        output_dir: Directory to save model (optional)
    """
    try:
        from transformers import AutoModelForCausalLM, AutoTokenizer
    except ImportError:
        print("❌ transformers library not installed")
        print("   Install with: pip install transformers torch")
        return False

    # Map model sizes to Hugging Face model IDs
    model_map = {
        "0.5b": "Qwen/Qwen2.5-Coder-0.5B-Instruct",
        "1.5b": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "3b": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "14b": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    }

    if model_size not in model_map:
        print(f"❌ Invalid model size: {model_size}")
        print(f"   Available sizes: {', '.join(model_map.keys())}")
        return False

    model_id = model_map[model_size]

    print(f"📥 Downloading {model_id} via Hugging Face...")
    print(f"⚠️  This will download ~{get_model_size_gb(model_size)}GB of data")
    print()

    try:
        # Download tokenizer
        print("📦 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_id,
            cache_dir=output_dir,
            trust_remote_code=True
        )
        print("✅ Tokenizer downloaded")
        print()

        # Download model
        print("📦 Downloading model weights...")
        print("   This may take a while depending on your internet connection...")
        model = AutoModelForCausalLM.from_pretrained(
            model_id,
            cache_dir=output_dir,
            trust_remote_code=True,
            device_map="auto"
        )
        print("✅ Model downloaded")
        print()

        # Save to specific directory if requested
        if output_dir:
            save_path = Path(output_dir) / f"qwen2.5-coder-{model_size}"
            save_path.mkdir(parents=True, exist_ok=True)

            print(f"💾 Saving model to {save_path}...")
            model.save_pretrained(save_path)
            tokenizer.save_pretrained(save_path)
            print(f"✅ Model saved to {save_path}")
            print()

        print("✅ Successfully downloaded Qwen2.5-Coder!")
        print()
        print("Test the model with:")
        print(f'   python -c "from transformers import AutoModelForCausalLM, AutoTokenizer; '
              f'model = AutoModelForCausalLM.from_pretrained(\'{model_id}\'); print(\'Model loaded!\')"')

        return True

    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


def download_via_hub(model_size="1.5b", output_dir="./models"):
    """
    Download Qwen2.5-Coder model files via Hugging Face Hub.

    Args:
        model_size: Model size (1.5b, 3b, 7b, 14b, 32b)
        output_dir: Directory to save model files
    """
    try:
        from huggingface_hub import snapshot_download
    except ImportError:
        print("❌ huggingface_hub library not installed")
        print("   Install with: pip install huggingface_hub")
        return False

    # Map model sizes to Hugging Face model IDs
    model_map = {
        "0.5b": "Qwen/Qwen2.5-Coder-0.5B-Instruct",
        "1.5b": "Qwen/Qwen2.5-Coder-1.5B-Instruct",
        "3b": "Qwen/Qwen2.5-Coder-3B-Instruct",
        "7b": "Qwen/Qwen2.5-Coder-7B-Instruct",
        "14b": "Qwen/Qwen2.5-Coder-14B-Instruct",
        "32b": "Qwen/Qwen2.5-Coder-32B-Instruct",
    }

    if model_size not in model_map:
        print(f"❌ Invalid model size: {model_size}")
        print(f"   Available sizes: {', '.join(model_map.keys())}")
        return False

    model_id = model_map[model_size]
    output_path = Path(output_dir) / f"qwen2.5-coder-{model_size}"

    print(f"📥 Downloading {model_id} to {output_path}...")
    print(f"⚠️  This will download ~{get_model_size_gb(model_size)}GB of data")
    print()

    try:
        print("🚀 Starting download...")
        snapshot_download(
            repo_id=model_id,
            local_dir=output_path,
            local_dir_use_symlinks=False,
            resume_download=True
        )

        print()
        print(f"✅ Successfully downloaded {model_id}!")
        print(f"📁 Model saved to: {output_path}")
        print()
        print("Model files:")
        for file in output_path.rglob("*"):
            if file.is_file():
                size_mb = file.stat().st_size / (1024 * 1024)
                print(f"   {file.name}: {size_mb:.2f} MB")

        return True

    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        return False


def get_model_size_gb(model_size):
    """Get approximate model size in GB."""
    size_map = {
        "0.5b": "1-2",
        "1.5b": "3-4",
        "3b": "6-8",
        "7b": "14-16",
        "14b": "28-32",
        "32b": "64-72",
    }
    return size_map.get(model_size, "unknown")


def list_available_models():
    """List all available Qwen2.5-Coder models."""
    print("📋 Available Qwen2.5-Coder Models:")
    print()

    models = [
        ("0.5b", "Qwen/Qwen2.5-Coder-0.5B-Instruct", "~1-2 GB", "Fastest, basic code tasks"),
        ("1.5b", "Qwen/Qwen2.5-Coder-1.5B-Instruct", "~3-4 GB", "Fast, good quality (recommended)"),
        ("3b", "Qwen/Qwen2.5-Coder-3B-Instruct", "~6-8 GB", "Balanced speed/quality"),
        ("7b", "Qwen/Qwen2.5-Coder-7B-Instruct", "~14-16 GB", "High quality"),
        ("14b", "Qwen/Qwen2.5-Coder-14B-Instruct", "~28-32 GB", "Excellent quality"),
        ("32b", "Qwen/Qwen2.5-Coder-32B-Instruct", "~64-72 GB", "Best quality, needs high-end GPU"),
    ]

    for size, model_id, disk_size, description in models:
        print(f"  {size:6s} | {model_id:45s} | {disk_size:12s} | {description}")

    print()
    print("💡 Recommendation:")
    print("   - For browser-based LLM: 0.5b or 1.5b (WebGPU compatible)")
    print("   - For local inference: 1.5b or 3b (good balance)")
    print("   - For production: 7b or 14b (best quality)")
    print()


def main():
    parser = argparse.ArgumentParser(
        description="Download Qwen2.5-Coder models",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Download 1.5B model via Ollama (recommended)
  python download_qwen_coder.py --method ollama --model 1.5b

  # Download 7B model via Hugging Face transformers
  python download_qwen_coder.py --method huggingface --model 7b

  # Download model files to specific directory
  python download_qwen_coder.py --method hub --model 1.5b --output ./models

  # List all available models
  python download_qwen_coder.py --list
        """
    )

    parser.add_argument(
        "--method",
        choices=["ollama", "huggingface", "hub"],
        default="ollama",
        help="Download method (default: ollama)"
    )

    parser.add_argument(
        "--model",
        choices=["0.5b", "1.5b", "3b", "7b", "14b", "32b"],
        default="1.5b",
        help="Model size (default: 1.5b)"
    )

    parser.add_argument(
        "--output",
        type=str,
        help="Output directory for model files (for huggingface/hub methods)"
    )

    parser.add_argument(
        "--list",
        action="store_true",
        help="List all available models"
    )

    args = parser.parse_args()

    # Show header
    print("=" * 70)
    print("🤖 Qwen2.5-Coder Model Downloader")
    print("=" * 70)
    print()

    # List models if requested
    if args.list:
        list_available_models()
        return

    # Download model
    success = False

    if args.method == "ollama":
        success = download_via_ollama(args.model)

    elif args.method == "huggingface":
        success = download_via_huggingface(args.model, args.output)

    elif args.method == "hub":
        output_dir = args.output or "./models"
        success = download_via_hub(args.model, output_dir)

    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
