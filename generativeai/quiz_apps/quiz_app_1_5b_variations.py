"""
Interactive C++ Quiz Application - 1.5b Model with Specification Variations
----------------------------------------------------------------------------
Fast two-phase generation with deterministic processing:
1. Phase 1: Select specification variation based on student level
2. Phase 2: Generate code from specification (1.5b)
3. Phase 3: Deterministic target/distractor extraction
4. Track progress and unlock difficulties

Usage: python quiz_app_1_5b_variations.py
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
from curriculum.curriculum_with_variations import EnhancedCurriculum, TopicWithVariations, SpecificationVariation, DifficultyLevel

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://trend-publishers-words-fire.trycloudflare.com"
MODEL = "qwen2.5:1.5b"
TIMEOUT = 300
KEEP_ALIVE = "60m"
PROGRESS_FILE = "student_progress.json"


class StudentProgress:
    """Track student progress through curriculum"""

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

    def get_topic_progress(self, topic_id: str) -> Dict:
        """Get progress for a topic"""
        if topic_id not in self.progress:
            self.progress[topic_id] = {
                'current_difficulty': DifficultyLevel.BEGINNER.value,
                'completed_difficulties': [],
                'scores': {},
                'unlocked': False
            }
        return self.progress[topic_id]

    def update_score(self, topic_id: str, difficulty: DifficultyLevel, score: int, total: int):
        """Update score for a topic/difficulty"""
        progress = self.get_topic_progress(topic_id)

        # Record score
        diff_key = difficulty.name
        if diff_key not in progress['scores']:
            progress['scores'][diff_key] = []
        progress['scores'][diff_key].append({'score': score, 'total': total})

        # Get best score
        best_score = max(s['score'] for s in progress['scores'][diff_key])

        self.save_progress()
        return best_score

    def is_difficulty_unlocked(self, topic_id: str, difficulty: DifficultyLevel) -> bool:
        """Check if difficulty is unlocked"""
        progress = self.get_topic_progress(topic_id)

        # BEGINNER always unlocked
        if difficulty == DifficultyLevel.BEGINNER:
            return True

        # Check if previous difficulty is passed
        prev_levels = {
            DifficultyLevel.INTERMEDIATE: DifficultyLevel.BEGINNER,
            DifficultyLevel.ADVANCED: DifficultyLevel.INTERMEDIATE,
            DifficultyLevel.EXPERT: DifficultyLevel.ADVANCED
        }

        prev_level = prev_levels.get(difficulty)
        if not prev_level:
            return True

        # Check if previous level has any scores
        prev_key = prev_level.name
        return prev_key in progress['scores'] and len(progress['scores'][prev_key]) > 0

    def is_topic_unlocked(self, topic_id: str) -> bool:
        """Check if topic is unlocked for next topic progression"""
        progress = self.get_topic_progress(topic_id)

        # Check if BEGINNER has been attempted
        return 'BEGINNER' in progress['scores'] and len(progress['scores']['BEGINNER']) > 0

    def get_current_difficulty(self, topic_id: str) -> DifficultyLevel:
        """Get current difficulty for topic"""
        progress = self.get_topic_progress(topic_id)

        # Find highest unlocked difficulty
        for level in [DifficultyLevel.EXPERT, DifficultyLevel.ADVANCED,
                      DifficultyLevel.INTERMEDIATE, DifficultyLevel.BEGINNER]:
            if self.is_difficulty_unlocked(topic_id, level):
                return level

        return DifficultyLevel.BEGINNER


class CppTokenExtractor:
    """Deterministic token extraction"""

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

    def generate_code(self, topic: TopicWithVariations, variation: SpecificationVariation) -> Optional[str]:
        """
        Phase 2: Generate code using 1.5b from specification
        """
        prompt = f"""Write a simple, complete C++ code example for this task:

{variation.specification}

Topic: {topic.name}
Difficulty: {variation.difficulty.name}

Requirements:
- Use modern C++ (C++11+)
- Complete working code
- Include necessary headers
- Add a main function
- Keep it simple and clear
- Match the {variation.difficulty.name} difficulty level

Just write the code, nothing else:"""

        response = self.call_ollama(prompt)
        if not response:
            return None

        # Extract code block if wrapped
        code_match = re.search(r'```(?:cpp)?\s*(.*?)\s*```', response, re.DOTALL)
        if code_match:
            return code_match.group(1).strip()

        return response

    def generate_question(self, topic: TopicWithVariations, variation: SpecificationVariation,
                         num_blanks: int = 3) -> Optional[Dict]:
        """
        Three-phase generation:
        Phase 1: Specification variation (already selected)
        Phase 2: Generate code with 1.5b from specification
        Phase 3: Deterministic processing
        """

        # Phase 2: Generate code
        code = self.generate_code(topic, variation)
        if not code:
            return None

        # Phase 3: Deterministic processing
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
            'variation': variation,
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions
        }


class QuizApp:
    """Interactive quiz application with difficulty progression"""

    def __init__(self):
        self.generator = QuestionGenerator1_5b()
        self.curriculum = EnhancedCurriculum()
        self.progress = StudentProgress()
        self.questions = []
        self.score = 0
        self.total_questions = 0

    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*80)
        print("⚡ C++ PROGRAMMING QUIZ - Fast Progressive Difficulty System")
        print("="*80)
        print("\nWelcome to the enhanced C++ programming quiz!")
        print("Answer fill-in-the-blank questions to unlock new difficulty levels.")
        print("\nNew Features:")
        print("  ✨ Multiple specification variations per topic")
        print("  📈 Progressive difficulty (BEGINNER → INTERMEDIATE → ADVANCED → EXPERT)")
        print("  🔓 Unlock system - pass BEGINNER to advance topics")
        print("  🏆 Challenge mode - return to topics for EXPERT level")
        print("  💾 Progress tracking - your scores are saved")
        print("  ⚡ Fast generation with 1.5b model + deterministic processing")
        print("="*80)

    def display_topic_menu(self):
        """Display topic selection menu"""
        topics = self.curriculum.get_all_topics()

        print("\n" + "="*80)
        print("📚 SELECT TOPIC")
        print("="*80)

        for i, topic in enumerate(topics, 1):
            progress = self.progress.get_topic_progress(topic.id)

            # Check if unlocked
            unlocked = (i == 1) or self.progress.is_topic_unlocked(topics[i-2].id)

            # Display status
            if unlocked:
                # Show difficulty progress
                difficulties_done = len(progress['scores'])
                status = f"[{difficulties_done}/4 difficulties]"
                print(f"  {i}. {topic.name} {'⭐' * topic.base_difficulty} {status}")
            else:
                print(f"  {i}. {topic.name} 🔒 (Complete previous topic's BEGINNER level)")

        print(f"  {len(topics)+1}. View Progress")
        print(f"  0. Exit")
        print("="*80)

        while True:
            try:
                choice = int(input("\nSelect topic (0 to exit): ").strip())
                if choice == 0:
                    return None
                elif choice == len(topics) + 1:
                    self.display_progress_report()
                    self.display_topic_menu()
                    return None
                elif 1 <= choice <= len(topics):
                    topic = topics[choice - 1]
                    # Check if unlocked
                    if choice == 1 or self.progress.is_topic_unlocked(topics[choice-2].id):
                        return topic
                    else:
                        print("❌ This topic is locked. Complete previous topic's BEGINNER level first.")
                else:
                    print(f"Please enter 0-{len(topics)+1}")
            except ValueError:
                print("Please enter a valid number")

    def display_difficulty_menu(self, topic: TopicWithVariations):
        """Display difficulty selection for a topic"""
        print("\n" + "="*80)
        print(f"📊 DIFFICULTY LEVELS - {topic.name}")
        print("="*80)

        progress = self.progress.get_topic_progress(topic.id)

        for level in DifficultyLevel:
            variations = topic.get_variations_by_difficulty(level)
            if not variations:
                continue

            unlocked = self.progress.is_difficulty_unlocked(topic.id, level)

            # Get best score if attempted
            level_key = level.name
            best_score = None
            if level_key in progress['scores'] and progress['scores'][level_key]:
                scores = progress['scores'][level_key]
                best_score = max(s['score'] for s in scores)
                best_total = max(s['total'] for s in scores)

            # Display
            if unlocked:
                status = f"✅ Best: {best_score}/{best_total}" if best_score is not None else "📝 Not attempted"
                print(f"  {level.value}. {level.name} ({len(variations)} variations) - {status}")
            else:
                print(f"  {level.value}. {level.name} 🔒 (Complete previous difficulty first)")

        print(f"  0. Back to topic selection")
        print("="*80)

        while True:
            try:
                choice = int(input("\nSelect difficulty (0 to go back): ").strip())
                if choice == 0:
                    return None

                # Find difficulty by value
                selected_diff = None
                for level in DifficultyLevel:
                    if level.value == choice:
                        selected_diff = level
                        break

                if selected_diff and self.progress.is_difficulty_unlocked(topic.id, selected_diff):
                    variations = topic.get_variations_by_difficulty(selected_diff)
                    if variations:
                        return random.choice(variations)  # Pick random variation
                    else:
                        print("No variations available for this difficulty")
                else:
                    print("❌ This difficulty is locked or invalid. Complete previous difficulty first.")
            except ValueError:
                print("Please enter a valid number")

    def display_progress_report(self):
        """Display student's overall progress"""
        print("\n" + "="*80)
        print("📊 YOUR PROGRESS REPORT")
        print("="*80)

        topics = self.curriculum.get_all_topics()

        for topic in topics:
            progress = self.progress.get_topic_progress(topic.id)

            print(f"\n{topic.name}:")

            if not progress['scores']:
                print("  Not started")
                continue

            for level in DifficultyLevel:
                level_key = level.name
                if level_key in progress['scores'] and progress['scores'][level_key]:
                    scores = progress['scores'][level_key]
                    best = max(s['score'] for s in scores)
                    total = max(s['total'] for s in scores)
                    attempts = len(scores)
                    print(f"  {level.name}: {best}/{total} (best of {attempts} attempts)")

        print("\n" + "="*80)
        input("\nPress Enter to continue...")

    def display_topic_info(self, topic: TopicWithVariations, variation: SpecificationVariation):
        """Display topic and variation information"""
        print(f"\n{'='*80}")
        print(f"📚 Topic: {topic.name}")
        print(f"{'='*80}")
        print(f"Description: {topic.description}")
        print(f"Base Difficulty: {'⭐' * topic.base_difficulty} ({topic.base_difficulty}/5)")
        print(f"\n🎯 Challenge Level: {variation.difficulty.name}")
        print(f"Specification: {variation.specification}")
        print(f"Minimum score to pass: {variation.min_score}/3")
        print("="*80)

    def display_question(self, question: Dict):
        """Display a question"""
        print(f"\n{'='*80}")
        print(f"FILL-IN-THE-BLANK QUESTION")
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
        variation = question['variation']
        percentage = (score / total * 100) if total > 0 else 0

        print(f"\n{'='*80}")
        print(f"📊 RESULTS")
        print(f"{'='*80}")
        print(f"Score: {score}/{total} ({percentage:.1f}%)")
        print(f"Required to pass: {variation.min_score}/{total}")

        if score >= variation.min_score:
            print(f"✅ PASSED! Great job!")

            # Check if this unlocks next difficulty
            topic = question['topic']
            next_level = None
            if variation.difficulty == DifficultyLevel.BEGINNER:
                next_level = DifficultyLevel.INTERMEDIATE
            elif variation.difficulty == DifficultyLevel.INTERMEDIATE:
                next_level = DifficultyLevel.ADVANCED
            elif variation.difficulty == DifficultyLevel.ADVANCED:
                next_level = DifficultyLevel.EXPERT

            if next_level:
                print(f"🔓 {next_level.name} difficulty unlocked for this topic!")
        else:
            print(f"❌ Need {variation.min_score - score} more correct to pass")
            print(f"💪 Try again to improve your score!")

        print(f"{'='*80}")

    def run_quiz(self):
        """Run the interactive quiz"""
        self.display_welcome()

        while True:
            # Select topic
            topic = self.display_topic_menu()
            if topic is None:
                print("\nThank you for using the quiz! Goodbye! 👋")
                break

            # Select difficulty
            variation = self.display_difficulty_menu(topic)
            if variation is None:
                continue

            # Generate question
            self.display_topic_info(topic, variation)
            print(f"\n⏳ Generating question...")
            print("Fast generation with 1.5b model...")

            question = self.generator.generate_question(topic, variation, num_blanks=3)

            if not question:
                print("\n❌ Failed to generate question. Please try again.")
                input("\nPress Enter to continue...")
                continue

            print("✅ Question generated!")
            input("\nPress Enter to start...")

            # Display and ask question
            self.display_question(question)
            num_blanks = len(question['sub_questions'])
            score = self.ask_question(question)

            # Update progress
            self.progress.update_score(topic.id, variation.difficulty, score, num_blanks)

            # Display summary
            self.display_question_summary(question, score, num_blanks)

            input("\nPress Enter to continue...")


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='Interactive C++ Quiz with Progressive Difficulty (Fast 1.5b Model)',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Features:
  • Fast two-phase LLM generation + deterministic processing
  • Four difficulty levels per topic (BEGINNER → INTERMEDIATE → ADVANCED → EXPERT)
  • Progress tracking - scores saved between sessions
  • Unlock system - pass BEGINNER to advance to next topic
  • Challenge mode - return to topics for harder difficulties
  • ~8s per question vs 25-30s with 14b model

Usage:
  python quiz_app_1_5b_variations.py

Then follow the interactive menus to:
  1. Select a topic
  2. Choose difficulty level (unlocked difficulties only)
  3. Answer the fill-in-the-blank question
  4. Track your progress and unlock new challenges
        """
    )

    app = QuizApp()
    try:
        app.run_quiz()
    except KeyboardInterrupt:
        print("\n\nQuiz interrupted. Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
