# Specification Variations System
## Progressive Difficulty with Two-Phase LLM Generation

This document explains the enhanced quiz system with specification variations, difficulty progression, and student progress tracking.

---

## 🎯 What's New?

### Previous System:
- ❌ Single specification per topic
- ❌ No progression within topics
- ❌ Linear difficulty (topic to topic only)
- ❌ No challenge/mastery mode

### New System:
- ✅ **4-7 specification variations** per topic
- ✅ **4 difficulty levels** per topic (BEGINNER → INTERMEDIATE → ADVANCED → EXPERT)
- ✅ **2D progression** (within topics + between topics)
- ✅ **Progressive unlocking** - complete easier levels to unlock harder ones
- ✅ **Challenge mode** - return to topics for mastery
- ✅ **Progress tracking** - scores saved between sessions

---

## 🚀 Quick Start

### Running the Enhanced Quiz Apps

**Option 1: Fast 1.5b Model (Recommended for Practice)**
```bash
cd generativeai
python quiz_app_1_5b_variations.py
```
- ⚡ ~8 seconds per question
- 🎯 Same progression system as 14b
- 💰 Lower cost
- 📚 Best for: Practice, homework, self-study

**Option 2: Quality 14b Model (Recommended for Assessments)**
```bash
cd generativeai
python quiz_app_14b_variations.py
```
- 🎓 ~25-30 seconds per question
- ✨ Highest quality
- 💎 Best for: Exams, formal assessments

Both apps share the same features:
- Interactive topic selection menu
- Difficulty progression display
- Automatic progress saving
- Return to topics for challenges
- Detailed progress reports

---

## 📚 How It Works

### The Three Phases

#### Phase 1: Select Specification Variation
```python
# System selects specification based on student's current difficulty level
topic = "For Loops"
difficulty = INTERMEDIATE  # Student's current level

variations = [
    "Create a for loop that prints even numbers from 0 to 20",
    "Write a loop that calculates the sum of numbers 1 to N",
    "Create a loop that prints odd numbers in reverse from 99 to 1"
]

selected = random.choice(variations)
# Result: "Write a loop that calculates the sum of numbers 1 to N"
```

#### Phase 2: Generate Code from Specification
```python
# LLM generates C++ code based on the selected specification
prompt = f"""Write C++ code for: {selected}

Topic: For Loops
Difficulty: INTERMEDIATE
"""

code = llm.generate(prompt)
```

**Example Output:**
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

#### Phase 3: Extract Targets & Distractors

**For 1.5b (Deterministic):**
```python
# Rule-based extraction
tokens = extract_all_tokens(code)
# Found: for, int, sum, cout, endl, return, ...

targets = select_best_targets(tokens, num=3)
# Selected: for, int, sum (highest priority)

distractors = {
    'for': ['while', 'do', 'if'],
    'int': ['float', 'double', 'char'],
    'sum': ['total', 'result', 'count']
}
```

**For 14b (LLM):**
```python
# LLM selects targets and generates distractors in one go
# Still uses specification from Phase 1
```

---

## 🎮 User Experience Flow

### 1. Start the Quiz
```bash
python quiz_app_1_5b_variations.py
```

### 2. Topic Selection Menu
```
================================================================================
📚 SELECT TOPIC
================================================================================
  1. Hello World ⭐ [2/4 difficulties]
  2. Integer Variables ⭐ [1/4 difficulties]
  3. For Loops ⭐⭐ [0/4 difficulties]
  4. While Loops ⭐⭐ 🔒 (Complete previous topic's BEGINNER level)
  5. Vector Basics ⭐⭐⭐ 🔒 (Complete previous topic's BEGINNER level)

  6. View Progress
  0. Exit
================================================================================

Select topic (0 to exit): 3
```

### 3. Difficulty Selection Menu
```
================================================================================
📊 DIFFICULTY LEVELS - For Loops
================================================================================
  1. BEGINNER (2 variations) - 📝 Not attempted
  2. INTERMEDIATE (3 variations) - 🔒 (Complete previous difficulty first)
  3. ADVANCED (2 variations) - 🔒 (Complete previous difficulty first)
  4. EXPERT (2 variations) - 🔒 (Complete previous difficulty first)

  0. Back to topic selection
================================================================================

Select difficulty (0 to go back): 1
```

### 4. Question Display
```
================================================================================
📚 Topic: For Loops
================================================================================
Description: Counted iteration
Base Difficulty: ⭐⭐ (2/5)

🎯 Challenge Level: BEGINNER
Specification: Create a for loop that counts from 0 to 5
Minimum score to pass: 2/3
================================================================================

⏳ Generating question...
Fast generation with 1.5b model...
✅ Question generated!

Press Enter to start...
```

### 5. Fill-in-the-Blank Question
```
================================================================================
FILL-IN-THE-BLANK QUESTION
================================================================================

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
int main(){
   _____(1)_____(int i = 0; i < 5; i++){
      _____(2)_____ << i << endl;
   }
   _____(3)_____ 0;
}
```

--- Blank 1 ---
Options:
  1. for
  2. while
  3. do
  4. if

Your answer (1-4): 1
✅ Correct!

--- Blank 2 ---
Options:
  1. cin
  2. print
  3. cout
  4. output

Your answer (1-4): 3
✅ Correct!

--- Blank 3 ---
Options:
  1. return
  2. exit
  3. end
  4. yield

Your answer (1-4): 1
✅ Correct!
```

### 6. Results & Unlocking
```
================================================================================
📊 RESULTS
================================================================================
Score: 3/3 (100.0%)
Required to pass: 2/3
✅ PASSED! Great job!
🔓 INTERMEDIATE difficulty unlocked for this topic!
================================================================================

Press Enter to continue...
```

### 7. View Progress Report
```
================================================================================
📊 YOUR PROGRESS REPORT
================================================================================

Hello World:
  BEGINNER: 3/3 (best of 1 attempts)
  INTERMEDIATE: 2/3 (best of 2 attempts)

Integer Variables:
  BEGINNER: 2/3 (best of 1 attempt)

For Loops:
  BEGINNER: 3/3 (best of 1 attempt)

================================================================================
```

---

## 🔓 Unlocking System

### Difficulty Unlocking (Within Topics)

1. **BEGINNER**: Always unlocked ✅
2. **INTERMEDIATE**: Unlocked after attempting BEGINNER
3. **ADVANCED**: Unlocked after attempting INTERMEDIATE
4. **EXPERT**: Unlocked after attempting ADVANCED

**Important:** You just need to **attempt** the previous difficulty to unlock the next one. You don't need to pass it! This allows exploration while still encouraging progression.

### Topic Unlocking (Between Topics)

- **First topic**: Always unlocked ✅
- **Subsequent topics**: Unlocked after attempting BEGINNER level of previous topic

**Example:**
```
✅ Topic 1: Hello World (always unlocked)
   - Try BEGINNER level → Topic 2 unlocks!

✅ Topic 2: Integer Variables (now unlocked)
   - Try BEGINNER level → Topic 3 unlocks!

✅ Topic 3: For Loops (now unlocked)
   - Practice all 4 difficulty levels if you want!
   - Try BEGINNER level → Topic 4 unlocks!
```

---

## 📊 Progress Tracking

### What Gets Saved?

Your progress is automatically saved to `student_progress.json`:

```json
{
  "L3_01": {
    "current_difficulty": 2,
    "completed_difficulties": [],
    "scores": {
      "BEGINNER": [
        {"score": 2, "total": 3},
        {"score": 3, "total": 3}
      ],
      "INTERMEDIATE": [
        {"score": 2, "total": 3}
      ]
    },
    "unlocked": true
  }
}
```

### What Can You Track?

- ✅ **Best score** per difficulty level
- ✅ **Number of attempts** per difficulty
- ✅ **Unlocked status** for topics and difficulties
- ✅ **Progress history** across sessions

---

## 🎯 Curriculum Structure

### Current Topics (6 Total)

#### Level 1: Basics
1. **Hello World** (⭐ Difficulty 1)
   - 4 variations (BEGINNER: 2, INTERMEDIATE: 1, ADVANCED: 1)

2. **Integer Variables** (⭐ Difficulty 1)
   - 5 variations (BEGINNER: 2, INTERMEDIATE: 1, ADVANCED: 1, EXPERT: 1)

#### Level 3: Loops
3. **For Loops** (⭐⭐ Difficulty 2)
   - 7 variations (BEGINNER: 2, INTERMEDIATE: 3, ADVANCED: 2, EXPERT: 1)

4. **While Loops** (⭐⭐ Difficulty 2)
   - 5 variations (BEGINNER: 2, INTERMEDIATE: 1, ADVANCED: 1, EXPERT: 2)

#### Level 7: Vectors
5. **Vector Basics** (⭐⭐⭐ Difficulty 3)
   - 6 variations (BEGINNER: 2, INTERMEDIATE: 3, ADVANCED: 1, EXPERT: 1)

**Total: 27+ specification variations across 6 topics**

---

## 💡 Example: Progression Through "For Loops"

### Attempt 1: BEGINNER Level
**Specification:** "Create a for loop that counts from 0 to 5"

**Code Generated:**
```cpp
for(int i = 0; i <= 5; i++){
    cout << i << endl;
}
```

**Targets:** `for`, `int`, `cout`

**Your Score:** 2/3 (66.7%)
- ✅ Passed! (Min: 2/3)
- 🔓 INTERMEDIATE unlocked

---

### Attempt 2: INTERMEDIATE Level
**Specification:** "Write a loop that calculates the sum of numbers 1 to N"

**Code Generated:**
```cpp
int N = 10, sum = 0;
for(int i = 1; i <= N; i++){
    sum += i;
}
cout << "Sum: " << sum << endl;
```

**Targets:** `for`, `int`, `sum`

**Your Score:** 2/3 (66.7%)
- ✅ Passed! (Min: 2/3)
- 🔓 ADVANCED unlocked

---

### Attempt 3: ADVANCED Level
**Specification:** "Create a for loop that prints a multiplication table for a given number"

**Code Generated:**
```cpp
int num = 5;
for(int i = 1; i <= 10; i++){
    cout << num << " x " << i << " = " << (num * i) << endl;
}
```

**Targets:** `for`, `int`, `cout`

**Your Score:** 3/3 (100%)
- ✅ Passed! (Min: 3/3)
- 🔓 EXPERT unlocked

---

### Attempt 4: EXPERT Level (Challenge Mode!)
**Specification:** "Create nested for loops to print a pyramid pattern of stars"

**Code Generated:**
```cpp
int height = 5;
for(int i = 1; i <= height; i++){
    for(int j = 1; j <= height - i; j++){
        cout << " ";
    }
    for(int k = 1; k <= 2*i - 1; k++){
        cout << "*";
    }
    cout << endl;
}
```

**Targets:** `for`, `int`, `cout`

**Your Score:** 3/3 (100%)
- 🏆 MASTERY ACHIEVED!

---

## 📁 Files in This System

### Core Application Files

**Enhanced Quiz Apps (NEW):**
- `quiz_app_14b_variations.py` - High-quality with difficulty progression
- `quiz_app_1_5b_variations.py` - Fast with difficulty progression

**Original Quiz Apps (Still Available):**
- `quiz_app_14b.py` - Original high-quality version
- `quiz_app_1_5b.py` - Original fast version
- `quiz_app_templates.py` - Template-based (no LLM)

### Curriculum Files

**Enhanced Curriculum (NEW):**
- `curriculum_with_variations.py` - Topics with 4 difficulty levels

**Original Curriculum:**
- `cpp_curriculum_progression.py` - Single-specification topics

### Documentation

**NEW:**
- `rag_specification_variations.md` - 50+ specification variations
- `SPECIFICATION_VARIATIONS_README.md` - This file!

**Existing:**
- `QUIZ_APPS_README.md` - Original quiz app guide
- `DETERMINISTIC_APPROACH.md` - Deterministic processing explained
- `MIDTERM_PROJECT_SPECIFICATION.md` - Midterm project guide

### Other Files
- `genai_ollama_rag_deterministic_1_5b.py` - RAG + Deterministic system
- `midterm_project_starter.py` - Project starter code
- `student_progress.json` - Your saved progress (auto-generated)

---

## 🎓 Recommended Learning Path

### For Beginners:
1. Start with `quiz_app_1_5b_variations.py` (faster, good for practice)
2. Begin with "Hello World" topic, BEGINNER level
3. Complete at least 2/3 to pass and unlock next difficulty
4. Try INTERMEDIATE level to challenge yourself
5. Move to next topic when ready (after attempting BEGINNER)

### For Advanced Students:
1. Use `quiz_app_14b_variations.py` for highest quality
2. Jump to topics you want to practice (if unlocked)
3. Start at INTERMEDIATE or ADVANCED if you're confident
4. Chase EXPERT level for mastery challenges
5. Return to previous topics to complete all difficulty levels

### For Instructors:
1. Use `quiz_app_14b_variations.py` for formal assessments
2. Assign specific topics and difficulty levels
3. Check `student_progress.json` to monitor progress
4. Encourage students to attempt EXPERT levels for extra credit
5. Use `rag_specification_variations.md` to understand learning objectives

---

## 🔧 Customization

### Adding New Topics

Edit `curriculum_with_variations.py`:

```python
TopicWithVariations(
    id="L5_01",
    name="Your New Topic",
    description="Brief description of the topic",
    base_difficulty=2,  # 1-5 stars
    prerequisites=["L3_01"],  # Previous topic IDs
    variations=[
        SpecificationVariation(
            difficulty=DifficultyLevel.BEGINNER,
            specification="Simple task description",
            description="What students learn",
            min_score=2
        ),
        # Add more variations...
    ]
)
```

### Adding New Specification Variations

Edit `rag_specification_variations.md`:

```markdown
### Topic X.X: Your Topic

#### BEGINNER Variations:
1. **Simple task description**
   - Focus: Core concept
   - Min score: 2/3
   - Example targets: keyword1, keyword2, keyword3
   - Key concepts: what students learn

#### INTERMEDIATE Variations:
2. **More complex task description**
   - Focus: Combined concepts
   - Min score: 2/3
   - Example targets: keyword1, keyword2, keyword3
   - Key concepts: additional learning
```

---

## 🆚 System Comparison

| Feature | Templates | 1.5b Original | 14b Original | 1.5b Variations ⭐ | 14b Variations ⭐ |
|---------|-----------|---------------|--------------|---------------------|-------------------|
| **Speed** | 3s | 8s | 25-30s | 8s | 25-30s |
| **Quality** | Fixed | Good | Excellent | Good | Excellent |
| **Variety** | None | High | High | Very High | Very High |
| **Difficulty Levels** | 1 | 1 | 1 | 4 | 4 |
| **Progression** | Linear | Linear | Linear | 2D | 2D |
| **Unlocking** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Progress Tracking** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Challenge Mode** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Cost** | $0 | $0.001 | $0.005 | $0.001 | $0.005 |
| **Best For** | Fixed curriculum | Fast practice | Exams | Practice + progression | Assessments + progression |

---

## ❓ FAQ

**Q: Do I need to pass BEGINNER to unlock INTERMEDIATE?**
A: You just need to **attempt** BEGINNER. Even if you get 0/3, INTERMEDIATE will unlock! This encourages exploration.

**Q: Can I skip topics?**
A: No, you must attempt BEGINNER level of previous topic to unlock the next topic. This ensures foundational knowledge.

**Q: Can I return to previous topics?**
A: Yes! You can always go back to any unlocked topic to practice at any difficulty level.

**Q: What happens if I retry a difficulty?**
A: Your **best score** is saved. You can retry as many times as you want to improve your score.

**Q: Can I use both 1.5b and 14b apps?**
A: Yes! They share the same progress file (`student_progress.json`), so your progress syncs between them.

**Q: Which app should I use for practice?**
A: Use `quiz_app_1_5b_variations.py` - it's 3x faster and great for daily practice.

**Q: Which app should I use for exams?**
A: Use `quiz_app_14b_variations.py` - it has higher quality questions.

**Q: How do I reset my progress?**
A: Delete `student_progress.json` file. Your progress will start fresh.

**Q: Can I see the correct code before answering?**
A: Yes! The complete code is shown at the top. This helps you understand context before filling blanks.

**Q: What's the minimum score to pass?**
A: BEGINNER/INTERMEDIATE: 2/3 (66.7%), ADVANCED/EXPERT: 3/3 (100%)

---

## 🚀 Future Enhancements

Planned improvements:

1. **Hint System** - Progressive hints for struggling students
2. **Explanation Mode** - Auto-generated explanations for answers
3. **Custom Topics** - Allow instructors to add their own variations
4. **Time Tracking** - Record time spent per difficulty
5. **Peer Comparison** - See how you rank vs others
6. **Adaptive Difficulty** - Auto-adjust based on performance
7. **Multi-Language** - Extend to Python, Java, etc.

---

## 📞 Support

If you encounter issues:

1. Check that Ollama server is running
2. Verify URL is correct in the code
3. Check `student_progress.json` for corrupted data
4. Try deleting progress and starting fresh
5. Read error messages carefully

For more help, refer to:
- `QUIZ_APPS_README.md` - Original quiz guide
- `DETERMINISTIC_APPROACH.md` - Technical details
- `rag_specification_variations.md` - All specification variations

---

## 🎉 Get Started Now!

```bash
# Quick start - Fast practice mode
python quiz_app_1_5b_variations.py

# Or - High quality assessment mode
python quiz_app_14b_variations.py
```

**Happy learning! 📚✨**

---

Last Updated: 2025-11-19
Version: 1.0
