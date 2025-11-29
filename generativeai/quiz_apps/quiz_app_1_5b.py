"""
Interactive C++ Quiz Application - 1.5b Model (Deterministic)
--------------------------------------------------------------
Uses qwen2.5:1.5b with deterministic processing for fast generation.
Follows curriculum progression and tracks student scores.

Usage: python quiz_app_1_5b.py [--level 1-10] [--questions 5]
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
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))
from curriculum.cpp_curriculum_progression import CppCurriculum, Topic

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://unpatented-saylor-nonirate.ngrok-free.dev"
MODEL = "qwen2.5:1.5b"
TIMEOUT = 300
KEEP_ALIVE = "60m"


class CppTokenExtractor:
    """Deterministic token extraction (same as our previous implementation)"""

    KEYWORDS = {
        'types': ['int', 'float', 'double', 'char', 'bool', 'void', 'string', 'auto', 'long', 'short'],
        'control': ['if', 'else', 'for', 'while', 'do', 'switch', 'case', 'break', 'continue', 'return'],
        'container': ['vector', 'map', 'set', 'list', 'queue', 'stack', 'array', 'deque', 'pair'],
        'method': ['push_back', 'pop_back', 'push', 'pop', 'insert', 'erase', 'clear', 'size', 'empty',
                   'front', 'back', 'begin', 'end', 'find', 'count'],
        'stream': ['cout', 'cin', 'endl', 'cerr', 'getline'],
        'keyword': ['namespace', 'using', 'class', 'struct', 'public', 'private', 'protected',
                    'const', 'static', 'virtual', 'new', 'delete'],
        'operator': ['++', '--', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>', '+=', '-='],
        'include': ['#include', 'iostream', 'vector', 'string', 'algorithm', 'cmath', 'fstream'],
    }

    PRIORITY = {
        'control': 10,
        'types': 9,
        'container': 8,
        'method': 7,
        'stream': 6,
        'keyword': 5,
        'include': 4,
        'operator': 2,
    }

    DISTRACTORS = {
        # Control flow
        'for': ['while', 'do', 'if'],
        'while': ['for', 'do', 'if'],
        'if': ['while', 'for', 'switch'],
        'else': ['elif', 'otherwise', 'then'],
        'switch': ['if', 'select', 'case'],
        'return': ['exit', 'end', 'yield'],
        'break': ['continue', 'exit', 'stop'],
        'continue': ['break', 'skip', 'next'],

        # Types
        'int': ['float', 'double', 'char'],
        'float': ['double', 'int', 'long'],
        'double': ['float', 'long', 'decimal'],
        'char': ['int', 'string', 'byte'],
        'bool': ['int', 'boolean', 'flag'],
        'void': ['int', 'null', 'none'],
        'string': ['char', 'text', 'str'],
        'auto': ['var', 'type', 'dynamic'],

        # Containers
        'vector': ['array', 'list', 'deque'],
        'map': ['dict', 'hashmap', 'table'],
        'set': ['list', 'array', 'collection'],
        'list': ['vector', 'array', 'deque'],
        'queue': ['stack', 'list', 'deque'],
        'stack': ['queue', 'list', 'array'],

        # Methods
        'push_back': ['insert', 'add', 'append'],
        'pop_back': ['remove', 'delete', 'pop'],
        'push': ['add', 'insert', 'append'],
        'pop': ['remove', 'delete', 'pop_back'],
        'insert': ['add', 'push', 'append'],
        'erase': ['remove', 'delete', 'clear'],
        'size': ['length', 'count', 'capacity'],
        'empty': ['isEmpty', 'null', 'zero'],
        'clear': ['erase', 'delete', 'remove'],

        # Stream
        'cout': ['cin', 'print', 'output'],
        'cin': ['cout', 'input', 'scanf'],
        'endl': ['newline', '\\n', 'end'],
        'getline': ['readline', 'gets', 'input'],

        # Keywords
        'namespace': ['package', 'module', 'scope'],
        'using': ['import', 'include', 'require'],
        'class': ['struct', 'type', 'object'],
        'public': ['private', 'protected', 'visible'],
        'const': ['final', 'readonly', 'static'],
        'static': ['const', 'final', 'global'],

        # Include
        '#include': ['#import', '#using', 'import'],
        'iostream': ['stdio', 'stream', 'io'],
        'vector': ['array', 'list', 'container'],
        'string': ['text', 'str', 'char'],

        # Operators
        '++': ['--', '+=', '+1'],
        '--': ['++', '-=', '-1'],
        '<<': ['>>', '<', '<<<'],
        '>>': ['<<', '>', '>>>'],
        '==': ['!=', '=', '==='],
        '!=': ['==', '<>', '!=='],
    }

    @staticmethod
    def extract_all_tokens(code: str) -> List[Dict]:
        """Extract all tokens from code"""
        tokens = []
        seen = set()

        for category, keywords in CppTokenExtractor.KEYWORDS.items():
            for keyword in keywords:
                # Create pattern
                if keyword in ['++', '--', '==', '!=', '<=', '>=', '&&', '||', '<<', '>>', '+=', '-=']:
                    pattern = re.escape(keyword)
                elif keyword.startswith('#'):
                    pattern = re.escape(keyword)
                else:
                    pattern = r'\b' + re.escape(keyword) + r'\b'

                for match in re.finditer(pattern, code):
                    token_key = f"{keyword}_{match.start()}"
                    if token_key not in seen:
                        tokens.append({
                            'token': keyword,
                            'category': category,
                            'position': match.start()
                        })
                        seen.add(token_key)

        tokens.sort(key=lambda x: x['position'])
        return tokens

    @staticmethod
    def select_best_targets(tokens: List[Dict], num_targets: int = 3) -> List[str]:
        """Select best targets using scoring"""
        if not tokens:
            return []

        scored_tokens = []
        seen = set()

        for token_info in tokens:
            token = token_info['token']

            if token in seen:
                continue

            category = token_info['category']
            score = CppTokenExtractor.PRIORITY.get(category, 1)
            score += len(token) * 0.1

            if token in CppTokenExtractor.DISTRACTORS:
                score += 2.0

            scored_tokens.append({'token': token, 'score': score})
            seen.add(token)

        scored_tokens.sort(key=lambda x: x['score'], reverse=True)
        return [st['token'] for st in scored_tokens[:num_targets]]

    @staticmethod
    def get_distractors(target: str) -> List[str]:
        """Get distractors for target"""
        if target in CppTokenExtractor.DISTRACTORS:
            return CppTokenExtractor.DISTRACTORS[target][:3]

        # Fallback: same category
        for category, keywords in CppTokenExtractor.KEYWORDS.items():
            if target in keywords:
                others = [k for k in keywords if k != target]
                if len(others) >= 3:
                    return random.sample(others, 3)

        return ['option1', 'option2', 'option3']


class QuestionGenerator1_5b:
    """Generate questions using 1.5b + deterministic processing"""

    def __init__(self):
        self.model = MODEL
        self.ollama_url = OLLAMA_URL

    def call_ollama(self, prompt: str) -> Optional[str]:
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
                            response_text += data["response"]
                    except json.JSONDecodeError:
                        continue

            return response_text.strip()

        except Exception as e:
            print(f"❌ Error: {e}")
            return None

    def generate_code(self, topic: Topic) -> Optional[str]:
        """Generate code using 1.5b (fast)"""

        example_prompt = random.choice(topic.examples)

        prompt = f"""Write a simple, complete C++ code example for: {example_prompt}

Requirements:
- Use modern C++ (C++11+)
- Complete working code
- Include necessary headers
- Add a main function
- Keep it simple and clear

Just write the code, nothing else:"""

        response = self.call_ollama(prompt)
        if not response:
            return None

        # Extract code block if wrapped
        code_match = re.search(r'```(?:cpp)?\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        return response

    def generate_question(self, topic: Topic, num_blanks: int = 3) -> Optional[Dict]:
        """Generate question using deterministic approach"""

        # Phase 1: Generate code with 1.5b
        code = self.generate_code(topic)
        if not code:
            return None

        # Phase 2: Deterministic processing
        tokens = CppTokenExtractor.extract_all_tokens(code)
        if not tokens:
            return None

        targets = CppTokenExtractor.select_best_targets(tokens, num_blanks)
        if not targets:
            return None

        # Generate distractors
        all_distractors = []
        for target in targets:
            distractors = CppTokenExtractor.get_distractors(target)
            all_distractors.append(distractors)

        # Create question code
        question_code = code
        for i, target in enumerate(targets):
            blank = f"_____({i+1})_____"
            question_code = question_code.replace(target, blank, 1)

        # Create sub-questions
        sub_questions = []
        for i, (target, distractors) in enumerate(zip(targets, all_distractors)):
            options = [target] + distractors
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
        self.generator = QuestionGenerator1_5b()
        self.curriculum = CppCurriculum()
        self.questions = []
        self.score = 0
        self.total_questions = 0

    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*80)
        print("⚡ C++ PROGRAMMING QUIZ - Fast 1.5b Model")
        print("="*80)
        print("\nWelcome to the interactive C++ programming quiz!")
        print("Answer fill-in-the-blank questions to test your knowledge.")
        print("\nFeatures:")
        print("  • Progressive curriculum (Beginner → Advanced)")
        print("  • Fast generation with 1.5b model + deterministic processing")
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
        print("Fast generation with 1.5b model...\n")

        selected_topics = random.sample(topics, min(num_questions, len(topics)))

        for i, topic in enumerate(selected_topics, 1):
            print(f"[{i}/{len(selected_topics)}] Generating: {topic.name}...", end=' ')
            question = self.generator.generate_question(topic, num_blanks=3)

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
        description='Interactive C++ Quiz with Fast 1.5b Model',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python quiz_app_1_5b.py                    # Default: Level 1, 5 questions
  python quiz_app_1_5b.py --level 3          # Level 3 (Loops), 5 questions
  python quiz_app_1_5b.py --level 5 --questions 10  # Level 5, 10 questions
  python quiz_app_1_5b.py --level 8 --questions 3   # Level 8 (Classes), 3 questions

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
