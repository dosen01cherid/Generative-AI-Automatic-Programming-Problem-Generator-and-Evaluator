# Generative AI: Automatic Programming Problem Generator and Evaluator

**Course:** Generative AI Applications
**Focus:** Leveraging Small LLMs for Educational Question Generation
**Updated:** 2025-11-19

---

## 📁 Folder Structure

This repository is organized into the following subfolders:

### `quiz_apps/`
Interactive quiz applications with progressive difficulty and curriculum tracking.

**Files:**
- `quiz_app_14b.py` - High-quality quiz (qwen2.5:14b, ~25-30s/question)
- `quiz_app_1_5b.py` - Fast quiz (qwen2.5:1.5b, ~8s/question)
- `quiz_app_14b_variations.py` - ⭐ Enhanced with difficulty progression & unlocking
- `quiz_app_1_5b_variations.py` - ⭐ Enhanced fast version with text-generation-webui support
- `quiz_app_templates.py` - Template-based (no LLM, ~3s/question)

**Quick Start:**
```bash
cd quiz_apps
python quiz_app_1_5b_variations.py  # Recommended for practice
```

---

### `curriculum/`
Curriculum definitions with topics, difficulty levels, and specification variations.

**Files:**
- `cpp_curriculum_progression.py` - Original C++ curriculum (50 topics, 10 levels)
- `curriculum_with_variations.py` - ⭐ Enhanced with 4 difficulty levels per topic

**Features:**
- 5 topics across 3 levels (Basics, Loops, Vectors)
- 27 specification variations
- 4 difficulty levels: BEGINNER → INTERMEDIATE → ADVANCED → EXPERT
- Progressive unlocking system

---

### `documentation/`
Complete guides, technical reports, and session summaries.

**Files:**
- `QUIZ_APPS_README.md` - User guide for all quiz applications
- `SPECIFICATION_VARIATIONS_README.md` - ⭐ Guide to difficulty progression system
- `SESSION_SUMMARY.md` - ⭐ Complete development session documentation
- `DETERMINISTIC_APPROACH.md` - Technical details of deterministic processing

**Start Here:**
- **New users:** Read `QUIZ_APPS_README.md` first
- **Using variations:** Read `SPECIFICATION_VARIATIONS_README.md`
- **Technical details:** Read `DETERMINISTIC_APPROACH.md`

---

### `midterm_projects/`
Midterm exam project specifications and starter code.

**Files:**
- `MIDTERM_PROJECT_SPECIFICATION.md` - C++ question generation project (1 week)
- `ENGLISH_GRAMMAR_MIDTERM_PROJECT.md` - ⭐ English grammar learning project (1 week)
- `midterm_project_starter.py` - C++ project starter code
- `english_grammar_starter.py` - ⭐ English grammar starter code

**For Students:**
- Form teams of 3 students
- Choose ONE project (C++ or English Grammar)
- Complete within 1 week
- Follow specification requirements

---

### `utilities/`
Helper scripts, RAG infrastructure, and demonstration code.

**Files:**
- `genai_ollama_rag_deterministic_1_5b.py` - RAG + Deterministic system
- `demo_deterministic_poc.py` - Standalone proof of concept
- `rag_specification_variations.md` - ⭐ 50+ specification variations catalog

**Purpose:**
- RAG infrastructure for context reduction (85-95% token savings)
- Deterministic processing demonstrations
- Specification variations for LLM prompts

---

### `presentations/`
HTML presentations for classroom teaching.

**Files:**
- `presentation.html` - ⭐ Complete journey presentation (32 slides)

**Content:**
- From large context to deterministic systems
- RAG infrastructure
- Small LLM optimization
- Specification variations approach
- Interactive demonstrations

**Usage:**
```bash
start presentations/presentation.html
```

---

## 🚀 Quick Start Guide

### For Students Learning C++

**Option 1: Fast Practice Mode**
```bash
cd quiz_apps
python quiz_app_1_5b_variations.py
```
- Choose C++ curriculum
- Start with Hello World → BEGINNER
- Progress through difficulty levels
- Track your scores

**Option 2: Quality Assessment Mode**
```bash
cd quiz_apps
python quiz_app_14b_variations.py
```
- Higher quality questions
- Same progression system
- Slower but more thorough

---

### For Instructors

**Teaching Material:**
1. Open `presentations/presentation.html` for lectures
2. Assign `midterm_projects/MIDTERM_PROJECT_SPECIFICATION.md` for projects
3. Use `documentation/` for reference materials

**Monitoring Students:**
- Check `student_progress.json` files in quiz_apps folder
- Track which topics students are attempting
- See difficulty progression

---

### For Project Teams

**C++ Project:**
1. Read `midterm_projects/MIDTERM_PROJECT_SPECIFICATION.md`
2. Use `midterm_projects/midterm_project_starter.py` as template
3. Customize curriculum and approaches

**English Grammar Project:**
1. Read `midterm_projects/ENGLISH_GRAMMAR_MIDTERM_PROJECT.md`
2. Use `midterm_projects/english_grammar_starter.py` as template
3. Design your grammar topics (minimum 3)

---

## 🎯 Key Features

### 1. Multi-Curriculum Support ⭐ NEW
- Students can choose which curriculum to practice
- Separate progress tracking per curriculum
- Easy to add new curricula (Math, Science, etc.)

### 2. Progressive Difficulty System ⭐ NEW
- 4 levels per topic: BEGINNER → INTERMEDIATE → ADVANCED → EXPERT
- Attempt-based unlocking (not pass-based)
- Return to topics for challenge mode
- 2D progression (within topics + between topics)

### 3. Small LLM Optimization
- **1.5b model:** 8s per question, good quality
- **14b model:** 25-30s per question, excellent quality
- **Templates:** 3s per question, fixed curriculum
- **Deterministic processing:** 95% rule-based, 5% AI

### 4. Text-Generation-WebUI Support ⭐ NEW
- Alternative to Ollama for local LLM running
- Works with 1.5b version
- Same API interface

---

## 📊 System Comparison

| Feature | Templates | 1.5b (Ollama) | 1.5b (WebUI) | 14b (Ollama) | Variations 1.5b | Variations 14b |
|---------|-----------|---------------|--------------|--------------|-----------------|----------------|
| Speed | 3s | 8s | 8s | 25-30s | 8s | 25-30s |
| Quality | Fixed | Good | Good | Excellent | Good | Excellent |
| Difficulty Levels | 1 | 1 | 1 | 1 | 4 | 4 |
| Progress Tracking | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Curriculum Choice | ❌ | ❌ | ✅ NEW | ❌ | ✅ NEW | ✅ NEW |
| Unlocking | ❌ | ❌ | ❌ | ❌ | ✅ | ✅ |
| Best For | Speed | Practice | Practice (local) | Exams | Practice + progression | Assessment + progression |

---

## 🛠️ Installation & Setup

### Prerequisites
```bash
# Python 3.8+
pip install requests

# Option 1: Ollama (Recommended)
# Download from: https://ollama.com
ollama pull qwen2.5:1.5b
ollama pull qwen2.5:14b

# Option 2: text-generation-webui
# Follow instructions at: https://github.com/oobabooga/text-generation-webui
```

### Running Quiz Apps
```bash
# Navigate to quiz_apps folder
cd generativeai/quiz_apps

# Run variations version (recommended)
python quiz_app_1_5b_variations.py

# Or use 14b for higher quality
python quiz_app_14b_variations.py
```

---

## 📈 Statistics

### Content Created
- **Quiz Apps:** 5 applications (3,500+ lines)
- **Curriculum:** 2 systems, 50+ topics total
- **Documentation:** 4 guides (3,000+ lines)
- **Midterm Projects:** 2 specifications (2,200+ lines)
- **Utilities:** 3 tools (1,500+ lines)
- **Presentations:** 1 slide deck (32 slides, 1,900+ lines)

### Performance Metrics
- **RAG System:** 85-95% token reduction
- **Deterministic Processing:** 100% consistency, 88% faster than pure LLM
- **Question Generation:** 8s (1.5b) vs 25-30s (14b)
- **Curriculum Coverage:** 27 specification variations across 5 topics

---

## 🎓 Learning Paths

### Path 1: Beginner Student
1. Start with `quiz_apps/quiz_app_1_5b_variations.py`
2. Choose C++ curriculum
3. Begin with "Hello World" BEGINNER level
4. Progress through difficulty levels
5. Complete BEGINNER on all topics before advancing

### Path 2: Advanced Student
1. Use `quiz_apps/quiz_app_14b_variations.py`
2. Jump to interested topics
3. Start at INTERMEDIATE if confident
4. Chase EXPERT levels for mastery

### Path 3: Project Team
1. Read midterm project specification
2. Choose C++ or English Grammar
3. Use starter code as template
4. Implement custom curriculum and approaches
5. Complete within 1 week

### Path 4: Instructor
1. Review `presentations/presentation.html`
2. Assign midterm project
3. Monitor student progress files
4. Use documentation for reference

---

## 🔧 Customization

### Adding New Curriculum
```python
# In curriculum/ folder, create new file:
# my_curriculum.py

from curriculum_with_variations import (
    TopicWithVariations,
    SpecificationVariation,
    DifficultyLevel
)

class MyCurriculum:
    TOPICS = [
        TopicWithVariations(
            id="MY_01",
            name="My Topic",
            description="Topic description",
            base_difficulty=1,
            prerequisites=[],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Task description",
                    description="What students learn",
                    min_score=2
                ),
                # Add more variations...
            ]
        ),
        # Add more topics...
    ]
```

### Switching Between Ollama and text-generation-webui
```python
# In quiz_apps/quiz_app_1_5b_variations.py

# For Ollama (default):
BACKEND = "ollama"
OLLAMA_URL = "https://your-cloudflare-url.trycloudflare.com"

# For text-generation-webui:
BACKEND = "webui"
WEBUI_URL = "http://localhost:5000"  # Or your WebUI URL
```

---

## ❓ FAQ

**Q: Which quiz app should I use?**
A: Use `quiz_app_1_5b_variations.py` for practice (fast). Use `quiz_app_14b_variations.py` for formal assessments (quality).

**Q: How do I add new topics?**
A: Edit `curriculum/curriculum_with_variations.py` and add `TopicWithVariations` objects.

**Q: Can I use both Ollama and text-generation-webui?**
A: Yes! The apps support switching between backends.

**Q: Where is my progress saved?**
A: In `quiz_apps/student_progress.json` (auto-generated after first quiz).

**Q: How do I reset my progress?**
A: Delete `quiz_apps/student_progress.json`.

**Q: Can I add non-C++ curricula?**
A: Yes! Create new curriculum file and modify quiz apps to support it.

---

## 📚 Additional Resources

- **Ollama:** https://ollama.com
- **text-generation-webui:** https://github.com/oobabooga/text-generation-webui
- **C++ Reference:** https://cppreference.com
- **English Grammar:** Cambridge Dictionary, Grammarly

---

## 🤝 Contributing

This is an educational project. To contribute:
1. Create new curriculum in `curriculum/` folder
2. Add documentation in `documentation/` folder
3. Update this README with new features
4. Test thoroughly before committing

---

## 📧 Support

For questions or issues:
- Check documentation in `documentation/` folder
- Read relevant README files
- Review presentation slides
- Ask instructor during office hours

---

**Last Updated:** 2025-11-19
**Version:** 2.0 (Reorganized with subfolders)
**Repository:** [GitHub URL]

---

## 🎉 Quick Links

- **Start Quiz:** `cd quiz_apps && python quiz_app_1_5b_variations.py`
- **View Presentation:** `start presentations/presentation.html`
- **Read Docs:** `documentation/SPECIFICATION_VARIATIONS_README.md`
- **Midterm Project:** `midterm_projects/ENGLISH_GRAMMAR_MIDTERM_PROJECT.md`

Happy Learning! 🚀📚
