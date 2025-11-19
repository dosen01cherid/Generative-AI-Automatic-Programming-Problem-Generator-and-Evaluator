# RAG (Retrieval-Augmented Generation) System

## Overview

The RAG system intelligently retrieves only the most relevant examples from the context.txt file based on each question, rather than loading the entire 252KB file every time.

## How It Works

### 1. Context Parsing (`ContextParser`)
- Parses `context.txt` into 250+ individual examples
- Extracts instructions section separately
- Each example is indexed with:
  - **ID**: Example identifier (S1, A1, B1, etc.)
  - **Description**: What the example teaches
  - **Keywords**: Extracted C++ concepts and terms
  - **Full text**: Complete example content

### 2. Keyword Extraction
Automatically extracts relevant C++ keywords from each example:
- **Language keywords**: int, for, while, class, struct, etc.
- **Standard library**: vector, map, string, iostream, etc.
- **Concepts**: loop, pointer, array, function, etc.
- **Operations**: push_back, size, insert, sort, etc.

### 3. Retrieval (`RAGRetriever`)
Uses keyword-based similarity matching:
1. Extracts keywords from user question
2. Calculates relevance score for each example using **Jaccard similarity**
3. Ranks examples by relevance
4. Returns top-K most relevant examples

**Relevance Score Formula:**
```
matches = query_keywords ∩ example_keywords
total = query_keywords ∪ example_keywords
jaccard = matches / total
score = jaccard × (1 + matches × 0.1)  # Boost for more matches
```

### 4. Dynamic Context Building
1. Always includes instruction section (how to create questions)
2. Adds top-K retrieved examples
3. Stops when reaching max token limit (30,000 tokens)
4. Typical context size: **4,000-8,000 tokens** (vs. 60,000+ for full file)

### 5. Response Generation
Sends optimized context to Ollama LLM for question generation.

## Benefits

### 🚀 Efficiency
- **85-95% smaller context** compared to loading full file
- Faster processing and lower latency
- Reduced token usage and cost

### 🎯 Relevance
- Only includes examples related to the question
- Better focused responses
- Higher quality output

### 🔄 Freshness
- Each question gets fresh, relevant examples
- No stale or irrelevant examples
- Adapts to different question types

### 📊 Scalability
- Can handle unlimited examples in context.txt
- Performance remains constant regardless of file size
- Easy to add more examples without degrading performance

## Usage

### Basic Usage
```bash
python genai_ollama_client_with_rag.py "Create a for loop example"
```

### Specify Number of Examples
```bash
python genai_ollama_client_with_rag.py "How to use vectors" --examples 30
```

### Quiet Mode (Only Output)
```bash
python genai_ollama_client_with_rag.py "Create class example" --quiet
```

### Custom Context File
```bash
python genai_ollama_client_with_rag.py "Question here" --context my_context.txt
```

## Example Output

```
============================================================
🧠 Ollama RAG Client
============================================================

🔍 Parsing context file...
📚 Parsed 251 examples from context file
✅ RAG system initialized with 251 examples

============================================================
🔎 Question: Create a simple for loop example
============================================================

📚 Retrieved 10 relevant examples in 0.00s:
   1. S15 - for Keyword
   2. A1 - For Loop - Initialization
   3. A2 - For Loop - Condition
   4. A3 - For Loop - Increment
   5. A4 - For Loop - Body
   ... and 5 more

📊 Context size: ~4,122 tokens

🚀 Generating response...
[AI-generated response here]

⏱️  Response time: 15.2s
📈 Retrieval time: 0.00s
🔢 Total examples in context: 10

============================================================
✅ Response generated successfully
============================================================

📝 Examples used: S15, A1, A2, A3, A4, A5, B10, C15, D20, D21
```

## Configuration

Edit the following constants in `genai_ollama_client_with_rag.py`:

```python
# RAG Configuration
MAX_EXAMPLES_TO_RETRIEVE = 20  # Number of examples to retrieve
MAX_CONTEXT_TOKENS = 30_000    # Maximum tokens for context
```

## Comparison: RAG vs. Full Context

| Metric | Full Context | RAG System |
|--------|-------------|------------|
| **Context Size** | ~60,000 tokens | ~4,000-8,000 tokens |
| **File Read** | Full 252KB | Full 252KB (once, at startup) |
| **Processing** | All 250 examples | Top 10-20 relevant examples |
| **Retrieval Time** | N/A | < 0.01s |
| **Relevance** | Mixed (all examples) | High (filtered examples) |
| **Scalability** | Poor (linear with file size) | Excellent (constant time) |
| **Memory Usage** | High | Low |

## Implementation Details

### Classes

1. **ContextParser**
   - Parses context.txt file
   - Extracts examples and instructions
   - Builds keyword index

2. **RAGRetriever**
   - Implements keyword-based retrieval
   - Calculates relevance scores
   - Returns ranked examples

3. **OllamaRAGClient**
   - Main client interface
   - Coordinates retrieval and generation
   - Manages Ollama API calls

### Keyword Matching Patterns

Automatic detection for common patterns:
- `"for loop"` → keywords: for, loop, iteration
- `"vector"` → keywords: vector, push_back, size
- `"class"` → keywords: class, object, oop
- `"file"` → keywords: file, fstream, ifstream, ofstream
- `"pointer"` → keywords: pointer, new, delete
- And many more...

## Future Enhancements

Potential improvements:
1. **TF-IDF weighting** for better keyword importance
2. **Semantic embeddings** using sentence transformers
3. **Query expansion** to include synonyms
4. **Caching** of retrieved contexts for repeated questions
5. **Hybrid retrieval** combining keyword and semantic search
6. **User feedback** to improve retrieval quality

## Performance Tips

1. **Increase examples** for complex questions:
   ```bash
   --examples 30
   ```

2. **Adjust max tokens** for longer contexts:
   Edit `MAX_CONTEXT_TOKENS` in the code

3. **Use specific keywords** in questions for better retrieval

4. **Question phrasing** affects retrieval:
   - Good: "Create a for loop with fill-in-the-blank"
   - Better: "Create a for loop fill-in-the-blank question testing the increment operator"

## Troubleshooting

### No relevant examples retrieved
- Make sure question contains C++ keywords
- Try rephrasing the question
- Increase `--examples` parameter

### Context too large
- Reduce `MAX_EXAMPLES_TO_RETRIEVE`
- Reduce `MAX_CONTEXT_TOKENS`

### Poor quality responses
- Increase number of examples retrieved
- Check if relevant examples exist in context.txt
- Try more specific questions

## License

Part of the Generative AI Automatic Programming Problem Generator and Evaluator project.
