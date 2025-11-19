"""Simple demo of difficulty progression"""
import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

try:
    from curriculum.curriculum_with_variations import EnhancedCurriculum, DifficultyLevel

    print("="*80)
    print("DIFFICULTY PROGRESSION DEMONSTRATION")
    print("="*80)

    curriculum = EnhancedCurriculum()

    # Show topics from different levels
    all_topics = [
        ("LEVEL 1: BASICS", curriculum.LEVEL_1_BASICS[:2]),
        ("LEVEL 3: LOOPS", curriculum.LEVEL_3_LOOPS[:2]),
        ("LEVEL 7: VECTORS", curriculum.LEVEL_7_VECTORS[:1])
    ]

    for level_name, topics in all_topics:
        print(f"\n{'='*80}")
        print(level_name)
        print('='*80)

        for topic in topics:
            print(f"\nTopic: {topic.name}")
            print(f"Description: {topic.description}")
            print(f"Prerequisites: {', '.join(topic.prerequisites) if topic.prerequisites else 'None'}\n")

            for level in DifficultyLevel:
                variations = topic.get_variations_by_difficulty(level)
                if variations:
                    print(f"{level.name} ({level.value}):")
                    for i, var in enumerate(variations, 1):
                        print(f"  {i}. {var.specification}")
                        print(f"     -> {var.description}")
                        print(f"     -> Min score: {var.min_score}/3")
                    print()

    print("\n" + "="*80)
    print("SUMMARY")
    print("="*80)
    print("\nKey Features:")
    print("  * Multiple specification variations per difficulty level")
    print("  * Each variation tests the same concept differently")
    print("  * BEGINNER must be completed to unlock next topic")
    print("  * INTERMEDIATE, ADVANCED, EXPERT are optional challenges")
    print("  * Students can return to topics for higher difficulties")
    print("\nTwo-Phase Generation (14b):")
    print("  1. LLM selects specification variation based on difficulty")
    print("  2. LLM generates code from selected specification")
    print("\nThree-Phase Generation (1.5b):")
    print("  1. LLM selects specification variation")
    print("  2. LLM generates code (fast 1.5b)")
    print("  3. Deterministic extraction of targets/distractors")
    print("\n" + "="*80)

except Exception as e:
    print(f"ERROR: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
