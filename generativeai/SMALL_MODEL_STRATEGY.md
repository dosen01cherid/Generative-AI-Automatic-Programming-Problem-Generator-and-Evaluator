# Strategy: Leveraging Small Model (qwen2.5:1.5b)

## Problem Statement

Small models like **qwen2.5:1.5b** have:
- ❌ **Weaker instruction-following** (harder to follow complex structured formats)
- ❌ **Less context understanding** (may miss nuances)
- ❌ **Lower accuracy** on complex tasks
- ✅ **Much faster** (85% faster than 14b model)
- ✅ **Lower cost** (resource efficient)
- ✅ **Good for simple tasks**

## Observed Performance (from question8_comparison.md)

| Metric | qwen2.5:1.5b | qwen2.5:14b | Winner |
|--------|--------------|-------------|--------|
| **Pre-load time** | 4.26s | 12.47s | 🏆 1.5b (70% faster) |
| **Response time** | 8.57s | 70.70s | 🏆 1.5b (88% faster) |
| **Total time** | 12.83s | 83.17s | 🏆 1.5b (85% faster) |
| **Response quality** | Good (simple) | Excellent (detailed) | 🏆 14b |
| **Format compliance** | ~60-70% | ~95% | 🏆 14b |

## Key Findings

### What 1.5b Does Well:
✅ Simple code generation
✅ Basic keyword identification
✅ Short, concise outputs
✅ Speed (85% faster!)

### What 1.5b Struggles With:
❌ Complex structured formats (CODE/TARGET/DISTRACTORS)
❌ Multi-step reasoning
❌ Consistent format adherence
❌ Detailed explanations

## Recommended Strategies

### Strategy 1: **Hybrid Pipeline** (Recommended)

Use 1.5b for speed, 14b for accuracy:

```
┌──────────────────────────────────┐
│  Phase 1: Fast Generation (1.5b) │
│  ──────────────────────────────   │
│  - Generate code quickly          │
│  - Identify potential targets     │
│  - Create initial drafts          │
│  Time: ~10s                       │
└──────────────────────────────────┘
              ↓
┌──────────────────────────────────┐
│  Phase 2: Validation (14b)        │
│  ──────────────────────────────   │
│  - Validate format                │
│  - Enhance quality                │
│  - Ensure correctness             │
│  Time: +15s                       │
└──────────────────────────────────┘
```

**Implementation:**
```python
# 1. Use 1.5b to generate code quickly
code = generate_with_1_5b("Create for loop")  # ~10s

# 2. Use 14b to extract targets and distractors
validated = validate_with_14b(code)  # +15s

# Total: 25s vs 70s for 14b alone
# Savings: 64% time saved!
```

### Strategy 2: **Template-Based Approach**

Force 1.5b into rigid templates:

**Bad (1.5b fails):**
```
Create a fill-in-the-blank question with CODE, TARGET, and DISTRACTORS.
```

**Good (1.5b succeeds):**
```
Complete this template:

CODE:
```cpp
[YOUR CODE HERE - just write code, nothing else]
```

What keyword from the code above should be replaced? One word only:
TARGET: _____

3 wrong keywords similar to TARGET:
1. _____
2. _____
3. _____
```

**Key Principles:**
- ✅ One task at a time
- ✅ Very explicit instructions
- ✅ Clear boundaries (```, ---, etc.)
- ✅ Minimal formatting required

### Strategy 3: **Task Decomposition**

Break complex tasks into simple steps:

**Instead of:** Generate complete structured question (fails)

**Do:** Three separate calls to 1.5b:

**Call 1: Generate Code Only**
```
Prompt: "Write a simple C++ for loop. Just code, nothing else."
Output: [code block]
Time: ~3s
```

**Call 2: Identify Target**
```
Prompt: "From this code: [code], what keyword is most important? One word:"
Output: for
Time: ~2s
```

**Call 3: Generate Distractors**
```
Prompt: "Given correct answer 'for', give 3 wrong C++ keywords:
1.
2.
3."
Output: while, do, if
Time: ~3s
```

**Total: ~8s vs 70s for 14b**
**Benefit: 88% faster, good enough for simple questions**

### Strategy 4: **Few-Shot Prompting**

Give 1.5b explicit examples in prompt:

```python
prompt = """
Example 1:
CODE: int main()
TARGET: int
DISTRACTORS: void, char, float

Example 2:
CODE: cout << "Hello"
TARGET: cout
DISTRACTORS: cin, print, output

Example 3:
CODE: for(int i = 0; i < 5; i++)
TARGET: for
DISTRACTORS: while, do, if

Now you try:
CODE: vector<int> v
TARGET: _____
DISTRACTORS: _____, _____, _____
"""
```

**Key:** Provide 3-5 examples in exact format expected.

### Strategy 5: **Constrained Generation**

Limit what 1.5b can generate:

```python
# Instead of free-form, use JSON schema-like constraints

prompt = """Generate ONLY what's asked, nothing more:

TASK 1: Write code
[Write C++ for loop here]

TASK 2: One word to replace
[Write one word]

TASK 3: Three wrong words
[Write word 1]
[Write word 2]
[Write word 3]

STOP. Do not write anything else."""
```

### Strategy 6: **Post-Processing Pipeline**

Let 1.5b be messy, clean it up:

```python
def use_small_model_with_cleanup(question):
    # 1. Let 1.5b generate (fast, possibly messy)
    raw_output = generate_with_1_5b(question)  # 10s

    # 2. Parse with regex/rules (deterministic)
    code = extract_code_block(raw_output)
    target = extract_first_cpp_keyword(raw_output)
    distractors = extract_list_items(raw_output)

    # 3. Validate and fix
    if not valid(target):
        target = fallback_target_from_code(code)

    if len(distractors) < 3:
        distractors = generate_generic_distractors(target)

    # 4. Create validated question
    return create_validated_question(code, target, distractors)
```

### Strategy 7: **Caching + Small Model**

Use cached examples + 1.5b for speed:

```python
# Pre-compute common patterns with 14b (offline)
cache = {
    'for_loop': {
        'code': 'for(int i=0; i<5; i++) {...}',
        'targets': ['for', 'int', 'i++'],
        'distractors': {...}
    },
    'vector': {...},
    'class': {...}
}

# At runtime, use 1.5b to adapt cached pattern
def generate_fast(question_type):
    template = cache[question_type]  # Instant!

    # Use 1.5b only to customize/adapt
    customized = adapt_with_1_5b(template, specifics)  # 5s

    return customized

# Total: 5s vs 70s!
```

## Recommended Implementation

### Option A: **Hybrid System** (Best Quality)

```python
class HybridQuestionGenerator:
    def __init__(self):
        self.fast_model = "qwen2.5:1.5b"
        self.quality_model = "qwen2.5:14b"

    def generate_question(self, prompt, quality_mode='auto'):
        if quality_mode == 'fast':
            # Use 1.5b only (10s, acceptable quality)
            return self.generate_with_small_model(prompt)

        elif quality_mode == 'quality':
            # Use 14b only (70s, best quality)
            return self.generate_with_large_model(prompt)

        elif quality_mode == 'auto':
            # Hybrid: 1.5b generates, 14b validates (25s, good quality)
            draft = self.generate_with_small_model(prompt)  # 10s
            validated = self.validate_with_large_model(draft)  # +15s
            return validated

    def generate_with_small_model(self, prompt):
        # Use Strategy 3 (Task Decomposition)
        code = self.generate_code_with_1_5b(prompt)  # 3s
        target = self.identify_target_with_1_5b(code)  # 2s
        distractors = self.generate_distractors_with_1_5b(target)  # 3s

        return {
            'code': code,
            'target': target,
            'distractors': distractors
        }
```

### Option B: **Template System** (Fastest, Acceptable Quality)

```python
class TemplateBasedGenerator:
    """
    Use 1.5b with rigid templates for simple questions.
    Best for: Simple questions, high volume, low complexity.
    """

    def generate(self, concept):
        # Get pre-defined template
        template = self.get_template(concept)

        # Simple prompt for 1.5b
        prompt = f"Complete this code: {template['code_stub']}"

        # 1.5b generates code (fast)
        code = call_1_5b(prompt)  # 3s

        # Deterministic extraction (no AI needed)
        target = template['target_pattern'].extract(code)
        distractors = template['distractors']

        return create_question(code, target, distractors)

    # Templates for common patterns
    templates = {
        'for_loop': {
            'code_stub': 'for loop from 0 to 5',
            'target_pattern': r'for|int|i\+\+',
            'distractors': ['while', 'do', 'if']
        },
        'vector': {
            'code_stub': 'vector with push_back',
            'target_pattern': r'vector|push_back',
            'distractors': ['array', 'insert', 'add']
        }
    }
```

### Option C: **Batch Processing** (Maximum Efficiency)

```python
class BatchProcessor:
    """
    Generate multiple questions in parallel using 1.5b.
    Trade individual quality for overall throughput.
    """

    def generate_batch(self, questions_list):
        # Generate all with 1.5b in parallel (fast)
        drafts = [
            self.generate_with_1_5b(q)  # 10s each, but parallel
            for q in questions_list
        ]
        # Total: 10s for all (vs 10s * N sequentially)

        # Validate batch with 14b (slower, but amortized)
        validated = self.validate_batch_with_14b(drafts)  # +20s total

        # Total: 30s for 10 questions
        # vs 70s * 10 = 700s with 14b alone
        # Savings: 95%!

        return validated
```

## Performance Comparison

| Approach | Time | Quality | Use Case |
|----------|------|---------|----------|
| **14b alone** | 70s | Excellent | Best quality needed |
| **1.5b alone** | 10s | Acceptable | Speed critical, simple questions |
| **Hybrid (1.5b + 14b)** | 25s | Very Good | Balanced (recommended) |
| **Template (1.5b)** | 5s | Good | High volume, simple patterns |
| **Batch (1.5b)** | 3s/question | Good | Multiple questions at once |

## Recommendations by Use Case

### For Production (Best Balance):
✅ **Use Hybrid System (Option A)**
- Time: 25s per question (64% faster than 14b)
- Quality: Very good (validated by 14b)
- Reliability: High

### For Development/Testing:
✅ **Use 1.5b Template System (Option B)**
- Time: 5s per question (93% faster)
- Quality: Good enough for iteration
- Reliability: Medium (needs error handling)

### For Bulk Generation:
✅ **Use Batch Processing (Option C)**
- Time: 3s per question (amortized)
- Quality: Good (batch validated)
- Reliability: High (quality check at end)

## Implementation Priority

### Phase 1: Quick Win (1 week)
1. Implement Template System (Option B)
2. Create templates for top 10 question types
3. Test with 1.5b model
4. Measure speed improvements

### Phase 2: Quality Enhancement (2 weeks)
1. Implement Hybrid System (Option A)
2. Use 1.5b for draft, 14b for validation
3. A/B test quality vs speed
4. Optimize pipeline

### Phase 3: Scale (1 month)
1. Implement Batch Processing (Option C)
2. Handle 100+ questions efficiently
3. Add caching layer
4. Monitor quality metrics

## Code Example: Hybrid System

```python
# hybrid_question_generator.py

class HybridGenerator:
    def __init__(self):
        self.models = {
            'fast': "qwen2.5:1.5b",
            'quality': "qwen2.5:14b"
        }

    def generate_question(self, topic, mode='hybrid'):
        if mode == 'hybrid':
            return self._hybrid_generate(topic)
        elif mode == 'fast':
            return self._fast_generate(topic)
        else:
            return self._quality_generate(topic)

    def _hybrid_generate(self, topic):
        # Step 1: Fast draft with 1.5b (10s)
        draft = self._generate_with_model(
            model=self.models['fast'],
            prompt=self._create_simple_prompt(topic),
            mode='draft'
        )

        # Step 2: Quality check with 14b (15s)
        validated = self._validate_with_model(
            model=self.models['quality'],
            draft=draft,
            mode='validate'
        )

        return validated

    def _create_simple_prompt(self, topic):
        # Simple, concrete prompt for 1.5b
        return f"""Write a simple C++ code example for: {topic}

Code only, no explanations:"""

    def _generate_with_model(self, model, prompt, mode):
        # Call Ollama API
        response = call_ollama(model, prompt)

        if mode == 'draft':
            # Extract just the code
            return extract_code_block(response)

        return response

    def _validate_with_model(self, model, draft, mode):
        # Let 14b extract targets and distractors
        prompt = f"""Given this code:
```cpp
{draft}
```

Extract in this format:
TARGET: [one keyword]
DISTRACTORS: [keyword1, keyword2, keyword3]"""

        response = call_ollama(model, prompt)

        # Parse and create validated question
        return parse_and_validate(draft, response)

# Usage
generator = HybridGenerator()

# Fast mode (10s)
q1 = generator.generate_question("for loop", mode='fast')

# Hybrid mode (25s, recommended)
q2 = generator.generate_question("vector operations", mode='hybrid')

# Quality mode (70s)
q3 = generator.generate_question("class definition", mode='quality')
```

## Conclusion

**Best Strategy for qwen2.5:1.5b:**

1. ✅ **Use Hybrid System** (1.5b + 14b) - Recommended
   - 64% faster than 14b alone
   - Maintains good quality
   - Production-ready

2. ✅ **Use Template System** for simple questions
   - 93% faster
   - Good enough for common patterns
   - Development/testing

3. ✅ **Use Batch Processing** for bulk generation
   - Maximum throughput
   - Quality validation at end
   - Scalable

**Key Insight:** Don't try to force 1.5b to do complex structured output. Instead, use it for what it's good at (fast code generation), and let 14b handle validation/structuring.

**Expected Results:**
- Speed: 3-25s per question (vs 70s with 14b alone)
- Quality: Good to Very Good (validated)
- Reliability: High (14b validates 1.5b output)
- Cost: Lower (less 14b usage)

🚀 **Start with Hybrid System, measure results, optimize from there!**
