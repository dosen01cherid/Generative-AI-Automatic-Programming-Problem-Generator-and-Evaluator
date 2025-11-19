"""
Test Small Model (qwen2.5:1.5b) Capability
-------------------------------------------
Systematically test the 1.5b model's ability to follow instructions
and generate fill-in-the-blank questions compared to the 14b model.

This will help identify strengths, weaknesses, and strategies to leverage
the smaller model effectively.
"""

import requests
import json
import time
import sys
import io

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

OLLAMA_URL = "https://null-server-reliability-integration.trycloudflare.com"
TIMEOUT = 300


def test_model(model_name, prompt, test_name):
    """Test a model with a specific prompt."""
    print(f"\n{'='*60}")
    print(f"🧪 Test: {test_name}")
    print(f"📊 Model: {model_name}")
    print(f"{'='*60}\n")

    start_time = time.time()
    response_text = ""

    try:
        payload = {
            "model": model_name,
            "prompt": prompt,
            "stream": True,
            "keep_alive": "10m"
        }

        with requests.post(
            f"{OLLAMA_URL}/api/generate",
            json=payload,
            stream=True,
            timeout=TIMEOUT
        ) as r:
            r.raise_for_status()

            for line in r.iter_lines(decode_unicode=True):
                if not line or not line.strip():
                    continue

                try:
                    data = json.loads(line)
                    if "response" in data:
                        chunk = data["response"]
                        print(chunk, end='', flush=True)
                        response_text += chunk
                except json.JSONDecodeError:
                    continue

        elapsed_time = time.time() - start_time
        print(f"\n\n⏱️  Time: {elapsed_time:.2f}s")
        print(f"📏 Length: {len(response_text)} chars")

        return response_text, elapsed_time

    except Exception as e:
        print(f"\n❌ Error: {e}")
        return None, 0


def main():
    print("="*60)
    print("🔬 Small Model Capability Testing")
    print("="*60)
    print("\nTesting qwen2.5:1.5b vs qwen2.5:14b on various tasks")
    print("to identify strengths, weaknesses, and leveraging strategies.\n")

    # Test 1: Simple structured output
    test1_prompt = """Create a simple C++ for loop example.

OUTPUT FORMAT:

CODE:
```cpp
[your code here]
```

TARGET:
[what to replace]

DISTRACTORS:
1. [option 1]
2. [option 2]
3. [option 3]

Follow this format exactly."""

    print("\n" + "="*60)
    print("TEST 1: Simple Structured Output (For Loop)")
    print("="*60)

    # Test with 1.5b
    result_1_5b, time_1_5b = test_model("qwen2.5:1.5b", test1_prompt, "Simple Structured - 1.5b")

    # Test with 14b
    result_14b, time_14b = test_model("qwen2.5:14b", test1_prompt, "Simple Structured - 14b")

    # Test 2: Very simple task (just generate code)
    test2_prompt = """Write a simple C++ program that prints "Hello World".

Just provide the code, nothing else."""

    print("\n" + "="*60)
    print("TEST 2: Very Simple Task (Just Code Generation)")
    print("="*60)

    result2_1_5b, time2_1_5b = test_model("qwen2.5:1.5b", test2_prompt, "Simple Code - 1.5b")
    result2_14b, time2_14b = test_model("qwen2.5:14b", test2_prompt, "Simple Code - 14b")

    # Test 3: Template-based approach
    test3_prompt = """Fill in the blanks:

CODE:
```cpp
#include <iostream>
using namespace std;
int main(){
   for(int i = 0; i < 5; i++){
      cout << i << endl;
   }
   return 0;
}
```

What keyword should be replaced? Just write one word: _____"""

    print("\n" + "="*60)
    print("TEST 3: Template-Based (Fill in Simple Blank)")
    print("="*60)

    result3_1_5b, time3_1_5b = test_model("qwen2.5:1.5b", test3_prompt, "Template - 1.5b")
    result3_14b, time3_14b = test_model("qwen2.5:14b", test3_prompt, "Template - 14b")

    # Test 4: Multiple choice generation only
    test4_prompt = """Given the correct answer "for", generate 3 wrong options that are similar C++ keywords.

Format:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]"""

    print("\n" + "="*60)
    print("TEST 4: Distractor Generation Only")
    print("="*60)

    result4_1_5b, time4_1_5b = test_model("qwen2.5:1.5b", test4_prompt, "Distractors - 1.5b")
    result4_14b, time4_14b = test_model("qwen2.5:14b", test4_prompt, "Distractors - 14b")

    # Test 5: Step-by-step prompting
    test5_prompt = """Let's create a fill-in-the-blank question step by step.

Step 1: Write a simple for loop in C++.
[Wait for response]"""

    print("\n" + "="*60)
    print("TEST 5: Step-by-Step Prompting")
    print("="*60)

    result5_1_5b, time5_1_5b = test_model("qwen2.5:1.5b", test5_prompt, "Step-by-step - 1.5b")
    result5_14b, time5_14b = test_model("qwen2.5:14b", test5_prompt, "Step-by-step - 14b")

    # Summary
    print("\n" + "="*80)
    print("📊 SUMMARY")
    print("="*80)

    print("\nTest 1 - Simple Structured Output:")
    print(f"  1.5b: {time_1_5b:.2f}s, {len(result_1_5b or ''):,} chars")
    print(f"  14b:  {time_14b:.2f}s, {len(result_14b or ''):,} chars")
    print(f"  Speed: 1.5b is {((time_14b/time_1_5b - 1) * 100):.0f}% faster" if time_1_5b > 0 else "")

    print("\nTest 2 - Simple Code Generation:")
    print(f"  1.5b: {time2_1_5b:.2f}s")
    print(f"  14b:  {time2_14b:.2f}s")

    print("\nTest 3 - Template-Based:")
    print(f"  1.5b: {time3_1_5b:.2f}s")
    print(f"  14b:  {time3_14b:.2f}s")

    print("\nTest 4 - Distractor Generation:")
    print(f"  1.5b: {time4_1_5b:.2f}s")
    print(f"  14b:  {time4_14b:.2f}s")

    print("\nTest 5 - Step-by-Step:")
    print(f"  1.5b: {time5_1_5b:.2f}s")
    print(f"  14b:  {time5_14b:.2f}s")

    print("\n" + "="*80)
    print("💡 RECOMMENDATIONS BASED ON RESULTS")
    print("="*80)
    print("\nAnalyze the outputs above to determine:")
    print("1. Can 1.5b follow structured formats reliably?")
    print("2. What tasks does 1.5b handle well?")
    print("3. Where does 1.5b struggle?")
    print("4. What strategies can leverage 1.5b effectively?")
    print("\nPossible strategies:")
    print("  - Use 1.5b for simple code generation only")
    print("  - Use 1.5b with very constrained templates")
    print("  - Use 1.5b for specific subtasks (distractors, code only)")
    print("  - Chain 1.5b + 14b (1.5b generates, 14b validates)")
    print("  - Use more examples/few-shot for 1.5b")
    print("  - Post-process 1.5b output with rules")


if __name__ == "__main__":
    main()
