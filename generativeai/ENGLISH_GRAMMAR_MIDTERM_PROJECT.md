# Midterm Exam Project: English Grammar Learning System
## Leveraging Small LLMs for Fill-in-the-Blank Question Generation

**Course:** Generative AI Applications
**Project Type:** Group Project (3 students per group)
**Duration:** 1 week
**Weight:** 30% of final grade

---

## 📚 Project Overview

Your team will build an **English Grammar Learning System** that uses small Language Learning Models (LLMs) to generate varied fill-in-the-blank questions. The system must demonstrate progressive curriculum design, smart use of small LLMs, and effective student learning support.

### Key Objectives:
1. Design at least **3 curriculum topics** in English grammar progression
2. Implement fill-in-the-blank question generation using small LLMs
3. Create variation and difficulty levels to prevent memorization
4. Apply deterministic processing where appropriate
5. Track student progress and provide feedback

---

## 🎯 Learning Goals

By completing this project, students will:
- ✅ Understand how to leverage small LLMs effectively
- ✅ Design educational curriculum with progressive difficulty
- ✅ Implement RAG or deterministic approaches for consistency
- ✅ Create engaging learning experiences with gamification
- ✅ Evaluate LLM output quality and reliability
- ✅ Balance AI capabilities with rule-based systems

---

## 📋 Project Requirements

### 1. Curriculum Design (30 points)

#### Minimum Requirements:
- **At least 3 grammar topics** in progressive order
- **At least 2 difficulty levels** per topic (e.g., BEGINNER, INTERMEDIATE, ADVANCED)
- **At least 3 specification variations** per difficulty level
- **Clear learning objectives** for each topic

#### Examples of Grammar Topics (Choose Your Own):

**Option A: Tense-Focused Progression**
1. Simple Present Tense
   - BEGINNER: Basic statements ("I ___ to school")
   - INTERMEDIATE: Questions ("___ you like pizza?")
   - ADVANCED: Mixed statements and questions

2. Present Continuous Tense
   - BEGINNER: Basic actions ("She is ___ a book")
   - INTERMEDIATE: Questions ("What ___ you doing?")
   - ADVANCED: Time expressions ("I am working ___ the moment")

3. Simple Past Tense
   - BEGINNER: Regular verbs ("I ___ pizza yesterday")
   - INTERMEDIATE: Irregular verbs ("She ___ to Paris last year")
   - ADVANCED: Mixed with time expressions

**Option B: Part-of-Speech Progression**
1. Nouns and Articles
   - BEGINNER: Singular/Plural ("One dog, two ___")
   - INTERMEDIATE: Articles (a/an/the)
   - ADVANCED: Countable/Uncountable

2. Verbs and Auxiliaries
   - BEGINNER: Action verbs ("She ___ running")
   - INTERMEDIATE: Auxiliary verbs ("I ___ go to school")
   - ADVANCED: Modal verbs ("You ___ study hard")

3. Adjectives and Adverbs
   - BEGINNER: Basic adjectives ("The ___ cat")
   - INTERMEDIATE: Comparatives ("bigger ___ ")
   - ADVANCED: Adverbs ("He runs ___")

**Option C: Sentence Structure Progression**
1. Basic Sentence Formation
2. Question Formation
3. Complex Sentences (conjunctions)

**Your team decides:**
- Which grammar topics to cover
- How many topics (minimum 3)
- Difficulty levels (minimum 2 per topic)
- Learning progression order

---

### 2. LLM Selection & Justification (15 points)

#### Requirements:
- Choose an appropriate small LLM (e.g., qwen2.5:1.5b, llama3.2:3b, gemma2:2b, etc.)
- **Document your choice** with reasoning
- **Compare at least 2 LLMs** if possible
- Justify why a small LLM is suitable for this task

#### Evaluation Criteria:
- Model size (smaller = better, if quality maintained)
- Generation speed
- Output quality
- Cost/resource efficiency
- Availability (Ollama, Hugging Face, etc.)

#### Example LLM Options:
| Model | Size | Speed | Quality | Best For |
|-------|------|-------|---------|----------|
| qwen2.5:1.5b | 1.5B | Very Fast | Good | Practice, Homework |
| qwen2.5:7b | 7B | Fast | Excellent | Assessments |
| llama3.2:3b | 3B | Fast | Very Good | Balanced |
| gemma2:2b | 2B | Very Fast | Good | Quick generation |
| phi-3:mini | 3.8B | Fast | Very Good | Reasoning tasks |

---

### 3. Question Generation System (40 points)

#### Core Components:

**A. Question Type Design (15 points)**

You must implement **at least one** fill-in-the-blank question type:

**Type 1: Single Word Blank**
```
Sentence: "She ___ to school every day."
Options:
  A) go
  B) goes
  C) going
  D) gone
Correct: B
```

**Type 2: Multiple Blanks**
```
Sentence: "I ___(1)___ ___(2)___ a book right now."
Blank 1: [am, is, are, was]
Blank 2: [read, reads, reading, reader]
Correct: am, reading
```

**Type 3: Phrase/Expression Blank**
```
Sentence: "I have been living here ___ five years."
Options:
  A) since
  B) for
  C) during
  D) from
Correct: B
```

**Bonus Types (Optional, +5 points each):**
- Error correction: "She don't like pizza" → "She doesn't like pizza"
- Word order: "school / goes / She / to" → "She goes to school"
- Transformation: Active → Passive, Direct → Indirect speech

**Your team decides:**
- Which question types to implement
- How many types (minimum 1, more = bonus)
- Complexity level

**B. Specification Variations (10 points)**

Create explicit specification variations for each difficulty level:

```python
# Example for Present Tense - BEGINNER
variations = [
    "Generate a sentence using present tense with 'I'",
    "Create a present tense statement about daily routine",
    "Write a simple present tense sentence about hobbies"
]

# Example for Present Tense - ADVANCED
variations = [
    "Create a complex present tense sentence with adverb of frequency",
    "Generate a present tense question with time expression",
    "Write a present tense negative statement with reason clause"
]
```

**C. LLM Integration Strategy (15 points)**

Choose and implement ONE of these approaches:

**Approach 1: Two-Phase Generation (Recommended)**
1. Phase 1: LLM generates complete sentence from specification
2. Phase 2: Deterministically select blank position and create distractors

**Approach 2: Full LLM Generation**
1. LLM generates sentence + identifies blank + creates distractors
2. Validate output and regenerate if needed

**Approach 3: Hybrid (RAG + Small LLM)**
1. Retrieve example sentences from corpus
2. LLM adapts examples with variations
3. Deterministic blank selection and distractor generation

**Approach 4: Template-Based with LLM Enhancement**
1. Pre-defined sentence templates
2. LLM fills in content variations
3. Deterministic distractor creation

**Your team decides:**
- Which approach to use
- How to ensure quality
- How to handle errors

---

### 4. Distractor Generation (10 points)

#### Requirements:
Create **plausible wrong answers** that test understanding:

**Rule-Based Distractors (Recommended):**
```python
# For verb conjugation
correct = "goes"
distractors = ["go", "going", "gone"]  # Other forms

# For articles
correct = "a"
distractors = ["an", "the", "∅ (no article)"]

# For prepositions
correct = "at"
distractors = ["in", "on", "to"]  # Common confusions
```

**LLM-Generated Distractors (Advanced):**
```
Prompt: "Create 3 plausible wrong answers for this blank:
Sentence: She ___ to school every day.
Correct: goes
Make distractors test understanding of subject-verb agreement."

Output: go, going, gone
```

**Your team decides:**
- Rule-based vs LLM-generated distractors
- How many options per blank (3-4 recommended)
- Quality control methods

---

### 5. Interactive Quiz Application (20 points)

#### Minimum Features:

**A. User Interface (10 points)**
- Topic selection menu
- Difficulty level selection
- Question display with clear formatting
- Answer input and validation
- Immediate feedback (correct/incorrect)
- Score tracking

**B. Progress Tracking (10 points)**
- Save student scores
- Track attempts per topic
- Display progress report
- (Optional) Unlocking system like C++ project

#### Example Flow:
```
================================================================================
ENGLISH GRAMMAR QUIZ
================================================================================

Welcome! Select a topic:
  1. Simple Present Tense [0/3 difficulties attempted]
  2. Present Continuous [0/3 difficulties attempted]
  3. Simple Past Tense 🔒 (Complete previous topic first)

Your choice: 1

Select difficulty:
  1. BEGINNER (3 variations)
  2. INTERMEDIATE 🔒 (Complete BEGINNER first)
  3. ADVANCED 🔒

Your choice: 1

Question 1/5:
Fill in the blank:
"She ___ to school every day."

A) go
B) goes
C) going
D) gone

Your answer: B

✅ Correct!
Explanation: Use "goes" for third person singular in present tense.

Score: 1/1
```

---

### 6. Documentation (15 points)

#### Required Documents:

**A. README.md (5 points)**
- Project overview
- Installation instructions
- Usage guide
- Team member contributions

**B. CURRICULUM_DESIGN.md (5 points)**
- Topic selection justification
- Difficulty progression explanation
- Learning objectives per topic
- Specification variations list

**C. TECHNICAL_REPORT.md (5 points)**
- LLM selection justification
- Approach explanation (why chosen)
- Quality evaluation results
- Challenges faced and solutions

**D. Example Output (Bonus +3 points)**
- Screenshots of quiz in action
- Sample questions generated
- Progress tracking visualization

---

## 👥 Team Structure (3 Students)

### Recommended Roles:

**Student 1: Curriculum Designer**
- Design grammar topics and progression
- Create specification variations
- Define difficulty levels
- Write learning objectives

**Student 2: LLM Engineer**
- Select and test LLM
- Implement generation approach
- Handle errors and validation
- Optimize performance

**Student 3: Application Developer**
- Build interactive quiz interface
- Implement progress tracking
- Create distractor generation
- User experience design

**Note:** All team members must contribute to documentation.

---

## 📅 Timeline (1 Week)

### Day 1-2: Planning & Design
- Form teams (3 students)
- Choose grammar topics (minimum 3)
- Select LLM to use
- Design curriculum progression
- Create specification variations

**Deliverable:** CURRICULUM_DESIGN.md draft

### Day 3-4: Implementation
- Implement LLM integration
- Create question generation system
- Build distractor generation
- Test with multiple examples

**Deliverable:** Working question generator

### Day 5-6: Quiz Application
- Build interactive interface
- Implement progress tracking
- Add scoring and feedback
- Polish user experience

**Deliverable:** Working quiz application

### Day 7: Documentation & Testing
- Complete all documentation
- Test with real users (classmates)
- Fix bugs and improve
- Prepare presentation (5 minutes)

**Deliverable:** Final submission

---

## 📊 Evaluation Rubric (Total: 130 points + 15 bonus)

### 1. Curriculum Design (30 points)
- [10] Topic selection and justification
- [10] Difficulty progression (at least 2 levels per topic)
- [10] Specification variations (at least 3 per level)

### 2. LLM Selection & Justification (15 points)
- [5] Model choice reasoning
- [5] Performance comparison
- [5] Efficiency considerations

### 3. Question Generation System (40 points)
- [15] Question type implementation
- [10] Specification variation system
- [15] LLM integration approach

### 4. Distractor Generation (10 points)
- [5] Quality of wrong answers
- [5] Difficulty appropriateness

### 5. Interactive Application (20 points)
- [10] User interface quality
- [10] Progress tracking system

### 6. Documentation (15 points)
- [5] README completeness
- [5] Curriculum design documentation
- [5] Technical report quality

### Bonus Points (Up to +15)
- [+5] Each additional question type beyond first
- [+5] Unlocking/gamification system
- [+5] Exceptional code quality and comments
- [+3] Example output screenshots/videos

### Presentation (Not graded separately)
- 5-minute team presentation
- Demonstrate working system
- Explain design choices
- Show example questions

---

## 🎯 Grading Scale

| Score | Grade | Description |
|-------|-------|-------------|
| 117-130+ | A | Excellent - All requirements exceeded |
| 104-116 | B | Good - All requirements met well |
| 91-103 | C | Satisfactory - Minimum requirements met |
| 78-90 | D | Needs improvement |
| <78 | F | Does not meet minimum requirements |

---

## 💡 Example Project Ideas

### Project Idea 1: "Tense Master"
**Topics:** Simple Present, Present Continuous, Simple Past
**LLM:** qwen2.5:1.5b (fast generation)
**Approach:** Two-phase (LLM generates sentence, deterministic blanks)
**Special Feature:** Tense transformation exercises

### Project Idea 2: "Grammar Explorer"
**Topics:** Articles, Prepositions, Conjunctions
**LLM:** llama3.2:3b (good reasoning)
**Approach:** RAG + small LLM (retrieve examples, LLM adapts)
**Special Feature:** Context-aware distractors

### Project Idea 3: "Sentence Builder"
**Topics:** Word Order, Question Formation, Negation
**LLM:** gemma2:2b (very fast)
**Approach:** Template + LLM enhancement
**Special Feature:** Sentence construction from scrambled words

---

## 📚 Resources & References

### Ollama Models
- Installation: https://ollama.com/download
- Model library: https://ollama.com/library
- API docs: https://github.com/ollama/ollama/blob/main/docs/api.md

### Grammar Resources
- **English Grammar Basics:** Cambridge Dictionary, Grammarly
- **Corpus for examples:** COCA (Corpus of Contemporary American English)
- **Question types:** TOEFL, IELTS, Cambridge English tests

### Code Examples
- Reference your C++ fill-in-the-blank project code
- Use similar structure for progress tracking
- Adapt deterministic approaches from previous work

### Python Libraries
```bash
pip install requests  # For Ollama API
pip install json      # For data storage
pip install random    # For question selection
pip install re        # For text processing
```

---

## 🚀 Getting Started

### Step 1: Set Up Environment
```bash
# Install Ollama
# Download from: https://ollama.com

# Pull a small model
ollama pull qwen2.5:1.5b

# Test it
ollama run qwen2.5:1.5b "Generate a simple present tense sentence"
```

### Step 2: Team Meeting 1
- Decide on 3+ grammar topics
- Assign roles (Curriculum, LLM, App)
- Create shared GitHub repository
- Set up project structure

### Step 3: Quick Prototype
```python
# Test LLM with simple prompt
import requests

def generate_sentence(topic):
    prompt = f"Generate a simple {topic} sentence with one blank for fill-in-the-blank quiz"
    response = requests.post('http://localhost:11434/api/generate', json={
        'model': 'qwen2.5:1.5b',
        'prompt': prompt,
        'stream': False
    })
    return response.json()['response']

# Test
print(generate_sentence("present tense"))
```

### Step 4: Iterate and Improve
- Start simple (single question type, 3 topics)
- Add complexity gradually
- Test with classmates
- Gather feedback and improve

---

## ⚠️ Common Pitfalls to Avoid

### 1. Over-Complexity
❌ **Bad:** Trying to cover 15 grammar topics with 5 difficulty levels each
✅ **Good:** Start with 3 well-designed topics, 2-3 difficulty levels

### 2. Ignoring Quality Control
❌ **Bad:** Accepting all LLM output without validation
✅ **Good:** Validate sentences are grammatically correct

### 3. Poor Distractors
❌ **Bad:** Random words as wrong answers
✅ **Good:** Plausible alternatives that test understanding

### 4. No Progress Tracking
❌ **Bad:** Each quiz session starts fresh
✅ **Good:** Save progress, show improvement over time

### 5. Vague Specifications
❌ **Bad:** "Generate a sentence"
✅ **Good:** "Generate a present tense sentence about daily routine with subject 'I'"

---

## 🎓 Learning Objectives Check

By the end of this project, you should be able to:

- [ ] Design a progressive educational curriculum
- [ ] Select appropriate small LLM for specific tasks
- [ ] Implement two-phase or hybrid LLM generation
- [ ] Create quality control for LLM outputs
- [ ] Generate plausible distractors (wrong answers)
- [ ] Build interactive quiz application
- [ ] Track and visualize student progress
- [ ] Document technical decisions
- [ ] Work effectively in a team of 3
- [ ] Present technical work clearly

---

## 📧 Submission Requirements

### What to Submit:

1. **GitHub Repository Link** containing:
   - All source code
   - Documentation (README, CURRICULUM, TECHNICAL_REPORT)
   - Example outputs
   - Requirements.txt (dependencies)

2. **Demo Video** (3-5 minutes):
   - Show quiz in action
   - Demonstrate question generation
   - Explain key features
   - Show progress tracking

3. **Team Contribution Report**:
   - What each member did
   - Challenges faced
   - Solutions implemented

### Submission Format:
- Submit via university LMS
- Due: [Insert deadline]
- Late penalty: -10% per day

---

## ❓ Frequently Asked Questions

**Q: Can we use topics other than grammar?**
A: Yes, but it must be language learning (vocabulary, pronunciation, idioms, etc.). Get approval from instructor first.

**Q: Can we use a larger model like 14b?**
A: Yes, but you must justify why a small model (1.5b-7b) wouldn't work. The goal is to leverage SMALL LLMs effectively.

**Q: Can we use ChatGPT or Claude API?**
A: No. You must use open-source models via Ollama or Hugging Face. This is about learning to work with resource constraints.

**Q: How many questions should the system generate?**
A: At least 5 questions per topic per difficulty level. More is better.

**Q: Can we use existing grammar question databases?**
A: You can use them for reference and inspiration, but questions must be LLM-generated with your specifications.

**Q: What if our LLM generates bad grammar?**
A: Implement validation! Check output quality, regenerate if needed, or add post-processing rules.

**Q: Can we work with 2 or 4 students?**
A: Strictly 3 students per group. Form teams in Week 1.

**Q: Do we need to deploy the application online?**
A: No, local/offline is fine. Bonus points (+5) if you deploy (Streamlit, Gradio, etc.).

---

## 🌟 Inspiration Examples

### Example 1: Verb Conjugation Master
```
Topic: Present Tense Verb Conjugation
Difficulty: BEGINNER

Question:
"She ___ breakfast every morning."

Options:
A) eat
B) eats
C) eating
D) eaten

Correct: B

Explanation:
"She" is third person singular, so we add 's' to the verb in present tense.

Generated by: qwen2.5:1.5b in 2.3 seconds
```

### Example 2: Article Challenge
```
Topic: Articles (a/an/the)
Difficulty: INTERMEDIATE

Question:
"I saw ___ elephant at ___ zoo yesterday."

Blank 1 options: [a, an, the, ∅]
Blank 2 options: [a, an, the, ∅]

Correct: an, the

Explanation:
"an" before vowel sound (elephant)
"the" for specific zoo (we know which one)

Generated by: llama3.2:3b in 3.1 seconds
```

### Example 3: Preposition Practice
```
Topic: Prepositions of Time
Difficulty: ADVANCED

Question:
"The meeting is scheduled ___ 3 PM ___ Friday ___ next week."

Options for blank 1: [at, on, in, by]
Options for blank 2: [at, on, in, by]
Options for blank 3: [at, on, in, by]

Correct: at, on, ∅

Explanation:
- "at" for specific time (3 PM)
- "on" for day (Friday)
- no preposition before "next week"

Generated by: qwen2.5:7b in 4.5 seconds
```

---

## 🎉 Get Started Now!

1. **Form your team** of 3 students
2. **Schedule first meeting** to divide roles
3. **Choose 3 grammar topics** you want to cover
4. **Select an LLM** to test (start with qwen2.5:1.5b)
5. **Create project repository** on GitHub
6. **Start coding** and have fun!

Remember: The goal is not perfection, but demonstrating understanding of how to leverage small LLMs effectively for educational applications.

Good luck! 🚀

---

**Questions?**
- Office hours: [Insert times]
- Email: [Insert email]
- Discussion forum: [Insert link]

---

**Last Updated:** 2025-11-19
**Version:** 1.0
**Instructor:** [Insert name]
