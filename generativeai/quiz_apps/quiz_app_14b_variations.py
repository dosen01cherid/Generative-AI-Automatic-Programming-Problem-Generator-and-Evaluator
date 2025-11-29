"""
Interactive C++ Quiz Application - 14b Model with Specification Variations
---------------------------------------------------------------------------
Two-phase LLM generation with difficulty progression:
1. Phase 1: Select specification variation based on student level
2. Phase 2: Generate code from specification
3. Track progress and unlock difficulties

Usage: python quiz_app_14b_variations.py
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
from curriculum.curriculum_with_variations import EnhancedCurriculum, TopicWithVariations, SpecificationVariation, DifficultyLevel

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Configuration
OLLAMA_URL = "https://unpatented-saylor-nonirate.ngrok-free.dev"
MODEL = "qwen2.5:14b"
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

        # Check if passed (best score >= min_score)
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


class QuestionGenerator14b:
    """Generate questions using 14b model with two-phase approach"""

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

    def generate_question(self, topic: TopicWithVariations, variation: SpecificationVariation,
                         num_blanks: int = 3, verbose: bool = False) -> Optional[Dict]:
        """
        Two-phase generation:
        Phase 1: Use specification variation (already selected)
        Phase 2: Generate code from specification
        """

        # Phase 2: Generate code from specification
        prompt = f"""Create a C++ fill-in-the-blank question for this specification:

"{variation.specification}"

Topic: {topic.name}
Description: {topic.description}
Difficulty: {variation.difficulty.name}

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
- Match difficulty level: {variation.difficulty.name}
"""

        if verbose:
            print(f"\n⏳ Generating question for: {variation.specification}...")

        response = self.call_ollama(prompt, verbose=False)

        if not response:
            return None

        # Parse response
        parsed = self.parse_response(response)
        if not parsed:
            return None

        # Create validated question
        return self.create_validated_question(parsed, topic, variation)

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

    def create_validated_question(self, parsed: Dict, topic: TopicWithVariations,
                                  variation: SpecificationVariation) -> Optional[Dict]:
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
            'variation': variation,
            'code': code,
            'question_code': question_code,
            'sub_questions': sub_questions
        }


class QuizApp:
    """Interactive quiz application with difficulty progression"""

    def __init__(self):
        self.generator = QuestionGenerator14b()
        self.curriculum = EnhancedCurriculum()
        self.progress = StudentProgress()
        self.questions = []
        self.score = 0
        self.total_questions = 0

    def display_welcome(self):
        """Display welcome message"""
        print("\n" + "="*80)
        print("🎓 C++ PROGRAMMING QUIZ - Progressive Difficulty System")
        print("="*80)
        print("\nWelcome to the enhanced C++ programming quiz!")
        print("Answer fill-in-the-blank questions to unlock new difficulty levels.")
        print("\nNew Features:")
        print("  ✨ Multiple specification variations per topic")
        print("  📈 Progressive difficulty (BEGINNER → INTERMEDIATE → ADVANCED → EXPERT)")
        print("  🔓 Unlock system - pass BEGINNER to advance topics")
        print("  🏆 Challenge mode - return to topics for EXPERT level")
        print("  💾 Progress tracking - your scores are saved")
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
            print("This may take a minute with the 14b model...")

            question = self.generator.generate_question(topic, variation, num_blanks=3, verbose=False)

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
        description='Interactive C++ Quiz with Progressive Difficulty',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Features:
  • Two-phase LLM generation with specification variations
  • Four difficulty levels per topic (BEGINNER → INTERMEDIATE → ADVANCED → EXPERT)
  • Progress tracking - scores saved between sessions
  • Unlock system - pass BEGINNER to advance to next topic
  • Challenge mode - return to topics for harder difficulties

Usage:
  python quiz_app_14b_variations.py

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
