import requests
import json

# Configuration
CLOUDFLARE_URL = "https://null-server-reliability-integration.trycloudflare.com"  # Replace with your actual URL
MODEL = "codellama"  # Or "deepseek-coder", "qwen2.5-coder", etc.

# Prompt for generating C++ code
prompt = """Generate a simple C++ program that displays one line of output to the screen.
Include all necessary headers and a complete main function.
The output should be: "Hello from C++!"
"""

# API endpoint
url = f"{CLOUDFLARE_URL.rstrip('/')}/api/generate"

# Request payload
payload = {
    "model": MODEL,
    "prompt": prompt,
    "stream": False,
    "options": {
        "temperature": 0.7,
        "num_predict": 300
    }
}

print("Sending request to Ollama...")
print(f"URL: {url}")
print(f"Model: {MODEL}\n")

try:
    response = requests.post(url, json=payload, timeout=60)
    response.raise_for_status()

    result = response.json()
    code = result.get('response', '')

    print("Generated C++ Code:")
    print("=" * 60)
    print(code)
    print("=" * 60)

except Exception as e:
    print(f"Error: {e}")
