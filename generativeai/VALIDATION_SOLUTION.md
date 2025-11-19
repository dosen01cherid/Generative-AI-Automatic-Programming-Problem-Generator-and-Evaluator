# Solution: Validated Question Generation

## Problem

The original RAG client had consistency issues:

❌ **Issues:**
1. Model manually creates blank version (error-prone)
2. Replaced part doesn't match correct answer
3. Answer position may be wrong
4. No validation of output consistency

**Example of Error:**
```
Code with blank: cout << v._____ << endl;
Options: 1. length  2. capacity  3. size  4. totalSize
Answer: 2  ← Should be "capacity"
But actual code had: cout << v.size() << endl;  ← Inconsistent!
```

## Solution: Two-Stage Validated Approach

### Architecture

```
┌─────────────────────────────────────────────────────┐
│  Stage 1: Model Generation (Structured Output)     │
│  ───────────────────────────────────────────────    │
│  Model outputs:                                     │
│  - CODE: Complete working C++ code                  │
│  - TARGET: Exact token to replace                   │
│  - DISTRACTORS: 3 wrong options                     │
└─────────────────────────────────────────────────────┘
                         ↓
┌─────────────────────────────────────────────────────┐
│  Stage 2: Deterministic Question Creation           │
│  ───────────────────────────────────────────────    │
│  System:                                            │
│  1. Validates TARGET exists in CODE                 │
│  2. Replaces TARGET with _____ (deterministic)      │
│  3. Creates options: [correct] + distractors        │
│  4. Shuffles and assigns answer position            │
│  5. Guarantees consistency                          │
└─────────────────────────────────────────────────────┘
```

### Implementation Details

#### 1. Structured Prompt Format

Forces model to output in parseable format:

```
CODE:
```cpp
#include <iostream>
#include <vector>
using namespace std;
int main(){
   vector<int> v = {1, 2, 3};
   cout << v.capacity() << endl;
   return 0;
}
```

TARGET:
capacity

DISTRACTORS:
1. length
2. size
3. totalSize
```

#### 2. QuestionValidator Class

**Key Methods:**

- `parse_model_output()`: Extracts CODE, TARGET, DISTRACTORS from model response
- `create_validated_question()`: Deterministically creates question with guaranteed consistency

**Validation Steps:**

```python
1. Verify TARGET exists in CODE
   - If not found: try case-insensitive match
   - If still not found: return error

2. Count occurrences of TARGET
   - If 0: return error
   - If >1: warn and replace first occurrence

3. Create question_code
   - Replace TARGET with "_____" deterministically
   - Guaranteed to match correct answer

4. Build options
   - Correct answer: TARGET (from code)
   - Distractors: from model output
   - Shuffle randomly
   - Record correct position

5. Return validated question
   - code: original working code
   - question_code: code with blank
   - options: shuffled list
   - answer: correct position (1-indexed)
   - target: what was replaced
```

### Benefits

✅ **Guaranteed Consistency**
- Blank always matches correct answer
- Answer position is always accurate
- No manual errors

✅ **Validation**
- Checks target exists in code
- Warns about multiple occurrences
- Handles edge cases

✅ **Deterministic**
- Same input → same output (except shuffle)
- Reproducible results
- No randomness in replacement

✅ **Transparent**
- Shows what was replaced
- Displays validation steps
- Clear error messages

## Usage

### Basic Usage

```bash
python genai_ollama_client_with_rag_validated.py "Create a vector example"
```

### With Options

```bash
# More examples
python genai_ollama_client_with_rag_validated.py "Create for loop" --examples 30

# Quiet mode
python genai_ollama_client_with_rag_validated.py "Create class" --quiet
```

## Example Output

```
============================================================
✅ FINAL VALIDATED QUESTION
============================================================

Complete Code:
```cpp
#include <iostream>
#include <vector>
using namespace std;
int main(){
   vector<int> v = {1, 2, 3};
   cout << v.capacity() << endl;
   return 0;
}
```

Question Code:
```cpp
#include <iostream>
#include <vector>
using namespace std;
int main(){
   vector<int> v = {1, 2, 3};
   cout << v._____() << endl;
   return 0;
}
```

Options:
1. size
2. length
3. capacity ✓ CORRECT
4. totalSize

Answer: 3

Target replaced: 'capacity'
============================================================
```

## Comparison: Original vs Validated

| Aspect | Original RAG | Validated RAG |
|--------|-------------|---------------|
| **Consistency** | ❌ Manual, error-prone | ✅ Guaranteed by system |
| **Answer accuracy** | ❌ Can mismatch | ✅ Always correct |
| **Validation** | ❌ None | ✅ Full validation |
| **Error handling** | ❌ Silent failures | ✅ Clear error messages |
| **Deterministic** | ❌ Random errors | ✅ Reproducible |
| **Response format** | Unstructured | Structured (CODE/TARGET/DISTRACTORS) |
| **Question creation** | By model | By system (deterministic) |

## Technical Details

### Parser Logic

```python
# 1. Extract CODE section
code_match = re.search(r'CODE:\s*```(?:cpp)?\s*(.*?)\s*```', output, re.DOTALL)

# 2. Extract TARGET
target_match = re.search(r'TARGET:\s*([^\n]+)', output)

# 3. Extract DISTRACTORS
for line in distractor_text.split('\n'):
    match = re.match(r'\d+\.\s*(.+)', line.strip())
    if match:
        distractors.append(match.group(1).strip())
```

### Replacement Logic

```python
# Find target in code (exact match)
if target not in code:
    # Try case-insensitive
    pattern = re.compile(re.escape(target), re.IGNORECASE)
    match = pattern.search(code)
    if match:
        target = match.group(0)  # Use actual case from code

# Replace deterministically
question_code = code.replace(target, "_____", 1)  # First occurrence only

# Create options with correct answer
options = [target] + distractors[:3]
# Shuffle and track answer position
```

## Error Handling

The validated client handles:

1. **Target not found in code**
   ```
   ❌ Target 'capacity' not found in code at all!
   ```

2. **Multiple occurrences**
   ```
   ⚠️  Warning: 'int' appears 5 times - replacing first occurrence
   ```

3. **Insufficient distractors**
   ```
   ❌ Failed to parse: need at least 3 distractors
   ```

4. **Unparseable output**
   ```
   ❌ Failed to parse model output
   ```

## Recommendations

### For Production Use

1. **Use validated client** for all question generation
2. **Log all failures** for analysis
3. **Monitor validation pass rate**
4. **Collect feedback** on question quality

### For Development

1. **Test with various question types**
2. **Check edge cases** (multi-word targets, special characters)
3. **Validate all outputs** before storing
4. **Keep examples** of failures for improvement

## Future Enhancements

Possible improvements:

1. **Multiple blank support**: Handle questions with multiple blanks
2. **Context-aware distractors**: Better wrong answer generation
3. **Difficulty scoring**: Classify questions by difficulty
4. **Auto-retry**: Regenerate if validation fails
5. **Batch processing**: Generate multiple questions at once
6. **Quality metrics**: Score question quality automatically

## Conclusion

The **validated approach** solves the consistency problem by:

1. ✅ Separating generation from question creation
2. ✅ Using deterministic replacement
3. ✅ Validating all outputs
4. ✅ Providing clear error messages
5. ✅ Guaranteeing answer accuracy

**Result**: 100% consistent, validated fill-in-the-blank questions! 🎉
