# RAG Infrastructure: Specification Variations for C++ Curriculum
## Two-Phase Question Generation System

This document contains explicit specification variations for each C++ topic across four difficulty levels. These variations are used in the two-phase LLM generation approach:

**Phase 1:** Select specification variation based on student's difficulty level
**Phase 2:** Generate C++ code from the selected specification

---

## Level 1: BASICS

### Topic 1.1: Hello World

#### BEGINNER Variations:
1. **Print 'Hello World' to console**
   - Focus: Basic output
   - Min score: 2/3
   - Example targets: `cout`, `endl`, `return`

2. **Display a welcome message using cout**
   - Focus: Output stream
   - Min score: 2/3
   - Example targets: `cout`, `<<`, `string`

#### INTERMEDIATE Variations:
3. **Print your name and age on separate lines**
   - Focus: Multiple outputs
   - Min score: 2/3
   - Example targets: `cout`, `endl`, `int`

4. **Output a formatted greeting with newlines**
   - Focus: Output formatting
   - Min score: 2/3
   - Example targets: `cout`, `endl`, `<<`

#### ADVANCED Variations:
5. **Create a program that prints a formatted greeting with your name, age, and university**
   - Focus: Complex formatting
   - Min score: 3/3
   - Example targets: `cout`, `endl`, `string`

6. **Display a multi-line banner with personal information**
   - Focus: Advanced formatting
   - Min score: 3/3
   - Example targets: `cout`, `endl`, `<<`

#### EXPERT Variations:
7. **Build a formatted ASCII art banner with embedded personal data**
   - Focus: Complex multi-line output
   - Min score: 3/3
   - Example targets: `cout`, `endl`, `string`

---

### Topic 1.2: Integer Variables

#### BEGINNER Variations:
1. **Declare an integer variable and assign it a value**
   - Focus: Variable declaration
   - Min score: 2/3
   - Example targets: `int`, `=`, `main`

2. **Create a variable to store someone's age and display it**
   - Focus: Variable with output
   - Min score: 2/3
   - Example targets: `int`, `cout`, `age`

#### INTERMEDIATE Variations:
3. **Declare two integer variables, assign values, and print both**
   - Focus: Multiple variables
   - Min score: 2/3
   - Example targets: `int`, `cout`, `endl`

4. **Create variables for height and weight, then calculate BMI concept**
   - Focus: Variable operations
   - Min score: 2/3
   - Example targets: `int`, `float`, `cout`

#### ADVANCED Variations:
5. **Declare variables for student ID, age, and year, then display them with labels**
   - Focus: Multiple variables with formatting
   - Min score: 3/3
   - Example targets: `int`, `cout`, `endl`

6. **Create a simple student record with 5 integer fields and formatted output**
   - Focus: Complex variable management
   - Min score: 3/3
   - Example targets: `int`, `cout`, `string`

#### EXPERT Variations:
7. **Create a program with multiple integer variables representing student data (ID, scores, etc.) with formatted table output**
   - Focus: Advanced data organization
   - Min score: 3/3
   - Example targets: `int`, `cout`, `endl`

---

## Level 3: LOOPS

### Topic 3.1: For Loops

#### BEGINNER Variations:
1. **Create a for loop that counts from 0 to 5**
   - Focus: Basic loop syntax
   - Min score: 2/3
   - Example targets: `for`, `int`, `cout`
   - Key concepts: initialization, condition, increment

2. **Write a loop that prints numbers 1 through 10**
   - Focus: Loop iteration
   - Min score: 2/3
   - Example targets: `for`, `i`, `cout`
   - Key concepts: counter variable, boundary

#### INTERMEDIATE Variations:
3. **Create a for loop that prints even numbers from 0 to 20**
   - Focus: Loop with step
   - Min score: 2/3
   - Example targets: `for`, `+=`, `cout`
   - Key concepts: increment by 2

4. **Write a loop that calculates the sum of numbers 1 to N**
   - Focus: Accumulator pattern
   - Min score: 2/3
   - Example targets: `for`, `int`, `sum`
   - Key concepts: accumulation, variable

5. **Create a loop that prints odd numbers in reverse from 99 to 1**
   - Focus: Decrement loop
   - Min score: 2/3
   - Example targets: `for`, `--`, `cout`
   - Key concepts: reverse iteration

#### ADVANCED Variations:
6. **Create a for loop that prints a multiplication table for a given number**
   - Focus: Loop with calculation
   - Min score: 3/3
   - Example targets: `for`, `int`, `*`
   - Key concepts: multiplication, formatting

7. **Write a loop that counts backwards from 100 to 0 by steps of 5**
   - Focus: Decrement with step
   - Min score: 3/3
   - Example targets: `for`, `-=`, `cout`
   - Key concepts: decrement, step size

8. **Create a loop to calculate factorial of a number**
   - Focus: Accumulative multiplication
   - Min score: 3/3
   - Example targets: `for`, `*=`, `int`
   - Key concepts: factorial, product

#### EXPERT Variations:
9. **Create nested for loops to print a pyramid pattern of stars**
   - Focus: Nested loops
   - Min score: 3/3
   - Example targets: `for`, `int`, `cout`
   - Key concepts: outer loop, inner loop, pattern

10. **Write nested loops to generate a multiplication table grid (1-10)**
    - Focus: Complex nested iteration
    - Min score: 3/3
    - Example targets: `for`, `int`, `*`
    - Key concepts: 2D iteration, formatting

---

### Topic 3.2: While Loops

#### BEGINNER Variations:
1. **Create a while loop that counts from 1 to 5**
   - Focus: Basic while syntax
   - Min score: 2/3
   - Example targets: `while`, `int`, `++`
   - Key concepts: condition, increment

2. **Write a countdown loop from 10 to 0**
   - Focus: Decrement while
   - Min score: 2/3
   - Example targets: `while`, `--`, `cout`
   - Key concepts: countdown, condition

#### INTERMEDIATE Variations:
3. **Create a while loop that doubles a number until it exceeds 100**
   - Focus: Conditional growth
   - Min score: 2/3
   - Example targets: `while`, `*=`, `int`
   - Key concepts: exponential growth

4. **Write a loop that sums numbers entered by user until they enter 0**
   - Focus: User-controlled loop
   - Min score: 2/3
   - Example targets: `while`, `cin`, `sum`
   - Key concepts: sentinel value

#### ADVANCED Variations:
5. **Write a while loop that finds the first power of 2 greater than 1000**
   - Focus: Search pattern
   - Min score: 3/3
   - Example targets: `while`, `*=`, `int`
   - Key concepts: search, condition

6. **Create a loop that calculates digits in a number**
   - Focus: Digit processing
   - Min score: 3/3
   - Example targets: `while`, `/=`, `count`
   - Key concepts: division, counting

#### EXPERT Variations:
7. **Create a while loop that implements a number guessing game with attempts limit**
   - Focus: Interactive loop with conditions
   - Min score: 3/3
   - Example targets: `while`, `cin`, `if`
   - Key concepts: game logic, attempts

8. **Implement a loop that validates user input with retry limit**
   - Focus: Input validation
   - Min score: 3/3
   - Example targets: `while`, `cin`, `bool`
   - Key concepts: validation, retry logic

---

## Level 7: VECTORS

### Topic 7.1: Vector Basics

#### BEGINNER Variations:
1. **Create a vector and add three numbers using push_back**
   - Focus: Basic vector operations
   - Min score: 2/3
   - Example targets: `vector`, `push_back`, `int`
   - Key concepts: initialization, insertion

2. **Declare a vector of integers and display its size**
   - Focus: Vector size function
   - Min score: 2/3
   - Example targets: `vector`, `size`, `cout`
   - Key concepts: container size

#### INTERMEDIATE Variations:
3. **Create a vector, add 5 elements, then print the first and last elements**
   - Focus: Vector access patterns
   - Min score: 2/3
   - Example targets: `vector`, `[]`, `push_back`
   - Key concepts: indexing, access

4. **Initialize a vector with values and check if it's empty**
   - Focus: Vector initialization and empty check
   - Min score: 2/3
   - Example targets: `vector`, `empty`, `if`
   - Key concepts: initialization list, empty

5. **Create a vector and iterate through it with a for loop**
   - Focus: Vector iteration
   - Min score: 2/3
   - Example targets: `vector`, `for`, `size`
   - Key concepts: iteration, bounds

#### ADVANCED Variations:
6. **Create a vector of student scores, add values, calculate average, and display**
   - Focus: Vector with calculations
   - Min score: 3/3
   - Example targets: `vector`, `push_back`, `float`
   - Key concepts: accumulation, average

7. **Build a vector, sort it, and find the maximum element**
   - Focus: Vector algorithms
   - Min score: 3/3
   - Example targets: `vector`, `sort`, `max`
   - Key concepts: sorting, finding max

#### EXPERT Variations:
8. **Implement a vector-based dynamic array that grows, shrinks, and reports capacity vs size**
   - Focus: Advanced vector management
   - Min score: 3/3
   - Example targets: `vector`, `capacity`, `resize`
   - Key concepts: capacity, size, memory

9. **Create a vector of vectors (2D matrix) for storing grades**
   - Focus: Nested vectors
   - Min score: 3/3
   - Example targets: `vector`, `push_back`, `[]`
   - Key concepts: 2D structure, nesting

---

## How to Use This Document

### For 14b Model:
The 14b model receives the specification directly and generates code with targets/distractors in one phase.

```
Prompt:
"Create a C++ fill-in-the-blank question for this specification:
'{variation.specification}'

Topic: {topic.name}
Difficulty: {variation.difficulty.name}
..."
```

### For 1.5b Model:
The 1.5b model only generates code from specification. Deterministic processing handles targets/distractors.

```
Prompt:
"Write a simple, complete C++ code example for this task:
{variation.specification}

Topic: {topic.name}
Difficulty: {variation.difficulty.name}
..."
```

Then apply deterministic extraction:
1. Extract all C++ keywords from generated code
2. Score and select best targets (control > types > container...)
3. Map targets to pre-defined distractors
4. Create question with numbered blanks

---

## Difficulty Progression Rules

1. **BEGINNER (Level 1)**
   - Simple, direct specifications
   - Focus on one concept at a time
   - Short, straightforward code
   - Min score: 2/3 to unlock INTERMEDIATE

2. **INTERMEDIATE (Level 2)**
   - Multiple concepts combined
   - Slightly longer code
   - Simple calculations or operations
   - Min score: 2/3 to unlock ADVANCED

3. **ADVANCED (Level 3)**
   - Complex specifications
   - Multiple operations or calculations
   - Formatted output requirements
   - Min score: 3/3 to unlock EXPERT

4. **EXPERT (Level 4)**
   - Challenging specifications
   - Nested structures or complex logic
   - Multiple concepts integrated
   - Min score: 3/3 (mastery level)

---

## Example: Complete Two-Phase Generation Flow

### Scenario: Student working on "For Loops" at INTERMEDIATE level

**Phase 1: Select Specification**
```python
topic = "For Loops (L3_01)"
difficulty = INTERMEDIATE
variation = random.choice([
    "Create a for loop that prints even numbers from 0 to 20",
    "Write a loop that calculates the sum of numbers 1 to N",
    "Create a loop that prints odd numbers in reverse from 99 to 1"
])
# Selected: "Write a loop that calculates the sum of numbers 1 to N"
```

**Phase 2: Generate Code (14b or 1.5b)**
```cpp
#include <iostream>
using namespace std;

int main() {
    int N = 10;
    int sum = 0;

    for (int i = 1; i <= N; i++) {
        sum += i;
    }

    cout << "Sum: " << sum << endl;
    return 0;
}
```

**Phase 3: Process Question (Deterministic for 1.5b)**
- Targets: `for`, `int`, `sum` (selected by scoring)
- Distractors:
  - `for` → [`while`, `do`, `if`]
  - `int` → [`float`, `double`, `char`]
  - `sum` → [`total`, `result`, `count`]

**Result:**
```cpp
#include <iostream>
using namespace std;

int main() {
    _____(1)_____ N = 10;
    _____(2)_____ sum = 0;

    _____(3)_____ (int i = 1; i <= N; i++) {
        sum += i;
    }

    cout << "Sum: " << sum << endl;
    return 0;
}

Blank 1: [int, float, double, char]
Blank 2: [sum, total, result, count]
Blank 3: [for, while, do, if]
```

---

## Statistics

**Total Topics:** 6 topics across 3 levels
**Total Variations:** 50+ specification variations
**Difficulty Distribution:**
- BEGINNER: 12 variations (direct, simple)
- INTERMEDIATE: 20 variations (combined concepts)
- ADVANCED: 12 variations (complex operations)
- EXPERT: 6 variations (mastery challenges)

**Key Benefits:**
1. ✨ **Variety:** Students see different problem formulations for same concept
2. 📈 **Progression:** Gradual increase in difficulty within each topic
3. 🎯 **Clarity:** Explicit specifications guide LLM generation
4. 🔓 **Motivation:** Unlock system encourages completion
5. 🏆 **Challenge:** Expert level provides mastery goals
6. 💾 **Tracking:** Progress saved across sessions

---

## Adding New Topics

To add a new topic with variations:

1. Define the topic in `curriculum_with_variations.py`:
```python
TopicWithVariations(
    id="L5_01",
    name="Your Topic Name",
    description="Brief description",
    base_difficulty=3,  # 1-5 stars
    prerequisites=["L3_01"],  # Previous topics
    variations=[...]
)
```

2. Add specification variations for each difficulty level:
```python
SpecificationVariation(
    difficulty=DifficultyLevel.BEGINNER,
    specification="Simple, direct task description",
    description="What this variation teaches",
    min_score=2  # Minimum to pass
)
```

3. Add to this RAG document with:
   - Clear specification text
   - Example target keywords
   - Key concepts covered
   - Difficulty-appropriate complexity

4. Test with both 14b and 1.5b models to ensure quality generation

---

## Prompt Engineering Tips

### For Better Code Generation:

**DO:**
- Use clear, specific task descriptions
- Include difficulty level in prompt
- Specify modern C++ (C++11+)
- Ask for complete, working code
- Request necessary headers

**DON'T:**
- Use vague specifications like "write a program"
- Mix multiple unrelated concepts in BEGINNER level
- Ask for overly complex code at lower levels
- Forget to specify input/output requirements

### Example Good Specifications:

✅ **BEGINNER:** "Create a for loop that counts from 0 to 5"
- Clear start and end
- One concept (for loop)
- Simple output

✅ **INTERMEDIATE:** "Write a loop that calculates the sum of numbers 1 to N"
- Combines loop + accumulation
- Clear goal (sum)
- Variable N adds complexity

✅ **EXPERT:** "Create nested for loops to print a pyramid pattern of stars"
- Multiple concepts (nested loops, pattern)
- Requires logic (pyramid shape)
- Complex output formatting

### Example Poor Specifications:

❌ **Too vague:** "Write a program about numbers"
❌ **Too complex for BEGINNER:** "Create a recursive function with memoization"
❌ **Mixing concepts:** "Use a for loop to read strings and sort them in a vector"

---

## Future Enhancements

Potential additions to this system:

1. **Hint System:** Progressive hints for students who struggle
2. **Explanation Mode:** Auto-generated explanations for wrong answers
3. **Code Review:** LLM provides feedback on student's own code
4. **Adaptive Difficulty:** Automatically adjust based on student performance
5. **Peer Comparison:** Show how student ranks vs others
6. **Time Tracking:** Record time spent per difficulty level
7. **Custom Topics:** Allow instructors to add their own variations
8. **Language Support:** Extend to Java, Python, etc.

---

Last Updated: 2025-11-19
Version: 1.0
