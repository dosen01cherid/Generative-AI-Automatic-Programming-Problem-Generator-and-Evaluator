"""
Midterm Project: Small LLM Optimization Framework
--------------------------------------------------
Starter code for comparing 5 strategies of leveraging small LLMs
for educational question generation.

Team Members:
- Student 1: [Name] - Strategies 1 & 3
- Student 2: [Name] - Strategies 4 & 5
- Student 3: [Name] - Evaluation Framework
- Student 4: [Name] - Documentation & Integration

Due Date: [Date]
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Tuple
import time
import json
import requests
from dataclasses import dataclass
from enum import Enum
import sys
import io

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://bye-suites-nsw-some.trycloudflare.com"
SMALL_MODEL = "qwen2.5:1.5b"
LARGE_MODEL = "qwen2.5:14b"
TIMEOUT = 300


@dataclass
class GenerationMetrics:
    """Metrics for a single question generation"""
    time_seconds: float
    tokens_used: int
    api_calls: int
    cost_estimate: float  # Estimated cost in dollars
    success: bool
    error_message: Optional[str] = None


@dataclass
class QualityMetrics:
    """Quality assessment of generated question"""
    format_compliance: float  # 0.0 to 1.0
    consistency: float  # Target matches answer
    distractor_quality: float  # 1-5 scale
    code_correctness: bool
    difficulty_estimate: int  # 1-5 scale


class StrategyType(Enum):
    """Types of generation strategies"""
    PURE_SMALL = "pure_small_model"
    DETERMINISTIC = "deterministic_heavy"
    HYBRID = "hybrid_1_5b_14b"
    SMART_FALLBACK = "smart_fallback"
    PROMPT_ENGINEERING = "prompt_engineering"


class QuestionGenerationStrategy(ABC):
    """
    Abstract base class for question generation strategies.
    All strategies must implement these methods.
    """

    def __init__(self, name: str):
        self.name = name
        self.generation_metrics: List[GenerationMetrics] = []
        self.quality_metrics: List[QualityMetrics] = []

    @abstractmethod
    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        Generate a fill-in-the-blank question.

        Args:
            topic: Description of what to generate (e.g., "for loop example")
            num_blanks: Number of blanks in the question

        Returns:
            Dictionary with:
                - code: Original complete code
                - question_code: Code with blanks
                - sub_questions: List of questions with options
                - metrics: GenerationMetrics object
        """
        pass

    @abstractmethod
    def get_strategy_description(self) -> str:
        """Return a description of this strategy"""
        pass

    def record_metrics(self, gen_metrics: GenerationMetrics, qual_metrics: QualityMetrics):
        """Record metrics for analysis"""
        self.generation_metrics.append(gen_metrics)
        self.quality_metrics.append(qual_metrics)

    def get_average_metrics(self) -> Dict:
        """Calculate average metrics across all generations"""
        if not self.generation_metrics:
            return {}

        total_time = sum(m.time_seconds for m in self.generation_metrics)
        total_tokens = sum(m.tokens_used for m in self.generation_metrics)
        total_cost = sum(m.cost_estimate for m in self.generation_metrics)
        success_count = sum(1 for m in self.generation_metrics if m.success)

        return {
            'avg_time': total_time / len(self.generation_metrics),
            'avg_tokens': total_tokens / len(self.generation_metrics),
            'avg_cost': total_cost / len(self.generation_metrics),
            'success_rate': success_count / len(self.generation_metrics),
            'total_generations': len(self.generation_metrics)
        }


# ============================================================================
# STRATEGY 1: Pure Small Model
# ============================================================================
# Student 1: Implement this strategy

class Strategy1_PureSmallModel(QuestionGenerationStrategy):
    """
    Strategy 1: Use only the small model (1.5b) for everything.

    Approach:
    - Single prompt asks 1.5b to generate code, targets, and distractors
    - No deterministic post-processing
    - Simplest approach, baseline for comparison

    Expected Performance:
    - Speed: Very Fast (~10s)
    - Quality: Acceptable (60-70%)
    - Cost: Very Low

    TODO for Student 1:
    1. Design prompt that asks 1.5b to generate everything
    2. Implement parsing of 1.5b output
    3. Handle format inconsistencies
    4. Measure metrics (time, tokens, success rate)
    """

    def __init__(self):
        super().__init__("Pure Small Model (1.5b)")
        self.model = SMALL_MODEL
        self.ollama_url = OLLAMA_URL

    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        TODO: Implement pure small model generation

        Steps:
        1. Create comprehensive prompt for 1.5b
        2. Call Ollama API
        3. Parse response (handle errors)
        4. Create question structure
        5. Record metrics
        """

        # TODO: Your implementation here
        start_time = time.time()

        # Example prompt structure (customize this):
        prompt = f"""Generate a C++ fill-in-the-blank question for: {topic}

OUTPUT FORMAT:

CODE:
```cpp
[complete code here]
```

TARGETS (what to blank out):
1. [target 1]
2. [target 2]
3. [target 3]

DISTRACTORS:
For Target 1:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]

For Target 2:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]

For Target 3:
1. [wrong option 1]
2. [wrong option 2]
3. [wrong option 3]
"""

        # TODO: Call Ollama API with this prompt
        # TODO: Parse response
        # TODO: Create question structure
        # TODO: Calculate metrics

        elapsed_time = time.time() - start_time

        # Placeholder - replace with actual implementation
        return None

    def get_strategy_description(self) -> str:
        return """
        Pure Small Model Strategy:
        - Uses qwen2.5:1.5b for all tasks
        - Single prompt generation
        - No post-processing
        - Fastest but least reliable
        """


# ============================================================================
# STRATEGY 2: Deterministic Heavy
# ============================================================================
# Student 1: Adapt our existing code (genai_ollama_rag_deterministic_1_5b.py)

class Strategy2_DeterministicHeavy(QuestionGenerationStrategy):
    """
    Strategy 2: Small model + heavy deterministic processing.

    This is our current approach - adapt the code from:
    genai_ollama_rag_deterministic_1_5b.py

    Expected Performance:
    - Speed: Fast (~8s)
    - Quality: Good (85-90%)
    - Cost: Very Low

    TODO for Student 1:
    1. Copy CppTokenExtractor from our deterministic code
    2. Copy deterministic question generation logic
    3. Wrap it in this interface
    4. Ensure metrics are captured
    """

    def __init__(self):
        super().__init__("Deterministic Heavy")
        # TODO: Initialize CppTokenExtractor and other components

    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        TODO: Implement deterministic heavy approach

        Steps:
        1. Use 1.5b to generate code only
        2. Use CppTokenExtractor to find all tokens
        3. Score and select best targets
        4. Generate distractors from templates
        5. Create question deterministically
        6. Record metrics
        """
        # TODO: Adapt code from genai_ollama_rag_deterministic_1_5b.py
        return None

    def get_strategy_description(self) -> str:
        return """
        Deterministic Heavy Strategy:
        - 1.5b generates code only (5% AI)
        - Pattern matching extracts tokens (95% deterministic)
        - Rule-based target selection
        - Template-based distractors
        - 100% consistent replacement
        """


# ============================================================================
# STRATEGY 3: Hybrid (1.5b + 14b)
# ============================================================================
# Student 1: Implement hybrid approach

class Strategy3_Hybrid(QuestionGenerationStrategy):
    """
    Strategy 3: Use 1.5b for speed, 14b for quality.

    Approach:
    - Phase 1: 1.5b generates code quickly
    - Phase 2: 14b validates and extracts targets/distractors

    Expected Performance:
    - Speed: Medium (~25s)
    - Quality: Very Good (90-95%)
    - Cost: Medium

    TODO for Student 1:
    1. Implement two-phase generation
    2. 1.5b generates code
    3. 14b validates and structures
    4. Measure metrics for both phases
    """

    def __init__(self):
        super().__init__("Hybrid (1.5b + 14b)")
        self.fast_model = SMALL_MODEL
        self.quality_model = LARGE_MODEL

    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        TODO: Implement hybrid generation

        Steps:
        1. Phase 1: Call 1.5b for code generation
        2. Phase 2: Call 14b for target extraction and validation
        3. Combine results
        4. Record metrics (sum of both phases)
        """
        # TODO: Your implementation here
        return None

    def get_strategy_description(self) -> str:
        return """
        Hybrid Strategy:
        - 1.5b: Fast code generation (~10s)
        - 14b: Quality validation (~15s)
        - Best of both worlds
        - Moderate cost
        """


# ============================================================================
# STRATEGY 4: Smart Fallback
# ============================================================================
# Student 2: Implement adaptive fallback

class Strategy4_SmartFallback(QuestionGenerationStrategy):
    """
    Strategy 4: Adaptive approach with quality threshold.

    Approach:
    - Try deterministic (fast) first
    - Check quality
    - If quality < threshold, retry with 14b
    - Learn optimal threshold over time

    Expected Performance:
    - Speed: Variable (8-25s avg)
    - Quality: Good (85-92%)
    - Cost: Low-Medium

    TODO for Student 2:
    1. Implement quality checker
    2. Implement fallback logic
    3. Track success rates
    4. Optimize threshold
    """

    def __init__(self, quality_threshold: float = 0.7):
        super().__init__("Smart Fallback")
        self.quality_threshold = quality_threshold
        self.fallback_count = 0
        self.total_attempts = 0

        # Initialize both strategies
        self.fast_strategy = Strategy2_DeterministicHeavy()
        self.fallback_strategy = Strategy3_Hybrid()

    def check_quality(self, result: Dict) -> float:
        """
        TODO: Implement quality checker

        Check if the generated question meets quality standards:
        - All targets exist in code
        - All distractors are valid
        - Proper format
        - Return quality score 0.0-1.0
        """
        # TODO: Your implementation here
        return 1.0  # Placeholder

    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        TODO: Implement smart fallback generation

        Steps:
        1. Try fast strategy first
        2. Check quality
        3. If quality < threshold, use fallback strategy
        4. Record which strategy was used
        5. Update metrics
        """
        self.total_attempts += 1

        # TODO: Your implementation here

        return None

    def get_fallback_rate(self) -> float:
        """Return percentage of generations that needed fallback"""
        if self.total_attempts == 0:
            return 0.0
        return self.fallback_count / self.total_attempts

    def get_strategy_description(self) -> str:
        return f"""
        Smart Fallback Strategy:
        - Try deterministic first (fast)
        - Quality check (threshold: {self.quality_threshold})
        - Fallback to 14b if needed
        - Current fallback rate: {self.get_fallback_rate():.1%}
        """


# ============================================================================
# STRATEGY 5: Prompt Engineering
# ============================================================================
# Student 2: Implement advanced prompting for small model

class Strategy5_PromptEngineering(QuestionGenerationStrategy):
    """
    Strategy 5: Enhanced prompting techniques for small model.

    Techniques:
    - Few-shot examples
    - Chain-of-thought
    - Step-by-step decomposition
    - Template constraints

    Expected Performance:
    - Speed: Medium (~15s)
    - Quality: Good (75-85%)
    - Cost: Low

    TODO for Student 2:
    1. Design few-shot examples
    2. Implement chain-of-thought prompting
    3. Test different prompt templates
    4. Find best prompt structure
    """

    def __init__(self):
        super().__init__("Prompt Engineering")
        self.model = SMALL_MODEL
        self.few_shot_examples = self.load_few_shot_examples()

    def load_few_shot_examples(self) -> List[str]:
        """
        TODO: Create 3-5 high-quality examples to include in prompt

        These examples show the model exactly what output format we want.
        """
        examples = [
            # TODO: Add few-shot examples
            # Example format:
            """Example 1:
CODE:
```cpp
int main() {
    for(int i = 0; i < 5; i++) {
        cout << i << endl;
    }
    return 0;
}
```
TARGET: for
DISTRACTORS: while, do, if
""",
            # Add more examples...
        ]
        return examples

    def create_enhanced_prompt(self, topic: str, num_blanks: int) -> str:
        """
        TODO: Create enhanced prompt with multiple techniques

        Include:
        1. Few-shot examples
        2. Step-by-step instructions
        3. Clear format constraints
        4. Chain-of-thought reasoning
        """

        # TODO: Build comprehensive prompt
        prompt = f"""You are an expert C++ programming teacher creating fill-in-the-blank questions.

EXAMPLES OF GOOD QUESTIONS:
{self.few_shot_examples[0]}

NOW CREATE A SIMILAR QUESTION FOR: {topic}

Think step by step:
1. First, write complete C++ code for {topic}
2. Then, identify the {num_blanks} most important keywords to test
3. For each keyword, think of 3 similar but wrong alternatives
4. Finally, format your answer exactly like the examples above

Your answer:
"""
        return prompt

    def generate_question(self, topic: str, num_blanks: int = 3) -> Optional[Dict]:
        """
        TODO: Implement prompt engineering generation

        Steps:
        1. Create enhanced prompt with few-shot examples
        2. Call 1.5b with enhanced prompt
        3. Parse response (should be better formatted)
        4. Record metrics
        """
        # TODO: Your implementation here
        return None

    def get_strategy_description(self) -> str:
        return """
        Prompt Engineering Strategy:
        - Few-shot learning (3-5 examples)
        - Chain-of-thought prompting
        - Step-by-step instructions
        - Template constraints
        - Enhanced 1.5b performance
        """


# ============================================================================
# EVALUATION FRAMEWORK
# ============================================================================
# Student 3: Implement comprehensive evaluation

class EvaluationFramework:
    """
    Comprehensive evaluation framework for comparing strategies.

    TODO for Student 3:
    1. Implement automated quality assessment
    2. Run batch experiments
    3. Statistical analysis
    4. Visualization
    """

    def __init__(self, strategies: List[QuestionGenerationStrategy]):
        self.strategies = strategies
        self.results = {}

    def evaluate_single_question(self, result: Dict) -> QualityMetrics:
        """
        TODO: Implement automated quality evaluation

        Metrics to calculate:
        1. Format compliance: Does output match expected format?
        2. Consistency: Do targets actually exist in code?
        3. Distractor quality: Are distractors plausible? (1-5 scale)
        4. Code correctness: Can we compile/analyze the code?
        5. Difficulty: Estimate question difficulty (1-5 scale)
        """

        # TODO: Implement quality checks

        # Placeholder
        return QualityMetrics(
            format_compliance=1.0,
            consistency=1.0,
            distractor_quality=4.0,
            code_correctness=True,
            difficulty_estimate=3
        )

    def run_speed_comparison(self, test_cases: List[str]) -> Dict:
        """
        TODO: Run Experiment 1 - Speed Comparison

        For each strategy:
        1. Generate questions for all test cases
        2. Measure total time, average time
        3. Calculate variance
        4. Create comparison chart
        """
        print("\n" + "="*60)
        print("EXPERIMENT 1: Speed Comparison")
        print("="*60)

        # TODO: Your implementation here

        return {}

    def run_quality_comparison(self, test_cases: List[str]) -> Dict:
        """
        TODO: Run Experiment 2 - Quality Comparison

        For each strategy:
        1. Generate questions
        2. Automated quality assessment
        3. Manual quality review (optional)
        4. Calculate average quality scores
        """
        print("\n" + "="*60)
        print("EXPERIMENT 2: Quality Comparison")
        print("="*60)

        # TODO: Your implementation here

        return {}

    def run_cost_analysis(self) -> Dict:
        """
        TODO: Run Experiment 3 - Cost-Quality Trade-off

        1. Plot cost vs quality for each strategy
        2. Identify Pareto frontier
        3. Recommend best strategy for different budgets
        """
        print("\n" + "="*60)
        print("EXPERIMENT 3: Cost-Quality Trade-off")
        print("="*60)

        # TODO: Your implementation here

        return {}

    def run_failure_analysis(self, edge_cases: List[str]) -> Dict:
        """
        TODO: Run Experiment 4 - Failure Analysis

        Test with edge cases:
        - Very simple (e.g., "hello world")
        - Very complex (e.g., "template metaprogramming")
        - Ambiguous (e.g., "sorting")

        Measure failure rates and analyze failure modes
        """
        print("\n" + "="*60)
        print("EXPERIMENT 4: Failure Analysis")
        print("="*60)

        # TODO: Your implementation here

        return {}

    def generate_report(self, output_file: str = "evaluation_report.md"):
        """
        TODO: Generate comprehensive comparison report

        Include:
        1. Summary statistics table
        2. Performance charts
        3. Quality comparison
        4. Cost analysis
        5. Recommendations
        """

        # TODO: Create markdown report

        pass

    def visualize_results(self):
        """
        TODO: Create visualizations

        Charts to create:
        1. Speed comparison (bar chart)
        2. Quality comparison (radar chart)
        3. Cost vs Quality (scatter plot)
        4. Success rate (bar chart)
        5. Failure mode analysis (pie chart)

        Use matplotlib/seaborn
        """

        # TODO: Create visualizations

        pass


# ============================================================================
# TEST DATASET
# ============================================================================

class TestDataset:
    """
    Predefined test cases for evaluation.

    TODO for Student 3:
    1. Expand to 50+ test cases
    2. Categorize by difficulty
    3. Add edge cases
    """

    @staticmethod
    def get_simple_cases() -> List[str]:
        """Simple programming concepts (20 cases)"""
        return [
            "Simple for loop from 0 to 5",
            "Print hello world",
            "Declare an integer variable",
            "If statement checking if number is positive",
            "While loop counting to 10",
            # TODO: Add 15 more simple cases
        ]

    @staticmethod
    def get_medium_cases() -> List[str]:
        """Medium difficulty concepts (20 cases)"""
        return [
            "Vector with push_back operations",
            "Class with constructor and methods",
            "Function with parameters and return value",
            "Array iteration with for loop",
            "String manipulation with substr",
            # TODO: Add 15 more medium cases
        ]

    @staticmethod
    def get_hard_cases() -> List[str]:
        """Hard concepts (10 cases)"""
        return [
            "Template function for generic sorting",
            "STL algorithm usage with lambda",
            "Smart pointer example with unique_ptr",
            "Exception handling with try-catch",
            "File I/O with ifstream",
            # TODO: Add 5 more hard cases
        ]

    @staticmethod
    def get_edge_cases() -> List[str]:
        """Edge cases for failure analysis"""
        return [
            "Empty main function",
            "Very complex template metaprogramming",
            "Just a single cout statement",
            "Nested templates with multiple parameters",
            "Ambiguous: sorting (many ways to implement)",
        ]

    @staticmethod
    def get_all_cases() -> List[str]:
        """All test cases combined"""
        return (
            TestDataset.get_simple_cases() +
            TestDataset.get_medium_cases() +
            TestDataset.get_hard_cases()
        )


# ============================================================================
# MAIN - EXAMPLE USAGE
# ============================================================================

def main():
    """
    Example usage and testing.

    TODO for Student 4:
    1. Create user-friendly interface
    2. Add command-line arguments
    3. Coordinate integration
    """

    print("="*60)
    print("Small LLM Optimization Framework - Midterm Project")
    print("="*60)

    # Initialize all strategies
    strategies = [
        Strategy1_PureSmallModel(),
        Strategy2_DeterministicHeavy(),
        Strategy3_Hybrid(),
        Strategy4_SmartFallback(),
        Strategy5_PromptEngineering(),
    ]

    # Test each strategy with a simple case
    test_topic = "Simple for loop from 0 to 5"

    print(f"\nTesting all strategies with: '{test_topic}'")
    print("="*60)

    for strategy in strategies:
        print(f"\n{strategy.name}:")
        print(strategy.get_strategy_description())

        # TODO: Uncomment when strategies are implemented
        # result = strategy.generate_question(test_topic, num_blanks=3)
        # if result:
        #     print(f"✅ Success in {result['metrics'].time_seconds:.2f}s")
        # else:
        #     print("❌ Failed")

    # Run full evaluation
    print("\n" + "="*60)
    print("Running Full Evaluation")
    print("="*60)

    evaluator = EvaluationFramework(strategies)

    # TODO: Uncomment when ready to run experiments
    # test_cases = TestDataset.get_all_cases()
    # evaluator.run_speed_comparison(test_cases)
    # evaluator.run_quality_comparison(test_cases[:30])
    # evaluator.run_cost_analysis()
    # evaluator.run_failure_analysis(TestDataset.get_edge_cases())
    # evaluator.generate_report()
    # evaluator.visualize_results()

    print("\n" + "="*60)
    print("Project Template Ready!")
    print("="*60)
    print("\nNext Steps:")
    print("1. Student 1: Implement Strategies 1, 2, 3")
    print("2. Student 2: Implement Strategies 4, 5")
    print("3. Student 3: Complete evaluation framework")
    print("4. Student 4: Integration and documentation")
    print("\nGood luck! 🚀")


if __name__ == "__main__":
    main()
