# Midterm Project: Small LLM Optimization Framework

## Project Overview

**Title:** Leveraging Small Language Models for Educational Question Generation: A Comparative Study

**Duration:** 1 Week (7 days)
**Team Size:** 3-4 Students
**Points:** 100 points
**Type:** Research + Implementation

---

## Learning Objectives

By completing this project, students will:

1. **Understand LLM Optimization Strategies**
   - Learn different approaches to leverage small vs large models
   - Understand trade-offs between speed, quality, and cost

2. **Implement Multiple AI Strategies**
   - Pure AI approaches
   - Hybrid approaches (AI + deterministic)
   - Adaptive approaches (fallback logic)
   - Prompt engineering techniques

3. **Conduct Scientific Evaluation**
   - Design experiments
   - Collect quantitative data
   - Perform statistical analysis
   - Draw evidence-based conclusions

4. **Technical Writing & Communication**
   - Write technical reports
   - Create data visualizations
   - Present findings clearly

---

## Problem Statement

Large language models (14b+ parameters) produce high-quality output but are slow and expensive. Small models (1.5b-3b parameters) are fast and cheap but less reliable.

**Research Question:** What is the optimal strategy for leveraging small LLMs in educational question generation?

---

## The 5 Strategies to Compare

### Strategy 1: Pure Small Model ⚡
**Approach:** Use qwen2.5:1.5b for everything

**How it works:**
- Single prompt asks model to generate code + targets + distractors
- No post-processing
- Simplest approach

**Expected Performance:**
- Speed: ⚡⚡⚡⚡⚡ Very Fast (~10s)
- Quality: ⭐⭐⭐ Acceptable (60-70%)
- Cost: 💰 Very Low
- Reliability: 🎯🎯 Low (60-70% success rate)

**Implementation Complexity:** Easy

---

### Strategy 2: Deterministic Heavy 🎯
**Approach:** Small model (1.5b) + deterministic processing (95%)

**How it works:**
- 1.5b generates code only (simple task)
- Regex patterns extract all tokens
- Rule-based scoring selects best targets
- Template lookup provides distractors
- Deterministic string replacement creates question

**Expected Performance:**
- Speed: ⚡⚡⚡⚡ Fast (~8s)
- Quality: ⭐⭐⭐⭐ Good (85-90%)
- Cost: 💰 Very Low
- Reliability: 🎯🎯🎯🎯 High (98% success rate)

**Implementation Complexity:** Medium (adapt existing code)

**Key Innovation:** Minimizes AI reliance, maximizes rule-based processing

---

### Strategy 3: Hybrid (1.5b + 14b) 🔬
**Approach:** Fast generation (1.5b) + quality validation (14b)

**How it works:**
- Phase 1: 1.5b generates code quickly (~10s)
- Phase 2: 14b validates and extracts targets/distractors (~15s)
- Combines speed of small model with quality of large model

**Expected Performance:**
- Speed: ⚡⚡⚡ Medium (~25s)
- Quality: ⭐⭐⭐⭐⭐ Very Good (90-95%)
- Cost: 💰💰 Medium
- Reliability: 🎯🎯🎯🎯🎯 Very High (95%+ success rate)

**Implementation Complexity:** Medium

**Key Innovation:** Best of both worlds - reasonable speed with high quality

---

### Strategy 4: Smart Fallback 🧠
**Approach:** Adaptive strategy selection based on quality

**How it works:**
- Try deterministic approach first (fast)
- Check quality of output automatically
- If quality < threshold → retry with 14b
- Track fallback rate, optimize threshold

**Expected Performance:**
- Speed: ⚡⚡⚡⚡ Variable (~8-25s, avg 12s)
- Quality: ⭐⭐⭐⭐ Good (85-92%)
- Cost: 💰 to 💰💰 Low-Medium (depends on fallback rate)
- Reliability: 🎯🎯🎯🎯 High (90%+ success rate)

**Implementation Complexity:** Hard

**Key Innovation:** Adapts strategy based on task difficulty

---

### Strategy 5: Prompt Engineering 📝
**Approach:** Enhanced prompting for small model

**How it works:**
- Include 3-5 few-shot examples in prompt
- Use chain-of-thought reasoning
- Step-by-step instructions
- Clear template constraints
- Makes 1.5b perform better through better prompting

**Expected Performance:**
- Speed: ⚡⚡⚡ Medium (~15s)
- Quality: ⭐⭐⭐⭐ Good (75-85%)
- Cost: 💰 Low (1.5b only, but longer prompts)
- Reliability: 🎯🎯🎯 Medium-High (75-85% success rate)

**Implementation Complexity:** Easy-Medium

**Key Innovation:** Maximizes small model capability through prompting

---

## Deliverables & Grading

### 1. Implementation (40 points)

**Requirements:**
- [ ] All 5 strategies implemented and working (25 pts)
- [ ] Unified interface (QuestionGenerationStrategy base class) (5 pts)
- [ ] Error handling and logging (5 pts)
- [ ] Code quality (comments, organization) (5 pts)

**Grading Criteria:**
- **Excellent (36-40):** All strategies work flawlessly, clean code, good error handling
- **Good (32-35):** 4-5 strategies work, minor bugs, decent code quality
- **Satisfactory (28-31):** 3-4 strategies work, some bugs, acceptable code
- **Needs Improvement (<28):** <3 strategies work or major issues

---

### 2. Evaluation Framework (30 points)

**Requirements:**
- [ ] Automated quality metrics (10 pts)
- [ ] 4 experiments completed (12 pts)
  - [ ] Speed comparison (3 pts)
  - [ ] Quality comparison (3 pts)
  - [ ] Cost-quality analysis (3 pts)
  - [ ] Failure analysis (3 pts)
- [ ] Statistical analysis (4 pts)
- [ ] Visualizations (4 pts)

**Grading Criteria:**
- **Excellent (27-30):** All experiments, rigorous analysis, excellent visualizations
- **Good (24-26):** All experiments, good analysis, good visualizations
- **Satisfactory (21-23):** 3+ experiments, basic analysis, basic charts
- **Needs Improvement (<21):** <3 experiments or weak analysis

---

### 3. Technical Report (20 points)

**Requirements:**
- [ ] Clear introduction and motivation (3 pts)
- [ ] Methodology section (strategy descriptions) (4 pts)
- [ ] Results section (data, tables, charts) (5 pts)
- [ ] Discussion (interpretation, insights) (4 pts)
- [ ] Conclusion and recommendations (2 pts)
- [ ] Professional formatting (2 pts)

**Length:** 15-20 pages (including figures/tables)

**Grading Criteria:**
- **Excellent (18-20):** Clear, comprehensive, insightful, professional
- **Good (16-17):** Complete, well-written, good analysis
- **Satisfactory (14-15):** All sections present, acceptable quality
- **Needs Improvement (<14):** Missing sections or poor quality

---

### 4. Presentation (10 points)

**Requirements:**
- [ ] 15-minute presentation (5 pts)
- [ ] Live demo of at least 2 strategies (3 pts)
- [ ] Q&A handling (2 pts)

**Content:**
- Problem and motivation (2 min)
- Methodology overview (3 min)
- Demo (4 min)
- Results and findings (4 min)
- Conclusions (2 min)

**Grading Criteria:**
- **Excellent (9-10):** Clear, engaging, good demo, answers questions well
- **Good (8):** Clear presentation, working demo, good answers
- **Satisfactory (7):** Acceptable presentation, demo works, basic answers
- **Needs Improvement (<7):** Unclear or incomplete

---

## Detailed Timeline

### Day 1: Monday - Setup & Planning (8 hours)

**Morning (9 AM - 12 PM):**
- 9:00 - 10:00: Team meeting, role assignment
- 10:00 - 11:00: Review starter code, understand base classes
- 11:00 - 12:00: Set up development environment, test Ollama connection

**Afternoon (1 PM - 5 PM):**
- 1:00 - 2:00: Design system architecture
- 2:00 - 3:30: Create test dataset (50 cases)
- 3:30 - 5:00: Implement base classes and utilities

**Evening Tasks:**
- Student 1: Plan Strategy 1 & 2 implementation
- Student 2: Plan Strategy 4 & 5 implementation
- Student 3: Plan evaluation framework
- Student 4: Start project documentation

**Deliverables:**
- ✅ Project plan document
- ✅ Code skeleton working
- ✅ Test dataset ready (50 cases)
- ✅ Team roles clarified

---

### Day 2: Tuesday - Core Implementation I (8 hours)

**Morning (9 AM - 12 PM):**
- Student 1: Implement Strategy 1 (Pure Small Model)
- Student 2: Research prompt engineering techniques
- Student 3: Build evaluation metrics (format, consistency)
- Student 4: Document strategies, set up report template

**Afternoon (1 PM - 5 PM):**
- Student 1: Implement Strategy 2 (Deterministic Heavy)
- Student 2: Begin Strategy 5 (Prompt Engineering)
- Student 3: Build quality metrics (distractor quality, difficulty)
- Student 4: Help with integration, testing

**Evening Tasks:**
- Test Strategy 1 & 2 with 5 sample cases
- Review code as team
- Plan next day's work

**Deliverables:**
- ✅ Strategy 1 working
- ✅ Strategy 2 working
- ✅ Basic evaluation metrics implemented

---

### Day 3: Wednesday - Core Implementation II (8 hours)

**Morning (9 AM - 12 PM):**
- Student 1: Implement Strategy 3 (Hybrid)
- Student 2: Complete Strategy 5, begin Strategy 4
- Student 3: Build experiment runners (speed, quality)
- Student 4: Test all completed strategies

**Afternoon (1 PM - 5 PM):**
- Student 1: Test and debug Strategy 3
- Student 2: Complete Strategy 4 (Smart Fallback)
- Student 3: Complete evaluation framework
- Student 4: Integration testing, fix bugs

**Evening Tasks:**
- Integration testing all strategies
- Fix critical bugs
- Prepare for experiments

**Deliverables:**
- ✅ All 5 strategies implemented
- ✅ Evaluation framework complete
- ✅ Integration testing passed

---

### Day 4: Thursday - Experimentation (10 hours)

**Morning (9 AM - 1 PM):**
- Run Experiment 1: Speed comparison (all 50 test cases)
- Run Experiment 2: Quality evaluation (30 test cases)
- Collect raw data, save to files

**Afternoon (2 PM - 6 PM):**
- Run Experiment 3: Cost-quality trade-off analysis
- Run Experiment 4: Failure analysis (20 edge cases)
- Data processing and cleaning

**Evening (7 PM - 9 PM):**
- Statistical analysis (t-tests, ANOVA)
- Begin creating visualizations
- Preliminary findings discussion

**Deliverables:**
- ✅ All experimental data collected
- ✅ Raw data files saved
- ✅ Initial statistical analysis

---

### Day 5: Friday - Analysis & Visualization (8 hours)

**Morning (9 AM - 12 PM):**
- Complete statistical analysis
- Create comparison tables
- Generate all visualizations:
  - Speed comparison bar chart
  - Quality radar chart
  - Cost vs quality scatter plot
  - Success rate comparison
  - Failure mode analysis

**Afternoon (1 PM - 5 PM):**
- Interpret results
- Identify key findings
- Draw conclusions
- Prepare recommendations

**Evening Tasks:**
- Team discussion of findings
- Outline report structure
- Divide writing tasks

**Deliverables:**
- ✅ Complete analysis
- ✅ All visualizations created
- ✅ Key findings identified
- ✅ Report outline ready

---

### Day 6: Saturday - Report Writing (8 hours)

**Morning (9 AM - 1 PM):**
- Student 1: Write methodology section
- Student 2: Write results section
- Student 3: Write analysis/discussion section
- Student 4: Write introduction & conclusion

**Afternoon (2 PM - 6 PM):**
- Combine sections
- Add figures and tables
- Format report (LaTeX or Markdown)
- Code documentation

**Evening (7 PM - 9 PM):**
- Internal review
- Revisions
- Proofreading

**Deliverables:**
- ✅ Complete draft report (15-20 pages)
- ✅ All code documented
- ✅ README completed

---

### Day 7: Sunday - Final Polish & Presentation (6 hours)

**Morning (9 AM - 12 PM):**
- Final report revisions
- Create presentation slides (15-20 slides)
- Prepare demo script

**Afternoon (1 PM - 4 PM):**
- Practice presentation
- Test demo on clean environment
- Final submission preparation

**Deliverables:**
- ✅ Final report (PDF)
- ✅ Presentation slides
- ✅ Source code + README
- ✅ Demo ready
- ✅ Submission package

---

## Team Roles & Responsibilities

### Role 1: Implementation Lead (Strategies 1-3)
**Assigned to:** Student 1

**Responsibilities:**
1. Implement Strategy 1: Pure Small Model
2. Implement Strategy 2: Deterministic Heavy (adapt our code)
3. Implement Strategy 3: Hybrid
4. Write methodology section for these strategies
5. Help with integration

**Skills Required:**
- Strong Python programming
- API integration (Ollama)
- Understanding of LLM prompting
- Pattern matching (regex)

**Time Commitment:** ~25-30 hours

**Deliverables:**
- Working implementations of Strategies 1-3
- Unit tests for each strategy
- Methodology write-up

---

### Role 2: Implementation Lead (Strategies 4-5)
**Assigned to:** Student 2

**Responsibilities:**
1. Implement Strategy 4: Smart Fallback
2. Implement Strategy 5: Prompt Engineering
3. Research prompt engineering techniques
4. Write methodology section for these strategies
5. Help with integration

**Skills Required:**
- Python programming
- Adaptive algorithms
- Prompt engineering
- Few-shot learning

**Time Commitment:** ~25-30 hours

**Deliverables:**
- Working implementations of Strategies 4-5
- Prompt template library
- Methodology write-up

---

### Role 3: Evaluation & Analysis Lead
**Assigned to:** Student 3

**Responsibilities:**
1. Build evaluation framework
2. Design and run all 4 experiments
3. Collect and process data
4. Statistical analysis
5. Create visualizations
6. Write results and analysis sections

**Skills Required:**
- Python programming
- Data analysis (pandas, numpy)
- Statistics
- Visualization (matplotlib, seaborn)
- Scientific methodology

**Time Commitment:** ~30-35 hours

**Deliverables:**
- Complete evaluation framework
- All experimental data
- Statistical analysis
- Visualizations
- Results & analysis write-up

---

### Role 4: Integration & Documentation Lead
**Assigned to:** Student 4

**Responsibilities:**
1. System integration and testing
2. Code documentation
3. Write introduction & conclusion
4. Create README and user guide
5. Coordinate team activities
6. Prepare presentation
7. Quality assurance

**Skills Required:**
- Python programming
- Technical writing
- Project management
- LaTeX or Markdown
- Presentation skills

**Time Commitment:** ~25-30 hours

**Deliverables:**
- Integrated system
- Complete documentation
- Technical report (intro & conclusion)
- Presentation slides
- Submission package

---

## Test Dataset

### Categories and Examples

**Simple (20 cases):**
1. Simple for loop from 0 to 5
2. Print hello world
3. Declare and initialize integer variable
4. If statement checking if number is positive
5. While loop counting to 10
6. Basic arithmetic operations
7. Simple function with return value
8. Array declaration and initialization
9. Switch statement with 3 cases
10. Do-while loop example
11. Boolean variable and condition
12. Simple cout statement
13. Variable assignment
14. Basic comparison operators
15. Increment and decrement operators
16. Simple calculation (sum of two numbers)
17. Character variable and output
18. Float variable with decimal
19. Return 0 from main
20. Namespace std usage

**Medium (20 cases):**
1. Vector with push_back operations
2. Class with constructor and methods
3. Function with multiple parameters
4. Array iteration with for loop
5. String manipulation with substr
6. For loop with nested if statement
7. Multiple variable declarations
8. Class with private and public members
9. Function overloading example
10. Vector iteration with iterator
11. Map with key-value pairs
12. Set operations (insert, find)
13. Queue push and pop operations
14. Stack implementation example
15. String concatenation
16. Reference parameters in function
17. Const member function
18. Static member variable
19. Default parameters in function
20. Multiple constructors (overloading)

**Hard (10 cases):**
1. Template function for generic sorting
2. STL algorithm usage with lambda
3. Smart pointer example with unique_ptr
4. Exception handling with try-catch
5. File I/O with ifstream
6. Template class implementation
7. Multiple inheritance example
8. Virtual functions and polymorphism
9. Operator overloading (+ operator)
10. Move semantics with rvalue references

**Edge Cases (20 cases):**
1. Empty main function
2. Very complex template metaprogramming
3. Just a single cout statement
4. Nested templates with multiple parameters
5. Very long function (100+ lines)
6. Ambiguous: "sorting" (many implementations)
7. Minimal code (just return 0)
8. Code with comments only
9. Multiple classes in one file
10. Recursive function (factorial)
11. Infinite loop example
12. Pointer arithmetic
13. Dynamic memory allocation (new/delete)
14. Multiple header includes
15. Namespace definition
16. Using directive vs declaration
17. Typedef examples
18. Enum class definition
19. Struct vs class
20. Friend function example

---

## Metrics Definitions

### Performance Metrics

**1. Generation Time**
- **Definition:** Total time from prompt submission to result returned
- **Unit:** Seconds
- **Measurement:** `time.time()` before and after generation
- **Target:** <30s acceptable, <15s good, <10s excellent

**2. Tokens Consumed**
- **Definition:** Total tokens used (prompt + response)
- **Unit:** Token count
- **Estimation:** ~4 chars = 1 token
- **Target:** <5000 tokens acceptable

**3. API Calls**
- **Definition:** Number of Ollama API calls made
- **Unit:** Count
- **Measurement:** Increment counter for each request
- **Target:** Minimize (fewer is better)

**4. Cost Estimate**
- **Definition:** Estimated cost in dollars
- **Calculation:**
  - 1.5b: $0.10 per 1M tokens
  - 14b: $0.50 per 1M tokens
- **Unit:** USD
- **Target:** <$0.01 per question

---

### Quality Metrics

**1. Format Compliance**
- **Definition:** Does output match expected structure?
- **Scale:** 0.0 (no match) to 1.0 (perfect match)
- **Checks:**
  - Has `code` field
  - Has `question_code` field
  - Has `sub_questions` list
  - Proper JSON/dict structure
- **Target:** >0.9 acceptable, >0.95 good

**2. Target-Answer Consistency**
- **Definition:** Do all targets exist in original code?
- **Scale:** 0.0 to 1.0 (percentage of targets found)
- **Measurement:**
  - Check if each target appears in code
  - Calculate: found_targets / total_targets
- **Target:** 1.0 (100% consistency required)

**3. Distractor Quality**
- **Definition:** How plausible are the wrong options?
- **Scale:** 1-5 (1=poor, 5=excellent)
- **Criteria:**
  - Same category as target (e.g., both are loops)
  - Syntactically valid in context
  - Not obviously wrong
  - Semantically similar
- **Measurement:** Manual evaluation or rule-based heuristics
- **Target:** >3.5 acceptable, >4.0 good

**4. Code Correctness**
- **Definition:** Is the generated code valid C++?
- **Scale:** Boolean (true/false)
- **Checks:**
  - Has `#include` statements
  - Has `main()` function
  - Proper syntax (basic check)
  - No obvious errors
- **Target:** 100% correct

**5. Question Difficulty**
- **Definition:** Estimated difficulty level
- **Scale:** 1-5 (1=very easy, 5=very hard)
- **Factors:**
  - Target complexity (int=easy, template=hard)
  - Code length
  - Concept sophistication
- **Measurement:** Rule-based scoring
- **Target:** Distribute evenly across levels

---

### Robustness Metrics

**1. Success Rate**
- **Definition:** Percentage of successful generations
- **Scale:** 0.0 to 1.0 (0% to 100%)
- **Measurement:** successes / total_attempts
- **Target:** >0.90 acceptable, >0.95 good

**2. Failure Mode Analysis**
- **Definition:** Categorization of failures
- **Categories:**
  - Format error (wrong structure)
  - Consistency error (target not in code)
  - Timeout error
  - API error
  - Quality error (low quality but valid)
- **Measurement:** Count failures by category
- **Target:** Identify common patterns

**3. Edge Case Handling**
- **Definition:** Performance on unusual inputs
- **Measurement:** Success rate on edge case dataset
- **Target:** >0.70 acceptable (edge cases are hard)

---

## Statistical Analysis

### Required Tests

**1. Speed Comparison (ANOVA)**
```python
from scipy import stats

# Compare mean generation times
# H0: All strategies have same mean time
# H1: At least one strategy differs

times_strategy1 = [...]
times_strategy2 = [...]
# ... for all 5 strategies

f_stat, p_value = stats.f_oneway(
    times_strategy1,
    times_strategy2,
    times_strategy3,
    times_strategy4,
    times_strategy5
)

if p_value < 0.05:
    print("Significant difference in speed")
```

**2. Pairwise Comparisons (t-tests)**
```python
# Compare each pair of strategies
# Use Bonferroni correction for multiple comparisons

from itertools import combinations

strategies = [s1, s2, s3, s4, s5]
alpha = 0.05 / 10  # Bonferroni correction (10 pairs)

for (name1, times1), (name2, times2) in combinations(strategies, 2):
    t_stat, p_value = stats.ttest_ind(times1, times2)
    if p_value < alpha:
        print(f"{name1} significantly different from {name2}")
```

**3. Quality Comparison (Chi-square)**
```python
# Compare success rates
# H0: All strategies have same success rate

from scipy.stats import chi2_contingency

# Contingency table: [successes, failures] for each strategy
observed = [
    [strategy1_successes, strategy1_failures],
    [strategy2_successes, strategy2_failures],
    # ... etc
]

chi2, p_value, dof, expected = chi2_contingency(observed)

if p_value < 0.05:
    print("Significant difference in success rates")
```

**4. Correlation Analysis**
```python
# Analyze cost vs quality trade-off

import numpy as np
from scipy.stats import pearsonr

costs = [...]  # Cost for each strategy
qualities = [...]  # Quality score for each strategy

correlation, p_value = pearsonr(costs, qualities)

print(f"Correlation between cost and quality: {correlation:.3f}")
```

---

## Visualization Requirements

### Required Charts

**1. Speed Comparison Bar Chart**
```python
import matplotlib.pyplot as plt
import numpy as np

strategies = ['Pure\nSmall', 'Deterministic', 'Hybrid', 'Smart\nFallback', 'Prompt\nEng']
times = [10, 8, 25, 12, 15]  # Average times
errors = [2, 1, 3, 4, 2]  # Standard deviations

plt.figure(figsize=(10, 6))
plt.bar(strategies, times, yerr=errors, capsize=5)
plt.ylabel('Generation Time (seconds)')
plt.title('Speed Comparison Across Strategies')
plt.grid(axis='y', alpha=0.3)
plt.savefig('speed_comparison.png', dpi=300, bbox_inches='tight')
```

**2. Quality Radar Chart**
```python
import numpy as np
import matplotlib.pyplot as plt

categories = ['Format', 'Consistency', 'Distractors', 'Code\nCorrectness', 'Success\nRate']
strategy1_scores = [0.7, 0.6, 3.0/5, 0.9, 0.65]
strategy2_scores = [1.0, 1.0, 4.0/5, 1.0, 0.98]
# ... etc

# Create radar chart
angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False)
scores = np.concatenate((strategy1_scores, [strategy1_scores[0]]))
angles = np.concatenate((angles, [angles[0]]))

fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(projection='polar'))
ax.plot(angles, scores, 'o-', linewidth=2, label='Strategy 1')
# Add other strategies...
ax.set_xticks(angles[:-1])
ax.set_xticklabels(categories)
ax.legend()
plt.savefig('quality_radar.png', dpi=300, bbox_inches='tight')
```

**3. Cost vs Quality Scatter Plot**
```python
import matplotlib.pyplot as plt

strategies = ['S1', 'S2', 'S3', 'S4', 'S5']
costs = [0.001, 0.001, 0.005, 0.002, 0.0015]
qualities = [0.65, 0.88, 0.93, 0.87, 0.78]

plt.figure(figsize=(10, 6))
plt.scatter(costs, qualities, s=200, alpha=0.6)
for i, strategy in enumerate(strategies):
    plt.annotate(strategy, (costs[i], qualities[i]))

# Pareto frontier
# ... draw line connecting best trade-offs

plt.xlabel('Cost per Question (USD)')
plt.ylabel('Overall Quality Score')
plt.title('Cost-Quality Trade-off Analysis')
plt.grid(alpha=0.3)
plt.savefig('cost_quality.png', dpi=300, bbox_inches='tight')
```

**4. Success Rate Comparison**
```python
strategies = ['Pure\nSmall', 'Deterministic', 'Hybrid', 'Smart\nFallback', 'Prompt\nEng']
success_rates = [0.65, 0.98, 0.95, 0.91, 0.80]

plt.figure(figsize=(10, 6))
bars = plt.bar(strategies, success_rates)
# Color code: red <0.7, yellow 0.7-0.9, green >0.9
colors = ['red' if r < 0.7 else 'yellow' if r < 0.9 else 'green' for r in success_rates]
for bar, color in zip(bars, colors):
    bar.set_color(color)

plt.ylabel('Success Rate')
plt.ylim([0, 1])
plt.title('Success Rate Comparison')
plt.axhline(y=0.9, color='gray', linestyle='--', label='Target (90%)')
plt.legend()
plt.savefig('success_rates.png', dpi=300, bbox_inches='tight')
```

**5. Failure Mode Pie Chart**
```python
failure_modes = ['Format Error', 'Consistency Error', 'Timeout', 'API Error', 'Quality Error']
counts = [15, 8, 3, 2, 12]

plt.figure(figsize=(8, 8))
plt.pie(counts, labels=failure_modes, autopct='%1.1f%%', startangle=90)
plt.title('Distribution of Failure Modes')
plt.savefig('failure_modes.png', dpi=300, bbox_inches='tight')
```

---

## Report Structure

### Recommended Structure (15-20 pages)

**Title Page**
- Project title
- Team members
- Date
- Course information

**Abstract (1 page)**
- Brief summary of project
- Key findings (1-2 sentences each)
- Recommendations

**1. Introduction (2 pages)**
- Background and motivation
- Problem statement
- Research questions
- Contributions

**2. Related Work (1 page)**
- Large vs small models
- Prompt engineering
- Hybrid systems
- Educational AI

**3. Methodology (3-4 pages)**
- System architecture
- Strategy 1 description
- Strategy 2 description
- Strategy 3 description
- Strategy 4 description
- Strategy 5 description
- Evaluation framework

**4. Experimental Setup (2 pages)**
- Test dataset description
- Metrics definition
- Experimental protocol
- Implementation details

**5. Results (3-4 pages)**
- Experiment 1: Speed comparison
  - Table of average times
  - Bar chart
  - Statistical analysis
- Experiment 2: Quality comparison
  - Quality metrics table
  - Radar chart
  - Analysis
- Experiment 3: Cost-quality analysis
  - Scatter plot
  - Pareto frontier
  - Recommendations
- Experiment 4: Failure analysis
  - Failure rate table
  - Pie chart
  - Common failure patterns

**6. Discussion (2-3 pages)**
- Interpretation of results
- Strategy comparison
- When to use each strategy
- Limitations
- Threats to validity
- Future work

**7. Conclusion (1 page)**
- Summary of findings
- Best strategy for different scenarios
- Recommendations
- Final thoughts

**8. References**
- Academic papers
- Technical documentation
- Tools used

**Appendices**
- Appendix A: Complete test dataset
- Appendix B: Raw experimental data
- Appendix C: Code documentation
- Appendix D: User guide

---

## Submission Requirements

### Files to Submit

**1. Source Code**
- `midterm_project_starter.py` (completed)
- `strategy1.py` (if separated)
- `strategy2.py` (if separated)
- `strategy3.py` (if separated)
- `strategy4.py` (if separated)
- `strategy5.py` (if separated)
- `evaluation.py`
- `utils.py`
- `requirements.txt`
- `README.md`

**2. Data Files**
- `test_dataset.json`
- `experiment1_results.csv`
- `experiment2_results.csv`
- `experiment3_results.csv`
- `experiment4_results.csv`
- `raw_data.xlsx` (optional)

**3. Documentation**
- `technical_report.pdf` (15-20 pages)
- `presentation.pdf` (15-20 slides)
- `user_guide.md`
- `API_documentation.md`

**4. Visualizations**
- `speed_comparison.png`
- `quality_radar.png`
- `cost_quality.png`
- `success_rates.png`
- `failure_modes.png`

**5. Demo**
- `demo_video.mp4` (optional, 3-5 min)
- `demo_script.md`

### Submission Format

**Zip file structure:**
```
team_name_midterm_project.zip
├── src/
│   ├── midterm_project_starter.py
│   ├── evaluation.py
│   ├── utils.py
│   └── requirements.txt
├── data/
│   ├── test_dataset.json
│   ├── experiment1_results.csv
│   ├── experiment2_results.csv
│   ├── experiment3_results.csv
│   └── experiment4_results.csv
├── docs/
│   ├── technical_report.pdf
│   ├── presentation.pdf
│   ├── user_guide.md
│   └── API_documentation.md
├── figures/
│   ├── speed_comparison.png
│   ├── quality_radar.png
│   ├── cost_quality.png
│   ├── success_rates.png
│   └── failure_modes.png
├── README.md
└── demo_video.mp4 (optional)
```

---

## Evaluation Rubric

### Implementation (40 points)

| Criteria | Excellent (36-40) | Good (32-35) | Satisfactory (28-31) | Needs Improvement (<28) |
|----------|-------------------|--------------|----------------------|-------------------------|
| **Completeness** | All 5 strategies work flawlessly | 4-5 strategies work with minor issues | 3-4 strategies work | <3 strategies work |
| **Code Quality** | Clean, well-commented, follows best practices | Good structure, some comments | Acceptable structure | Poor organization |
| **Error Handling** | Comprehensive error handling and logging | Good error handling | Basic error handling | Little/no error handling |
| **Interface** | Unified, elegant API | Consistent API | Working API | Inconsistent API |

### Evaluation Framework (30 points)

| Criteria | Excellent (27-30) | Good (24-26) | Satisfactory (21-23) | Needs Improvement (<21) |
|----------|-------------------|--------------|----------------------|-------------------------|
| **Metrics** | All metrics implemented correctly | Most metrics correct | Basic metrics | Incomplete metrics |
| **Experiments** | All 4 experiments, rigorous | All 4 experiments, good | 3 experiments | <3 experiments |
| **Analysis** | Deep statistical analysis | Good statistical tests | Basic analysis | Weak analysis |
| **Visualization** | Excellent charts, professional | Good charts | Basic charts | Poor/no charts |

### Technical Report (20 points)

| Criteria | Excellent (18-20) | Good (16-17) | Satisfactory (14-15) | Needs Improvement (<14) |
|----------|-------------------|--------------|----------------------|-------------------------|
| **Content** | Comprehensive, insightful | Complete, well-written | All sections present | Missing sections |
| **Analysis** | Deep interpretation of results | Good interpretation | Basic interpretation | Weak analysis |
| **Writing** | Clear, professional, no errors | Clear, few errors | Acceptable, some errors | Unclear, many errors |
| **Format** | Perfect formatting, figures | Good formatting | Acceptable formatting | Poor formatting |

### Presentation (10 points)

| Criteria | Excellent (9-10) | Good (8) | Satisfactory (7) | Needs Improvement (<7) |
|----------|-------------------|----------|------------------|------------------------|
| **Clarity** | Very clear and engaging | Clear | Somewhat clear | Unclear |
| **Demo** | Flawless, impressive | Works well | Works | Doesn't work |
| **Q&A** | Excellent answers | Good answers | Acceptable answers | Poor answers |
| **Time** | Perfect timing (15 min) | Within 14-16 min | Within 13-17 min | <13 or >17 min |

---

## Tips for Success

### Technical Tips

1. **Start with Strategy 2 (Deterministic)**
   - We already have the code
   - Adapt it to your interface
   - Use as baseline for comparison

2. **Test Early, Test Often**
   - Test each strategy with simple cases first
   - Don't wait until the end
   - Fix bugs as you go

3. **Use Version Control**
   - Git for collaboration
   - Branch for each strategy
   - Merge when tested

4. **Handle Errors Gracefully**
   - Ollama server might go down
   - Timeouts can happen
   - Add retry logic

5. **Save Everything**
   - Save all experimental data
   - Save intermediate results
   - You might need them later

### Project Management Tips

1. **Daily Stand-ups**
   - 15-minute daily meetings
   - What did you do?
   - What will you do?
   - Any blockers?

2. **Use Project Management Tools**
   - Trello, Asana, or simple checklist
   - Assign tasks clearly
   - Track progress

3. **Communicate Actively**
   - WhatsApp/Slack group
   - Share progress
   - Ask for help early

4. **Divide and Conquer**
   - Work in parallel
   - Clear ownership
   - Integrate frequently

5. **Leave Buffer Time**
   - Things take longer than expected
   - Leave time for debugging
   - Leave time for writing

### Analysis Tips

1. **Collect Rich Data**
   - Not just success/failure
   - Capture all metrics
   - Save intermediate results

2. **Look for Patterns**
   - Which strategy fails on what?
   - Are failures predictable?
   - Can you categorize?

3. **Be Honest**
   - If something doesn't work, say so
   - Negative results are valuable
   - Explain limitations

4. **Compare Fairly**
   - Same test cases for all
   - Same environment
   - Document conditions

5. **Visualize Everything**
   - Tables are good
   - Charts are better
   - Both is best

### Writing Tips

1. **Start Early**
   - Don't wait for all experiments
   - Write methodology as you code
   - Update as you go

2. **Use Templates**
   - IEEE or ACM format
   - LaTeX for professional look
   - Markdown for simplicity

3. **Tell a Story**
   - Motivation → Problem → Solution → Results → Conclusion
   - Clear narrative arc
   - Keep reader engaged

4. **Show, Don't Just Tell**
   - Use examples
   - Include code snippets
   - Add screenshots

5. **Proofread**
   - Grammar and spelling matter
   - Read out loud
   - Have teammate review

---

## Resources

### Technical Resources

**Python Libraries:**
- `requests`: Ollama API calls
- `numpy`: Numerical computations
- `pandas`: Data manipulation
- `matplotlib`: Basic plotting
- `seaborn`: Advanced visualization
- `scipy`: Statistical tests

**Installation:**
```bash
pip install requests numpy pandas matplotlib seaborn scipy
```

### Learning Resources

**Prompt Engineering:**
- [Prompt Engineering Guide](https://www.promptingguide.ai/)
- Few-shot learning examples
- Chain-of-thought prompting

**Statistical Analysis:**
- [SciPy Stats Tutorial](https://docs.scipy.org/doc/scipy/tutorial/stats.html)
- t-tests, ANOVA, chi-square
- Correlation analysis

**Visualization:**
- [Matplotlib Gallery](https://matplotlib.org/stable/gallery/index.html)
- [Seaborn Tutorial](https://seaborn.pydata.org/tutorial.html)

### Writing Resources

**LaTeX Templates:**
- [Overleaf Templates](https://www.overleaf.com/gallery/tagged/academic-journal)
- IEEE Conference Template
- ACM Article Template

**Report Writing:**
- [How to Write a Technical Report](https://www.ece.rice.edu/~mk1/ece580/Technical_Report_Format.pdf)
- [Scientific Writing Guide](https://www.nature.com/scitable/topicpage/effective-writing-13815989/)

---

## Frequently Asked Questions

**Q: Can we use models other than 1.5b and 14b?**
A: Yes, but document your choices and justify them. The comparison should still include at least one small (<3b) and one large (>10b) model.

**Q: What if Ollama server is down during experiments?**
A: Save your data frequently. If server goes down, document it and continue when it's back. You can also simulate results for some strategies if needed (clearly label simulated data).

**Q: Can we implement only 4 strategies instead of 5?**
A: You need at least 4 to get full credit, but 5 is strongly recommended for comprehensive comparison.

**Q: How detailed should code comments be?**
A: Every function should have a docstring. Complex logic should have inline comments. Someone should be able to understand your code without running it.

**Q: Can we work in groups larger than 4?**
A: Not recommended. If you have 5 students, split into 2 groups (3+2) or one student can work independently on a simplified version.

**Q: What programming language must we use?**
A: Python is required for consistency and because the starter code is in Python. Generated questions are about C++ code, but the generator itself is Python.

**Q: Can we use ChatGPT or other AI assistants?**
A: Yes, for learning and debugging, but:
- You must understand all code you submit
- You must cite AI assistance in your report
- The core implementation must be your own work
- Be prepared to explain any code during Q&A

**Q: How long should the final presentation be?**
A: 15 minutes: 10 min presentation + 5 min Q&A. Practice to stay within time.

**Q: Do we need to submit the code for generating questions, or just the framework?**
A: Both. Submit complete working code that can generate questions and run all experiments.

**Q: What if our experiments show that the simplest strategy (pure small model) is best?**
A: That's a valid finding! Explain why, provide evidence, discuss implications. Science is about discovering truth, not confirming hypotheses.

---

## Contact and Support

**Instructor:** [Your Name]
**Email:** [your.email@university.edu]
**Office Hours:** [Days and times]
**Course Website:** [URL]

**Teaching Assistants:**
- TA 1: [name and email]
- TA 2: [name and email]

**Submission Deadline:** [Date and Time]
**Late Policy:** [Your late policy]

**Questions?**
- Post in course forum (preferred)
- Email instructor
- Office hours

---

## Good Luck! 🚀

This is a challenging but rewarding project. You will:
- Learn cutting-edge AI techniques
- Gain experience with LLM optimization
- Develop scientific research skills
- Create something useful

Work hard, communicate often, and have fun!

**Remember:** The goal is not just to complete the project, but to learn and grow as AI engineers and researchers.

---

**Document Version:** 1.0
**Last Updated:** [Date]
**License:** Educational Use Only
