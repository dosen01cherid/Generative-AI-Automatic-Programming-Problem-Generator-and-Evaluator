"""
Interactive C++ Quiz Application - 14b Model
---------------------------------------------
Uses qwen2.5:14b for high-quality question generation.
Follows curriculum progression and tracks student scores.

Usage: python quiz_app_14b.py [--level 1-10] [--questions 5]
"""

import requests
import json
import time
import re
import random
import sys
import io
import argparse
import os
from typing import Dict, List, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from curriculum.cpp_curriculum_progression import CppCurriculum, Topic

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://unpatented-saylor-nonirate.ngrok-free.dev"
MODEL = "qwen2.5:14b"
TIMEOUT = 300
KEEP_ALIVE = "60m"


class QuestionGenerator14b:
    """Generate questions using 14b model with validation"""

    def __init__(self):
        self.model = MODEL
        self.ollama_url = OLLAMA_URL

    def call_ollama(self, prompt: str, verbose: bool = False) -> Optional[str]:
        """Call Ollama API"""
        try:
            payload = {
                "model": self.model,
                "prompt": prompt,
                "stream": True,
                "keep_alive": KEEP_ALIVE
            }

            response_text = ""
            with requests.post(
                f"{self.ollama_url}/api/generate",
                json=payload,
                stream=True,
                timeout=TIMEOUT
            ) as r:
                r.raise_for_status()

                for line in r.iter_lines(decode_unicode=True):
                    if not line or not line.strip():
                        continue

                    try:
                        data = json.loads(line)
                        if "response" in data:
                            chunk = data["response"]
                            if verbose:
                                print(chunk, end='', flush=True)
                            response_text += chunk
                    except json.JSONDecodeError:
                        continue

            if verbose:
                print()
            return response_text.strip()

        except Exception as e:
            print(f"❌ Error calling Ollama: {e}")
            return None

    def generate_question(self, topic: Topic, num_blanks: int = 3, verbose: bool = False) -> Optional[Dict]:
        """Generate a validated question from topic"""

        # Pick random example from topic
        example_prompt = random.choice(topic.examples)

        prompt = f"""Create a C++ fill-in-the-blank question for: {example_prompt}

Topic: {topic.name}
Description: {topic.description}
Difficulty: {topic.difficulty}/5

Generate in this EXACT format:

CODE:
```cpp
[complete, working C++ code here]
```

TARGETS (keywords to blank out, exactly {num_blanks}):
1. [keyword 1]
2. [keyword 2]
3. [keyword 3]

DISTRACTORS (3 wrong options for each target):
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

IMPORTANT:
- Each TARGET must appear EXACTLY in the CODE
- DISTRACTORS must be similar but wrong
- Use modern C++ (C++11+)
"""

        if verbose:
            print(f"\n⏳ Generating question for: {topic.name}...")

        response = self.call_ollama(prompt, verbose=False)

        if not response:
            return None

        # Parse response
        parsed = self.parse_response(response)
        if not parsed:
            return None

        # Create validated question
        return self.create_validated_question(parsed, topic)

    def parse_response(self, response: str) -> Optional[Dict]:
        """Parse 14b model response"""
        try:
            # Extract CODE
            code_match = re.search(r'CODE:\s*```(?:cpp)?\s*(.*?)\s*```', response, re.DOTALL | re.IGNORECASE)
            if not code_match:
                return None
            code = code_match.group(1).strip()

            # Extract TARGETS
            targets_match = re.search(r'TARGETS?.*?:\s*(.*?)(?=DISTRACTORS?:)', response, re.DOTALL | re.IGNORECASE)
            if not targets_match:
                return None

            targets = []
            for line in targets_match.group(1).split('\n'):
                match = re.match(r'\d+\.\s*(.+)', line.strip())
                if match:
                    targets.append(match.group(1).strip())

            # Extract DISTRACTORS
            distractors_match = re.search(r'DISTRACTORS?:\s*(.*?)$', response, re.DOTALL | re.IGNORECASE)
            if not distractors_match:
                return None

            all_distractors = []
            distractor_text = distractors_match.group(1)
            sections = re.split(r'For Target \d+:', distractor_text, flags=re.IGNORECASE)

            for section in sections[1:]:  # Skip first empty section
                target_distractors = []
                for line in section.split('\n'):
                    match = re.match(r'\d+\.\s*(.+)', line.strip())
                    if match:
                        target_distractors.append(match.group(1).strip())
                if target_distractors:
                    all_distractors.append(target_distractors[:3])

            return {
                'code': code,
                'targets': targets,
                'distractors': all_distractors
            }

        except Exception as e:
            print(f"⚠️  Parse error: {e}")
            return None

    def create_validated_question(self, parsed: Dict, topic: Topic) -> Optional[Dict]:
        """Create validated question with numbered blanks"""

        code = parsed['code']
        targets = parsed['targets']
        all_distractors = parsed['distractors']

        # Validate targets exist in code
        validated_targets = []
        validated_distractors = []

        for target, distractors in zip(targets, all_distractors):
            if target in code:
                validated_targets.append(target)
                validated_distractors.append(distractors)

        if not validated_targets:
            return None

        # Create question code with numbered blanks
        question_code = code
        for i, target in enumerate(validated_targets):
            blank = f"_____({i+1})_____"
            question_code = question_code.replace(target, blank, 1)

        # Create sub-questions
        sub_questions = []
        for i, (target, distractors) in enumerate(zip(validated_targets, validated_distractors)):
            options = [target] + distractors[:3]
            random.shuffle(options)

            answer_pos = options.index(target) + 1

            sub_questions.append({
                'number': i + 1,
                'target': target,
                'options': options,
                'answer': answer_pos,
                'user_answer': None
            })

        return {
            'topic': topic,
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions
        }


class QuizApp:
    """Interactive quiz application"""

    def __init__(self):
        self.generator = QuestionGenerator14b()
        self.curriculum = CppCurriculum()
        self.questions = []
        self.score = 0
        self.total_questions = 0

    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*80)
        print("🎓 C++ PROGRAMMING QUIZ - Powered by 14b Model")
        print("="*80)
        print("\nWelcome to the interactive C++ programming quiz!")
        print("Answer fill-in-the-blank questions to test your knowledge.")
        print("\nFeatures:")
        print("  • Progressive curriculum (Beginner → Advanced)")
        print("  • High-quality questions from 14b model")
        print("  • Instant feedback and scoring")
        print("  • Track your progress")
        print("="*80)

    def display_topic_info(self, topic: Topic):
        """Display topic information"""
        print(f"\n{'='*80}")
        print(f"📚 Topic: {topic.name}")
        print(f"{'='*80}")
        print(f"Description: {topic.description}")
        print(f"Difficulty: {'⭐' * topic.difficulty} ({topic.difficulty}/5)")
        if topic.prerequisites:
            print(f"Prerequisites: {', '.join(topic.prerequisites)}")
        print("="*80)

    def display_question(self, question: Dict, question_num: int, total: int):
        """Display a question"""
        print(f"\n{'='*80}")
        print(f"Question {question_num}/{total}")
        print(f"{'='*80}")
        print("\nComplete Code:")
        print("```cpp")
        print(question['code'])
        print("```")
        print("\nFill in the blanks:")
        print("```cpp")
        print(question['question_code'])
        print("```")

    def ask_question(self, question: Dict) -> int:
        """Ask all sub-questions and return score"""
        score = 0

        for sq in question['sub_questions']:
            print(f"\n--- Blank {sq['number']} ---")
            print("Options:")
            for i, option in enumerate(sq['options'], 1):
                print(f"  {i}. {option}")

            # Get user answer
            while True:
                try:
                    answer = input(f"\nYour answer (1-{len(sq['options'])}): ").strip()
                    answer_num = int(answer)
                    if 1 <= answer_num <= len(sq['options']):
                        sq['user_answer'] = answer_num
                        break
                    else:
                        print(f"Please enter a number between 1 and {len(sq['options'])}")
                except ValueError:
                    print("Please enter a valid number")
                except KeyboardInterrupt:
                    print("\n\nQuiz interrupted by user.")
                    return score

            # Check answer
            if sq['user_answer'] == sq['answer']:
                print("✅ Correct!")
                score += 1
            else:
                correct_option = sq['options'][sq['answer'] - 1]
                user_option = sq['options'][sq['user_answer'] - 1]
                print(f"❌ Incorrect. You answered: {user_option}")
                print(f"   Correct answer: {correct_option}")

        return score

    def display_question_summary(self, question: Dict, score: int, total: int):
        """Display summary for this question"""
        percentage = (score / total * 100) if total > 0 else 0
        print(f"\n{'='*80}")
        print(f"Question Score: {score}/{total} ({percentage:.1f}%)")
        print(f"{'='*80}")

    def display_final_results(self):
        """Display final quiz results"""
        print(f"\n{'='*80}")
        print("🏆 QUIZ COMPLETE!")
        print(f"{'='*80}")
        print(f"\nFinal Score: {self.score}/{self.total_questions}")
        percentage = (self.score / self.total_questions * 100) if self.total_questions > 0 else 0
        print(f"Percentage: {percentage:.1f}%")

        # Grade
        if percentage >= 90:
            grade = "A (Excellent!)"
            emoji = "🌟"
        elif percentage >= 80:
            grade = "B (Good!)"
            emoji = "😊"
        elif percentage >= 70:
            grade = "C (Fair)"
            emoji = "🙂"
        elif percentage >= 60:
            grade = "D (Needs Improvement)"
            emoji = "😐"
        else:
            grade = "F (Keep Practicing)"
            emoji = "📚"

        print(f"Grade: {grade} {emoji}")
        print(f"{'='*80}")

        # Detailed breakdown
        print("\nDetailed Results:")
        for i, q in enumerate(self.questions, 1):
            topic = q['topic']
            correct = sum(1 for sq in q['sub_questions'] if sq['user_answer'] == sq['answer'])
            total = len(q['sub_questions'])
            status = "✅" if correct == total else "❌" if correct == 0 else "⚠️"
            print(f"  {status} Q{i}: {topic.name} - {correct}/{total}")

    def run_quiz(self, level: int = 1, num_questions: int = 5):
        """Run the quiz"""
        self.display_welcome()

        # Get topics for this level
        topics = self.curriculum.get_by_level(level)

        if not topics:
            print(f"❌ Invalid level: {level}. Please choose 1-10.")
            return

        print(f"\n📖 Level {level} Topics:")
        for topic in topics:
            print(f"  • {topic.name}")

        # Generate questions
        print(f"\n⏳ Generating {num_questions} questions...")
        print("This may take a few minutes with the 14b model...\n")

        selected_topics = random.sample(topics, min(num_questions, len(topics)))

        for i, topic in enumerate(selected_topics, 1):
            print(f"[{i}/{len(selected_topics)}] Generating: {topic.name}...", end=' ')
            question = self.generator.generate_question(topic, num_blanks=3, verbose=False)

            if question:
                self.questions.append(question)
                print("✅")
            else:
                print("❌ Failed")

        if not self.questions:
            print("\n❌ Failed to generate any questions. Please try again.")
            return

        print(f"\n✅ Generated {len(self.questions)} questions successfully!")
        input("\nPress Enter to start the quiz...")

        # Run quiz
        for i, question in enumerate(self.questions, 1):
            self.display_topic_info(question['topic'])
            self.display_question(question, i, len(self.questions))

            num_blanks = len(question['sub_questions'])
            q_score = self.ask_question(question)

            self.score += q_score
            self.total_questions += num_blanks

            self.display_question_summary(question, q_score, num_blanks)

            if i < len(self.questions):
                input("\nPress Enter for next question...")

        # Final results
        self.display_final_results()


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Interactive C++ Quiz with 14b Model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quiz_app_14b.py                    # Default: Level 1, 5 questions
  python quiz_app_14b.py --level 3          # Level 3 (Loops), 5 questions
  python quiz_app_14b.py --level 5 --questions 10  # Level 5, 10 questions
  python quiz_app_14b.py --level 8 --questions 3   # Level 8 (Classes), 3 questions

Curriculum Levels:
  Level 1: Basics (Hello World, Variables, I/O)
  Level 2: Control Flow (If, Switch, Boolean)
  Level 3: Loops (For, While, Nested)
  Level 4: Functions (Parameters, Overloading)
  Level 5: Arrays (Declaration, Iteration, Search)
  Level 6: Strings (Operations, Algorithms)
  Level 7: Vectors (STL Container)
  Level 8: Classes (OOP Basics)
  Level 9: Advanced Containers (Map, Set, Queue, Stack)
  Level 10: Advanced Topics (Pointers, Files, Templates)
        """
    )

    parser.add_argument(
        '--level', '-l',
        type=int,
        default=1,
        choices=range(1, 11),
        help='Curriculum level (1-10, default: 1)'
    )

    parser.add_argument(
        '--questions', '-q',
        type=int,
        default=5,
        help='Number of questions (default: 5)'
    )

    args = parser.parse_args()

    # Run quiz
    app = QuizApp()
    try:
        app.run_quiz(level=args.level, num_questions=args.questions)
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")


if __name__ == "__main__":
    main()
