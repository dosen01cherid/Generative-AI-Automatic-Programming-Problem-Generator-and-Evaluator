# Qwen2.5-Coder Model Downloader

This script provides multiple methods to download Qwen2.5-Coder models for various use cases.

## Quick Start

### List Available Models
```bash
python download_qwen_coder.py --list
```

### Download via Ollama (Recommended for Local Inference)
```bash
# Download 1.5B model (fast, good quality)
python download_qwen_coder.py --method ollama --model 1.5b

# Download 7B model (higher quality)
python download_qwen_coder.py --method ollama --model 7b
```

### Download via Hugging Face
```bash
# Download with transformers library
python download_qwen_coder.py --method huggingface --model 1.5b

# Download to specific directory
python download_qwen_coder.py --method hub --model 1.5b --output ./models
```

## Prerequisites

### For Ollama Method
1. Install Ollama from https://ollama.com
2. No Python dependencies required

### For Hugging Face Methods
```bash
# For transformers method
pip install transformers torch accelerate

# For hub method
pip install huggingface_hub
```

## Available Models

| Size | Model ID | Disk Space | Use Case |
|------|----------|------------|----------|
| 0.5B | Qwen/Qwen2.5-Coder-0.5B-Instruct | ~1-2 GB | Browser-based LLM, fastest |
| 1.5B | Qwen/Qwen2.5-Coder-1.5B-Instruct | ~3-4 GB | **Recommended** for most uses |
| 3B | Qwen/Qwen2.5-Coder-3B-Instruct | ~6-8 GB | Balanced speed/quality |
| 7B | Qwen/Qwen2.5-Coder-7B-Instruct | ~14-16 GB | High quality code generation |
| 14B | Qwen/Qwen2.5-Coder-14B-Instruct | ~28-32 GB | Excellent quality |
| 32B | Qwen/Qwen2.5-Coder-32B-Instruct | ~64-72 GB | Best quality (requires GPU) |

## Usage Examples

### 1. Browser-Based LLM Integration
For running in browser (see Q3_Journal_Paper.md Section 6.4):
```bash
# Download smallest model for WebGPU
python download_qwen_coder.py --method hub --model 0.5b --output ./browser_models
```

Then convert to ONNX/WebGPU format using MLC-AI tools.

### 2. Local Python Development
```bash
# Download via Hugging Face transformers
python download_qwen_coder.py --method huggingface --model 1.5b

# Test the model
python -c "
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained('Qwen/Qwen2.5-Coder-1.5B-Instruct')
tokenizer = AutoTokenizer.from_pretrained('Qwen/Qwen2.5-Coder-1.5B-Instruct')

prompt = 'Write a Python function to check if a number is prime'
inputs = tokenizer(prompt, return_tensors='pt')
outputs = model.generate(**inputs, max_length=200)
print(tokenizer.decode(outputs[0]))
"
```

### 3. Ollama API Server
```bash
# Download via Ollama
python download_qwen_coder.py --method ollama --model 1.5b

# Run Ollama server
ollama serve

# Test via API
curl http://localhost:11434/api/generate -d '{
  "model": "qwen2.5-coder:1.5b",
  "prompt": "Write a hello world in Python"
}'
```

## Download Methods Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **Ollama** | Easy to use, includes API server, optimized | Requires Ollama installation | Local inference, API usage |
| **Hugging Face Transformers** | Direct Python integration, flexible | Requires PyTorch, larger size | Python development, fine-tuning |
| **Hugging Face Hub** | Raw model files, portable | Manual setup required | Custom deployment, browser conversion |

## Model Recommendations

### For Browser-Based LLM (Q3 Paper Section 6.4)
- **Best:** 0.5B or 1.5B models
- **Why:** WebGPU memory constraints, faster download, good for code completion
- **Format:** Convert to ONNX or use MLC-AI for WebGPU

### For Quiz App Question Generation
- **Best:** 1.5B model
- **Why:** Fast generation (8s/question), good quality, runs on consumer hardware
- **Method:** Ollama (easy API integration)

### For Production/Research
- **Best:** 7B or 14B models
- **Why:** Highest quality code generation
- **Method:** Hugging Face Transformers (flexible deployment)

## Troubleshooting

### Ollama: "command not found"
```bash
# Install Ollama first
# Windows: Download from https://ollama.com
# Linux: curl -fsSL https://ollama.com/install.sh | sh
# macOS: brew install ollama
```

### Hugging Face: "No module named 'transformers'"
```bash
pip install transformers torch accelerate
```

### Out of Memory Error
- Try a smaller model (0.5B or 1.5B)
- For transformers: Use `device_map="auto"` and `load_in_8bit=True`
```python
model = AutoModelForCausalLM.from_pretrained(
    "Qwen/Qwen2.5-Coder-1.5B-Instruct",
    device_map="auto",
    load_in_8bit=True  # Requires bitsandbytes library
)
```

### Slow Download
- Use `--resume` flag (hub method automatically resumes)
- Download during off-peak hours
- Consider using a download manager

## Integration with Existing Projects

### With Quiz Apps (generativeai/quiz_apps/)
```python
# In quiz_app_1_5b_variations.py
# Update OLLAMA_URL if running locally:
OLLAMA_URL = "http://localhost:11434"

# Or keep using Cloudflare tunnel for remote access
```

### With RAG System (genai_ollama_client_with_rag_validated.py)
```python
# Model is automatically detected if using Ollama
# Just ensure model name matches:
MODEL_NAME = "qwen2.5-coder:1.5b"
```

### With Browser-Based Problem Generator (Section 6.4)
See Q3_Journal_Paper.md Section 6.4 for complete integration guide.

## Performance Benchmarks

Based on typical hardware:

| Model | CPU (Intel i7) | GPU (RTX 3060) | Memory |
|-------|----------------|----------------|--------|
| 0.5B  | ~2-3s/token    | ~0.5s/token    | 2 GB   |
| 1.5B  | ~5-8s/token    | ~1s/token      | 4 GB   |
| 7B    | ~20-30s/token  | ~3s/token      | 16 GB  |
| 14B   | N/A (too slow) | ~6s/token      | 32 GB  |

*Token = ~0.75 words on average*

## Additional Resources

- **Qwen2.5-Coder Documentation:** https://github.com/QwenLM/Qwen2.5-Coder
- **Ollama Documentation:** https://ollama.com/library/qwen2.5-coder
- **Hugging Face Models:** https://huggingface.co/Qwen
- **MLC-AI (Browser LLM):** https://github.com/mlc-ai/web-llm

## License

Qwen2.5-Coder models are released under Apache 2.0 license.
Check individual model cards on Hugging Face for specific terms.

---

**Related Documentation:**
- Q3_Journal_Paper.md - Section 6.4: Browser-based LLM integration
- generativeai/README.md - Quiz app system overview
- generativeai/RAG_SYSTEM_README.md - RAG infrastructure
