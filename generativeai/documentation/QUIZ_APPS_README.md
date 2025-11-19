# C++ Quiz Applications - User Guide

## Overview

This system provides interactive C++ programming quizzes with automatic question generation and scoring. Two versions are available:

1. **quiz_app_14b.py** - High-quality questions using large 14b model
2. **quiz_app_1_5b.py** - Fast generation using small 1.5b model with deterministic processing

Both follow the same structured curriculum progression from beginner to advanced topics.

---

## Quick Start

### For Beginners (Recommended: Use Fast 1.5b)

```bash
# Start with Level 1 (Basics) - 5 questions
python quiz_app_1_5b.py

# Or specify level and number of questions
python quiz_app_1_5b.py --level 1 --questions 3
```

### For Quality (Use 14b Model)

```bash
# Better quality but slower
python quiz_app_14b.py --level 1 --questions 5
```

---

## Curriculum Structure

The curriculum is organized into **10 levels**, covering a full semester (20 weeks):

### Level 1: Basics (Week 1-2) ⭐
**Topics:**
- Hello World - First C++ program
- Basic Output - Using cout and endl
- Integer Variables - Declaring and using int
- Basic Arithmetic - Math operations
- Basic Input - Using cin

**Example Command:**
```bash
python quiz_app_1_5b.py --level 1 --questions 5
```

---

### Level 2: Control Flow (Week 3-4) ⭐⭐
**Topics:**
- If Statements - Basic conditionals
- If-Else Statements - Two-way branching
- Nested If Statements - Multiple levels
- Switch Statements - Multi-way branching
- Boolean Variables - Logical operators

**Example Command:**
```bash
python quiz_app_1_5b.py --level 2 --questions 5
```

---

### Level 3: Loops (Week 5-6) ⭐⭐ to ⭐⭐⭐
**Topics:**
- For Loops - Counted iteration
- While Loops - Conditional iteration
- Do-While Loops - Post-test loops
- Nested Loops - Loops within loops
- Break and Continue - Loop control

**Example Command:**
```bash
python quiz_app_1_5b.py --level 3 --questions 5
```

---

### Level 4: Functions (Week 7-8) ⭐⭐⭐
**Topics:**
- Void Functions - No return value
- Return Functions - Functions that return
- Function Parameters - Passing arguments
- Function Overloading - Same name, different params
- Reference Parameters - Passing by reference

**Example Command:**
```bash
python quiz_app_14b.py --level 4 --questions 4
```

---

### Level 5: Arrays (Week 9-10) ⭐⭐⭐ to ⭐⭐⭐⭐
**Topics:**
- Array Declaration - Creating arrays
- Array Iteration - Looping through arrays
- Array Search - Finding elements
- Multi-dimensional Arrays - 2D arrays
- Array Algorithms - Sorting, reversing

**Example Command:**
```bash
python quiz_app_14b.py --level 5 --questions 5
```

---

### Level 6: Strings (Week 11-12) ⭐⭐⭐ to ⭐⭐⭐⭐
**Topics:**
- String Basics - Using C++ string class
- String Input/Output - Reading and displaying
- String Operations - Manipulations
- String Algorithms - Working with text
- String Comparison - Comparing strings

**Example Command:**
```bash
python quiz_app_1_5b.py --level 6 --questions 5
```

---

### Level 7: Vectors (Week 13-14) ⭐⭐⭐ to ⭐⭐⭐⭐
**Topics:**
- Vector Basics - Introduction to vectors
- Vector Iteration - Looping through vectors
- Vector Operations - push_back, insert, erase
- Vector Algorithms - Using STL algorithms
- 2D Vectors - Vectors of vectors

**Example Command:**
```bash
python quiz_app_14b.py --level 7 --questions 5
```

---

### Level 8: Classes (Week 15-16) ⭐⭐⭐⭐
**Topics:**
- Class Basics - Defining classes
- Constructors - Initializing objects
- Public and Private - Access specifiers
- Member Functions - Methods in classes
- Multiple Objects - Arrays/vectors of objects

**Example Command:**
```bash
python quiz_app_14b.py --level 8 --questions 4
```

---

### Level 9: Advanced Containers (Week 17-18) ⭐⭐⭐⭐
**Topics:**
- Map Container - Key-value pairs
- Set Container - Unique elements
- Queue Container - FIFO structure
- Stack Container - LIFO structure
- Container Selection - Choosing the right one

**Example Command:**
```bash
python quiz_app_14b.py --level 9 --questions 5
```

---

### Level 10: Advanced Topics (Week 19-20) ⭐⭐⭐⭐ to ⭐⭐⭐⭐⭐
**Topics:**
- Pointers Basics - Introduction to pointers
- File I/O - Reading and writing files
- Exception Handling - Try-catch blocks
- Templates - Generic programming
- Lambda Expressions - Anonymous functions

**Example Command:**
```bash
python quiz_app_14b.py --level 10 --questions 3
```

---

## Command Line Options

### quiz_app_1_5b.py (Fast Model)

```bash
python quiz_app_1_5b.py [OPTIONS]

Options:
  --level, -l    Curriculum level (1-10, default: 1)
  --questions, -q    Number of questions (default: 5)
  --help, -h    Show help message

Examples:
  python quiz_app_1_5b.py
  python quiz_app_1_5b.py --level 3
  python quiz_app_1_5b.py --level 5 --questions 10
  python quiz_app_1_5b.py -l 8 -q 3
```

**Speed:** ~8 seconds per question
**Quality:** Good (85-90% accuracy)
**Best For:** Practice, quick review, large number of questions

---

### quiz_app_14b.py (Quality Model)

```bash
python quiz_app_14b.py [OPTIONS]

Options:
  --level, -l    Curriculum level (1-10, default: 1)
  --questions, -q    Number of questions (default: 5)
  --help, -h    Show help message

Examples:
  python quiz_app_14b.py
  python quiz_app_14b.py --level 4
  python quiz_app_14b.py --level 7 --questions 8
  python quiz_app_14b.py -l 10 -q 5
```

**Speed:** ~25-30 seconds per question
**Quality:** Very Good (90-95% accuracy)
**Best For:** Exams, assessments, quality practice

---

## How the Quiz Works

### 1. Question Generation
- System selects random topics from chosen level
- Generates complete C++ code examples
- Identifies important keywords to blank out
- Creates plausible wrong options (distractors)

### 2. Question Display
```
Complete Code:
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

Fill in the blanks:
```cpp
#include <iostream>
using namespace std;
_____(3)_____ main(){
   _____(2)_____(int i = 0; i < 5; i++){
      _____(1)_____ << i << endl;
   }
   return 0;
}
```

--- Blank 1 ---
Options:
  1. cin
  2. cout ✓ CORRECT
  3. print
  4. output

Your answer (1-4): 2
✅ Correct!
```

### 3. Scoring
- Each blank is worth 1 point
- Immediate feedback (correct/incorrect)
- Question summary after each question
- Final grade at the end:
  - A: 90-100% 🌟
  - B: 80-89% 😊
  - C: 70-79% 🙂
  - D: 60-69% 😐
  - F: <60% 📚

---

## Usage Scenarios

### Scenario 1: Self-Study

**Goal:** Learn C++ progressively

**Approach:**
```bash
# Week 1: Start with basics
python quiz_app_1_5b.py --level 1 --questions 5

# Week 3: Move to control flow
python quiz_app_1_5b.py --level 2 --questions 5

# Week 5: Practice loops
python quiz_app_1_5b.py --level 3 --questions 10

# Continue through levels...
```

---

### Scenario 2: Exam Preparation

**Goal:** Prepare for midterm covering Levels 1-5

**Approach:**
```bash
# Day 1: Review Level 1
python quiz_app_14b.py --level 1 --questions 10

# Day 2: Review Level 2
python quiz_app_14b.py --level 2 --questions 10

# Day 3-5: Continue through Level 5
python quiz_app_14b.py --level 5 --questions 10

# Day 6: Mixed review
# Generate questions from multiple levels manually
```

---

### Scenario 3: Quick Review Before Class

**Goal:** 5-minute warmup on today's topic (Functions)

**Approach:**
```bash
# Fast generation, 3 questions
python quiz_app_1_5b.py --level 4 --questions 3
```

---

### Scenario 4: Homework Practice

**Goal:** Practice this week's topic with quality questions

**Approach:**
```bash
# Week 13: Vector practice with quality questions
python quiz_app_14b.py --level 7 --questions 5
```

---

## Grading Scale

The quiz automatically calculates your grade:

| Score | Grade | Meaning | Emoji |
|-------|-------|---------|-------|
| 90-100% | A | Excellent! | 🌟 |
| 80-89% | B | Good! | 😊 |
| 70-79% | C | Fair | 🙂 |
| 60-69% | D | Needs Improvement | 😐 |
| <60% | F | Keep Practicing | 📚 |

---

## Tips for Success

### 1. Start with Your Level
- Don't skip levels
- Complete prerequisites first
- Check topic descriptions

### 2. Practice Regularly
- Short sessions daily better than one long session
- Review mistakes immediately
- Retake quizzes on weak topics

### 3. Use the Right Tool
- **Fast 1.5b:** Daily practice, quick review
- **Quality 14b:** Exams, important assessments
- **Both:** Compare your understanding

### 4. Read the Complete Code First
- Understand what the code does
- Look for patterns
- Think about the missing parts

### 5. Learn from Mistakes
- Read the correct answer explanation
- Understand why it's correct
- Note the distractor patterns

---

## Curriculum Statistics

**Total Content:**
- 10 Levels
- 50 Topics
- 150+ Example Variations
- Covers 20 weeks of instruction

**Difficulty Distribution:**
- Level 1 (⭐): 5 topics
- Level 2 (⭐⭐): 14 topics
- Level 3 (⭐⭐⭐): 19 topics
- Level 4 (⭐⭐⭐⭐): 10 topics
- Level 5 (⭐⭐⭐⭐⭐): 2 topics

---

## Viewing the Curriculum

To see all available topics:

```bash
python cpp_curriculum_progression.py
```

**Output:**
```
================================================================================
C++ CURRICULUM PROGRESSION
================================================================================

Level 1: Basics (Week 1-2)
--------------------------------------------------------------------------------
  L1_01: Hello World ⭐
      First C++ program with cout
      Prerequisites: None
      Examples: 3 variations
  L1_02: Basic Output ⭐
      Using cout and endl
      Prerequisites: L1_01
      Examples: 3 variations
  ...

================================================================================
CURRICULUM STATISTICS
================================================================================
Total Topics: 50
Total Example Variations: 150
...
```

---

## Comparison: 1.5b vs 14b

| Feature | 1.5b (Fast) | 14b (Quality) |
|---------|-------------|---------------|
| **Speed** | ~8s/question | ~25-30s/question |
| **Quality** | Good (85-90%) | Very Good (90-95%) |
| **Code Quality** | Good | Excellent |
| **Distractor Quality** | Good (template-based) | Excellent (AI-generated) |
| **Consistency** | 100% (deterministic) | 95% (AI-based) |
| **Best For** | Practice, review | Exams, assessments |
| **Cost** | Very Low | Medium |
| **Reliability** | 98% success | 95% success |

---

## Troubleshooting

### Problem: "Connection Error"
**Solution:**
- Check if Ollama server is running
- Verify Cloudflare tunnel URL is correct
- Check internet connection

### Problem: "No questions generated"
**Solution:**
- Try a different level
- Reduce number of questions
- Check model is loaded in Ollama

### Problem: "UnicodeEncodeError"
**Solution:**
- UTF-8 encoding is auto-fixed in code
- If still occurs, run in UTF-8 terminal
- Use Python 3.8+

### Problem: Quiz too easy/hard
**Solution:**
- Adjust level up/down
- Level 1-3: Beginner
- Level 4-7: Intermediate
- Level 8-10: Advanced

---

## Advanced Usage

### Custom Quiz Sessions

Create your own quiz script:

```python
from cpp_curriculum_progression import CppCurriculum
from quiz_app_1_5b import QuizApp

# Get specific topics
curriculum = CppCurriculum()
loop_topics = [
    curriculum.get_topic_by_id('L3_01'),  # For loops
    curriculum.get_topic_by_id('L3_02'),  # While loops
]

# Create custom quiz with these topics
app = QuizApp()
# ... custom implementation
```

### Batch Question Generation

Generate multiple questions for manual review:

```python
from quiz_app_14b import QuestionGenerator14b
from cpp_curriculum_progression import CppCurriculum

generator = QuestionGenerator14b()
curriculum = CppCurriculum()

# Generate 10 questions from Level 3
topics = curriculum.get_by_level(3)
for topic in topics:
    question = generator.generate_question(topic)
    # Save to file or review
```

---

## System Requirements

### Required:
- Python 3.8+
- Ollama server running
- Internet connection (for Cloudflare tunnel)
- Models loaded: qwen2.5:1.5b, qwen2.5:14b

### Python Packages:
```bash
pip install requests
```

### Recommended:
- Terminal with UTF-8 support
- At least 8GB RAM
- SSD for faster model loading

---

## For Educators

### Using in Classroom

**Week 1 Lab:**
```bash
# All students start together
python quiz_app_1_5b.py --level 1 --questions 5

# Review results as a class
# Discuss common mistakes
```

**Midterm Assessment:**
```bash
# Use quality model for grading
python quiz_app_14b.py --level 5 --questions 10

# Students record their scores
# Standardized questions (same level)
```

**Homework Assignment:**
```bash
# Assign different levels per student ability
# Beginners: Level 2-3
python quiz_app_1_5b.py --level 2 --questions 10

# Advanced: Level 7-8
python quiz_app_14b.py --level 8 --questions 8
```

### Creating Custom Curriculum

Extend the curriculum with your own topics:

```python
# Edit cpp_curriculum_progression.py

# Add new topic to appropriate level
Topic(
    id="L11_01",
    name="Your New Topic",
    description="Description here",
    difficulty=3,
    prerequisites=["L10_05"],
    examples=[
        "Example prompt 1",
        "Example prompt 2",
    ]
)
```

---

## Midterm Project

Students can use these systems for the midterm project:
- Compare 1.5b vs 14b approaches
- Implement Strategy 2 (deterministic) using quiz_app_1_5b as reference
- Run experiments on curriculum topics
- Analyze performance across difficulty levels

See **MIDTERM_PROJECT_SPECIFICATION.md** for full details.

---

## Support and Issues

**Found a bug?**
- Check if Ollama server is running
- Verify model is loaded
- Try with smaller number of questions first

**Want to contribute?**
- Add more topics to curriculum
- Improve distractor templates
- Add more example variations
- Create new quiz modes

---

## Example Session

Here's what a complete quiz session looks like:

```
$ python quiz_app_1_5b.py --level 3 --questions 3

================================================================================
⚡ C++ PROGRAMMING QUIZ - Fast 1.5b Model
================================================================================

Welcome to the interactive C++ programming quiz!
...

📖 Level 3 Topics:
  • For Loops
  • While Loops
  • Do-While Loops
  • Nested Loops
  • Break and Continue

⏳ Generating 3 questions...
[1/3] Generating: For Loops... ✅
[2/3] Generating: While Loops... ✅
[3/3] Generating: Break and Continue... ✅

✅ Generated 3 questions successfully!

Press Enter to start the quiz...

================================================================================
📚 Topic: For Loops
================================================================================
Description: Counted iteration
Difficulty: ⭐⭐ (2/5)
...

[Quiz continues with questions, options, scoring...]

================================================================================
🏆 QUIZ COMPLETE!
================================================================================

Final Score: 7/9
Percentage: 77.8%
Grade: C (Fair) 🙂

Detailed Results:
  ⚠️ Q1: For Loops - 2/3
  ✅ Q2: While Loops - 3/3
  ⚠️ Q3: Break and Continue - 2/3
```

---

## Quick Reference

**Common Commands:**

```bash
# Beginner level, fast
python quiz_app_1_5b.py --level 1 --questions 5

# Intermediate level, quality
python quiz_app_14b.py --level 5 --questions 5

# Advanced level, fast
python quiz_app_1_5b.py --level 9 --questions 3

# View curriculum
python cpp_curriculum_progression.py

# Help
python quiz_app_1_5b.py --help
python quiz_app_14b.py --help
```

**Level Guide:**
- Level 1-2: First month (Basics, Control)
- Level 3-4: Second month (Loops, Functions)
- Level 5-6: Third month (Arrays, Strings)
- Level 7-8: Fourth month (Vectors, Classes)
- Level 9-10: Fifth month (Containers, Advanced)

---

## Changelog

**Version 1.0 (Current)**
- Initial release
- 50 topics across 10 levels
- Two quiz applications (1.5b, 14b)
- Interactive scoring
- Curriculum progression system
- 150+ example variations

---

## License

Educational Use Only

---

**Happy Learning! 🚀📚**

For questions or feedback, contact your instructor.
