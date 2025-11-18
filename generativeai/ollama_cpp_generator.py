import requests
import json

def generate_cpp_code(cloudflare_url, prompt="Generate a simple C++ program that displays 'Hello, World!' to the screen"):
    """
    Connect to Ollama instance through cloudflared domain and generate C++ code

    Args:
        cloudflare_url: The cloudflared public domain URL (e.g., https://your-tunnel.trycloudflare.com)
        prompt: The prompt to send to Ollama
    """
    # Ensure URL doesn't end with slash
    cloudflare_url = cloudflare_url.rstrip('/')

    # Ollama API endpoint
    api_endpoint = f"{cloudflare_url}/api/generate"

    # Prepare the request payload
    payload = {
        "model": "codellama",  # You can change this to "deepseek-coder" or other code models
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    }

    print(f"Connecting to Ollama at: {cloudflare_url}")
    print(f"Prompt: {prompt}\n")
    print("Generating code...\n")

    try:
        # Make the request
        response = requests.post(
            api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            timeout=60
        )

        response.raise_for_status()

        # Parse response
        result = response.json()
        generated_code = result.get('response', '')

        print("Generated C++ Code:")
        print("=" * 60)
        print(generated_code)
        print("=" * 60)

        return generated_code

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

def generate_cpp_code_streaming(cloudflare_url, prompt="Generate a simple C++ program that displays 'Hello, World!' to the screen"):
    """
    Connect to Ollama with streaming enabled for real-time response

    Args:
        cloudflare_url: The cloudflared public domain URL
        prompt: The prompt to send to Ollama
    """
    # Ensure URL doesn't end with slash
    cloudflare_url = cloudflare_url.rstrip('/')

    # Ollama API endpoint
    api_endpoint = f"{cloudflare_url}/api/generate"

    # Prepare the request payload
    payload = {
        "model": "codellama",
        "prompt": prompt,
        "stream": True,
        "options": {
            "temperature": 0.7,
            "num_predict": 500
        }
    }

    print(f"Connecting to Ollama at: {cloudflare_url}")
    print(f"Prompt: {prompt}\n")
    print("Generated C++ Code (streaming):")
    print("=" * 60)

    try:
        # Make streaming request
        response = requests.post(
            api_endpoint,
            json=payload,
            headers={"Content-Type": "application/json"},
            stream=True,
            timeout=60
        )

        response.raise_for_status()

        full_response = ""

        # Process streaming response
        for line in response.iter_lines():
            if line:
                chunk = json.loads(line)
                text = chunk.get('response', '')
                print(text, end='', flush=True)
                full_response += text

                if chunk.get('done', False):
                    break

        print("\n" + "=" * 60)
        return full_response

    except requests.exceptions.RequestException as e:
        print(f"Error connecting to Ollama: {e}")
        return None

if __name__ == "__main__":
    # Example usage
    print("Ollama C++ Code Generator via Cloudflare Tunnel")
    print("=" * 60)

    # Get cloudflare URL from user
    cloudflare_url = input("Enter your cloudflared public domain URL: ").strip()

    if not cloudflare_url:
        print("Error: URL is required")
        exit(1)

    # Add https:// if not present
    if not cloudflare_url.startswith(('http://', 'https://')):
        cloudflare_url = f"https://{cloudflare_url}"

    print("\nChoose mode:")
    print("1. Non-streaming (wait for complete response)")
    print("2. Streaming (real-time response)")

    mode = input("Enter choice (1 or 2): ").strip()

    # Custom prompt or use default
    custom_prompt = input("\nEnter custom prompt (or press Enter for default): ").strip()
    if not custom_prompt:
        custom_prompt = "Generate a simple C++ program that displays one line of output to the screen. Include necessary headers and a main function."

    print("\n")

    # Generate code based on mode
    if mode == "2":
        result = generate_cpp_code_streaming(cloudflare_url, custom_prompt)
    else:
        result = generate_cpp_code(cloudflare_url, custom_prompt)

    if result:
        print("\n✓ Code generation completed successfully!")
    else:
        print("\n✗ Code generation failed.")
