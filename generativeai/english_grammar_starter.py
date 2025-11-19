"""
English Grammar Quiz System - Starter Code
-------------------------------------------
Midterm Project Template for English Grammar Learning

This starter code provides the basic structure for your English grammar quiz system.
Your team should:
1. Design your own grammar topics (minimum 3)
2. Choose your LLM model
3. Implement question generation
4. Add distractor generation
5. Build interactive quiz interface
6. Add progress tracking

Team Members:
1. [Student 1 Name] - Role: [Curriculum Designer]
2. [Student 2 Name] - Role: [LLM Engineer]
3. [Student 3 Name] - Role: [Application Developer]
"""

import requests
import json
import random
import sys
import io
import os
from typing import Dict, List, Optional
from dataclasses import dataclass
from enum import Enum

# Fix encoding for Windows
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "http://localhost:11434"  # Default Ollama URL
MODEL = "qwen2.5:1.5b"  # Change to your chosen model
TIMEOUT = 60
PROGRESS_FILE = "student_grammar_progress.json"


class DifficultyLevel(Enum):
    """Difficulty levels for grammar topics"""
    BEGINNER = 1
    INTERMEDIATE = 2
    ADVANCED = 3


@dataclass
class SpecificationVariation:
    """A specific way to ask for a grammar question"""
    difficulty: DifficultyLevel
    specification: str
    description: str
    min_score: int  # Minimum score to pass


@dataclass
class GrammarTopic:
    """A grammar topic with multiple difficulty variations"""
    id: str
    name: str
    description: str
    base_difficulty: int  # 1-5 stars
    prerequisites: List[str]
    variations: List[SpecificationVariation]

    def get_variations_by_difficulty(self, level: DifficultyLevel) -> List[SpecificationVariation]:
        """Get all variations for a specific difficulty level"""
        return [v for v in self.variations if v.difficulty == level]


class EnglishGrammarCurriculum:
    """
    Example curriculum structure - CUSTOMIZE THIS FOR YOUR PROJECT!

    TODO for your team:
    1. Replace these example topics with your chosen grammar topics
    2. Add more variations (minimum 3 per difficulty level)
    3. Ensure logical progression between topics
    """

    # TODO: Customize these topics for your project!
    TOPICS = [
        GrammarTopic(
            id="G1_01",
            name="Simple Present Tense",
            description="Basic present tense with regular verbs",
            base_difficulty=1,
            prerequisites=[],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a simple present tense sentence with subject 'I' and a daily activity",
                    description="Basic present tense with I",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Generate a present tense sentence with 'He/She' and a hobby",
                    description="Third person singular",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Create a present tense question with 'Do/Does'",
                    description="Present tense questions",
                    min_score=2
                ),
                # TODO: Add more variations!
            ]
        ),

        # TODO: Add your Topic 2 here
        GrammarTopic(
            id="G2_01",
            name="Articles (a/an/the)",
            description="Using articles correctly",
            base_difficulty=2,
            prerequisites=["G1_01"],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a sentence using article 'a' before a consonant",
                    description="Article 'a' usage",
                    min_score=2
                ),
                # TODO: Add more variations!
            ]
        ),

        # TODO: Add your Topic 3 here (minimum requirement)
        # TODO: Add more topics if you want (bonus points!)
    ]

    @classmethod
    def get_all_topics(cls) -> List[GrammarTopic]:
        """Get all topics"""
        return cls.TOPICS

    @classmethod
    def get_topic_by_id(cls, topic_id: str) -> Optional[GrammarTopic]:
        """Get specific topic by ID"""
        for topic in cls.get_all_topics():
            if topic.id == topic_id:
                return topic
        return None


class GrammarDistractorGenerator:
    """
    Generate plausible wrong answers for grammar questions

    TODO for your team:
    1. Add more distractor rules for your chosen topics
    2. Customize based on your grammar topics
    3. Consider using LLM for some distractors (bonus!)
    """

    # TODO: Customize these rules for your grammar topics!
    DISTRACTOR_RULES = {
        # Verb forms
        'go': ['goes', 'going', 'gone'],
        'goes': ['go', 'going', 'went'],
        'is': ['are', 'am', 'was'],
        'are': ['is', 'am', 'were'],

        # Articles
        'a': ['an', 'the', '∅'],
        'an': ['a', 'the', '∅'],
        'the': ['a', 'an', '∅'],

        # Prepositions
        'in': ['on', 'at', 'to'],
        'on': ['in', 'at', 'by'],
        'at': ['in', 'on', 'to'],

        # TODO: Add more rules for your topics!
    }

    @classmethod
    def get_distractors(cls, correct_answer: str, num_distractors: int = 3) -> List[str]:
        """
        Get plausible wrong answers for a correct answer

        Args:
            correct_answer: The correct word/phrase
            num_distractors: Number of wrong options to generate

        Returns:
            List of plausible wrong answers
        """
        # Check if we have pre-defined distractors
        if correct_answer.lower() in cls.DISTRACTOR_RULES:
            return cls.DISTRACTOR_RULES[correct_answer.lower()][:num_distractors]

        # TODO: Add LLM-based distractor generation here (bonus!)
        # For now, return generic distractors
        return [f"option_{i+1}" for i in range(num_distractors)]


class QuestionGenerator:
    """
    Generate grammar questions using small LLM

    TODO for your team:
    1. Choose your generation approach (Two-phase, Full LLM, Hybrid, or Template)
    2. Implement the chosen approach
    3. Add validation for LLM outputs
    4. Handle errors gracefully
    """

    def __init__(self, model: str = MODEL, ollama_url: str = OLLAMA_URL):
        self.model = model
        self.ollama_url = ollama_url

    def call_llm(self, prompt: str) -> Optional[str]:
        """
        Call the LLM via Ollama API

        TODO: Add error handling and retries
        """
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": False
            }

            response = requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                timeout=TIMEOUT
            )
            response.raise_for_status()

            data = response.json()
            return data.get('response', '').strip()

        except Exception as e:
            print(f"❌ Error calling LLM: {e}")
            return None

    def generate_question(self, topic: GrammarTopic, variation: SpecificationVariation) -> Optional[Dict]:
        """
        Generate a fill-in-the-blank question

        TODO for your team:
        Implement ONE of these approaches:

        APPROACH 1: Two-Phase (Recommended)
        - Phase 1: LLM generates complete sentence
        - Phase 2: Deterministically select blank and create distractors

        APPROACH 2: Full LLM
        - LLM generates sentence + blank + distractors in one go
        - Validate and parse output

        APPROACH 3: Hybrid (RAG + Small LLM)
        - Retrieve example sentences
        - LLM adapts with variations
        - Deterministic distractors

        APPROACH 4: Template + LLM
        - Use templates for structure
        - LLM fills variations
        - Rule-based distractors
        """

        # EXAMPLE: Simple two-phase approach
        # Phase 1: Generate sentence from specification
        prompt = f"""Generate a simple English sentence for a grammar quiz.

Topic: {topic.name}
Task: {variation.specification}
Difficulty: {variation.difficulty.name}

Requirements:
- Make it natural and grammatically correct
- Suitable for {variation.difficulty.name} level students
- Keep it clear and simple

Just output the sentence, nothing else:"""

        sentence = self.call_llm(prompt)
        if not sentence:
            return None

        # Phase 2: TODO - Deterministically select blank position
        # For now, this is a placeholder
        # You should implement:
        # 1. Identify key word to blank out (verb, article, preposition, etc.)
        # 2. Create the blank
        # 3. Generate distractors using GrammarDistractorGenerator

        # Placeholder question structure
        question = {
            'topic': topic,
            'variation': variation,
            'sentence': sentence,
            'blank_word': 'TODO',  # TODO: Extract the word to blank out
            'question_text': sentence,  # TODO: Replace word with _____
            'options': ['TODO1', 'TODO2', 'TODO3', 'TODO4'],  # TODO: Create real options
            'correct_index': 0  # TODO: Which option is correct (0-3)
        }

        return question


class StudentProgress:
    """
    Track student progress through topics and difficulty levels

    TODO: This is complete, but you can enhance it with:
    - Time tracking
    - Detailed analytics
    - Achievement badges
    - Learning curve analysis
    """

    def __init__(self, filename: str = PROGRESS_FILE):
        self.filename = filename
        self.progress = self.load_progress()

    def load_progress(self) -> Dict:
        """Load progress from file"""
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except:
                pass
        return {}

    def save_progress(self):
        """Save progress to file"""
        with open(self.filename, 'w') as f:
            json.dump(self.progress, f, indent=2)

    def update_score(self, topic_id: str, difficulty: DifficultyLevel, score: int, total: int):
        """Record a quiz attempt"""
        if topic_id not in self.progress:
            self.progress[topic_id] = {'scores': {}}

        diff_key = difficulty.name
        if diff_key not in self.progress[topic_id]['scores']:
            self.progress[topic_id]['scores'][diff_key] = []

        self.progress[topic_id]['scores'][diff_key].append({
            'score': score,
            'total': total,
            'percentage': (score / total * 100) if total > 0 else 0
        })

        self.save_progress()

    def get_best_score(self, topic_id: str, difficulty: DifficultyLevel) -> Optional[int]:
        """Get best score for a topic/difficulty"""
        if topic_id not in self.progress:
            return None

        diff_key = difficulty.name
        if diff_key not in self.progress[topic_id]['scores']:
            return None

        scores = self.progress[topic_id]['scores'][diff_key]
        return max(s['score'] for s in scores) if scores else None


class GrammarQuizApp:
    """
    Main quiz application

    TODO for your team:
    1. Implement interactive menus
    2. Add question display with clear formatting
    3. Collect and validate user answers
    4. Provide immediate feedback
    5. Show progress reports
    6. (Optional) Add unlocking system
    """

    def __init__(self):
        self.generator = QuestionGenerator()
        self.curriculum = EnglishGrammarCurriculum()
        self.progress = StudentProgress()

    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*80)
        print("🎓 ENGLISH GRAMMAR QUIZ SYSTEM")
        print("="*80)
        print("\nWelcome! This quiz will help you practice English grammar.")
        print("\nFeatures:")
        print("  📚 Multiple grammar topics")
        print("  📈 Progressive difficulty levels")
        print("  💾 Progress tracking")
        print("  ✅ Immediate feedback")
        print("="*80)

    def run_quiz(self):
        """
        Main quiz loop

        TODO: Implement this method with:
        1. Topic selection menu
        2. Difficulty selection
        3. Question generation
        4. Answer collection
        5. Scoring and feedback
        6. Progress updates
        """
        self.display_welcome()

        # TODO: Implement topic selection menu
        # TODO: Implement difficulty selection
        # TODO: Generate and display questions
        # TODO: Collect user answers
        # TODO: Score and provide feedback
        # TODO: Update progress

        print("\n🎉 Quiz completed! Check back later for more practice.")


def main():
    """
    Main entry point

    This starter code is intentionally incomplete!
    Your team needs to:
    1. Complete the TODO items throughout this file
    2. Design your grammar topics and variations
    3. Implement your chosen LLM approach
    4. Build the interactive quiz interface
    5. Add progress tracking features
    6. Test thoroughly and fix bugs
    7. Write documentation
    """

    print("\n" + "="*80)
    print("ENGLISH GRAMMAR QUIZ - STARTER CODE")
    print("="*80)
    print("\n⚠️  This is starter code! You need to implement:")
    print("  1. Your grammar topic selections (minimum 3)")
    print("  2. Specification variations (minimum 3 per difficulty)")
    print("  3. Question generation approach")
    print("  4. Distractor generation logic")
    print("  5. Interactive quiz interface")
    print("  6. Progress tracking display")
    print("  7. Complete documentation")
    print("\n🚀 Good luck with your project!")
    print("="*80 + "\n")

    # Test basic LLM connection
    print("Testing LLM connection...")
    generator = QuestionGenerator()
    test_response = generator.call_llm("Say 'Hello, I am working!'")

    if test_response:
        print(f"✅ LLM is working! Response: {test_response}")
    else:
        print("❌ LLM connection failed. Please check:")
        print("   1. Ollama is running (ollama serve)")
        print("   2. Model is downloaded (ollama pull qwen2.5:1.5b)")
        print("   3. URL is correct (http://localhost:11434)")
        return

    # Test curriculum
    print("\n" + "="*80)
    print("Current Curriculum Topics:")
    print("="*80)
    curriculum = EnglishGrammarCurriculum()
    for topic in curriculum.get_all_topics():
        print(f"\n{topic.id}: {topic.name}")
        print(f"  Difficulty: {'⭐' * topic.base_difficulty}")
        print(f"  Variations: {len(topic.variations)}")
        for level in DifficultyLevel:
            variations = topic.get_variations_by_difficulty(level)
            if variations:
                print(f"    {level.name}: {len(variations)} variations")

    print("\n⚠️  Remember to customize these topics for your project!")
    print("="*80 + "\n")

    # TODO: Uncomment this when quiz is implemented
    # app = GrammarQuizApp()
    # app.run_quiz()


if __name__ == "__main__":
    main()
