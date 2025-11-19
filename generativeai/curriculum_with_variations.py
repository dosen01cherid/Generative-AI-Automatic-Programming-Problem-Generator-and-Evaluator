"""
Enhanced Curriculum with Difficulty Variations
-----------------------------------------------
Each topic now has multiple difficulty levels with explicit specification variations.
Students must complete minimum difficulty before advancing.
"""

import sys
import io
from typing import List, Dict
from dataclasses import dataclass
from enum import Enum

# Fix encoding
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


class DifficultyLevel(Enum):
    """Difficulty levels within a topic"""
    BEGINNER = 1      # Must complete to unlock next topic
    INTERMEDIATE = 2  # Optional practice
    ADVANCED = 3      # Challenge mode
    EXPERT = 4        # Master level


@dataclass
class SpecificationVariation:
    """A specific way to ask for a programming task"""
    difficulty: DifficultyLevel
    specification: str
    description: str
    min_score: int  # Minimum score to pass (out of 3 blanks)


@dataclass
class TopicWithVariations:
    """Enhanced topic with multiple difficulty variations"""
    id: str
    name: str
    description: str
    base_difficulty: int  # Overall topic difficulty (1-5)
    prerequisites: List[str]
    variations: List[SpecificationVariation]

    def get_variations_by_difficulty(self, level: DifficultyLevel) -> List[SpecificationVariation]:
        """Get all variations for a specific difficulty level"""
        return [v for v in self.variations if v.difficulty == level]


class EnhancedCurriculum:
    """Curriculum with difficulty variations"""

    # Level 1: Basics
    LEVEL_1_BASICS = [
        TopicWithVariations(
            id="L1_01",
            name="Hello World",
            description="First C++ program with cout",
            base_difficulty=1,
            prerequisites=[],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Print 'Hello World' to console",
                    description="Simple hello world program",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Display a welcome message using cout",
                    description="Variation: Welcome message",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Print your name and age on separate lines",
                    description="Multiple output lines",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Create a program that prints a formatted greeting with your name, age, and university",
                    description="Complex formatted output",
                    min_score=3
                ),
            ]
        ),

        TopicWithVariations(
            id="L1_03",
            name="Integer Variables",
            description="Declaring and using int variables",
            base_difficulty=1,
            prerequisites=["L1_01"],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Declare an integer variable and assign it a value",
                    description="Simple variable declaration",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a variable to store someone's age and display it",
                    description="Age variable with output",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Declare two integer variables, assign values, and print both",
                    description="Multiple variables",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Declare variables for student ID, age, and year, then display them with labels",
                    description="Multiple variables with formatting",
                    min_score=3
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.EXPERT,
                    specification="Create a program with multiple integer variables representing student data (ID, scores, etc.) with formatted table output",
                    description="Complex variable management",
                    min_score=3
                ),
            ]
        ),
    ]

    # Level 3: Loops
    LEVEL_3_LOOPS = [
        TopicWithVariations(
            id="L3_01",
            name="For Loops",
            description="Counted iteration",
            base_difficulty=2,
            prerequisites=["L1_03"],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a for loop that counts from 0 to 5",
                    description="Simple counting loop",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Write a loop that prints numbers 1 through 10",
                    description="Counting 1 to 10",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Create a for loop that prints even numbers from 0 to 20",
                    description="Even numbers only",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Write a loop that calculates the sum of numbers 1 to N",
                    description="Accumulator pattern",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Create a for loop that prints a multiplication table for a given number",
                    description="Multiplication table",
                    min_score=3
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Write a loop that counts backwards from 100 to 0 by steps of 5",
                    description="Decrement with step",
                    min_score=3
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.EXPERT,
                    specification="Create nested for loops to print a pyramid pattern of stars",
                    description="Nested loops pattern",
                    min_score=3
                ),
            ]
        ),

        TopicWithVariations(
            id="L3_02",
            name="While Loops",
            description="Conditional iteration",
            base_difficulty=2,
            prerequisites=["L3_01"],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a while loop that counts from 1 to 5",
                    description="Simple while counter",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Write a countdown loop from 10 to 0",
                    description="Countdown timer",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Create a while loop that doubles a number until it exceeds 100",
                    description="Conditional growth",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Write a while loop that finds the first power of 2 greater than 1000",
                    description="Search pattern",
                    min_score=3
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.EXPERT,
                    specification="Create a while loop that implements a number guessing game with attempts limit",
                    description="Interactive loop with conditions",
                    min_score=3
                ),
            ]
        ),
    ]

    # Level 7: Vectors
    LEVEL_7_VECTORS = [
        TopicWithVariations(
            id="L7_01",
            name="Vector Basics",
            description="Introduction to vector container",
            base_difficulty=3,
            prerequisites=["L5_01"],
            variations=[
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Create a vector and add three numbers using push_back",
                    description="Basic vector operations",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.BEGINNER,
                    specification="Declare a vector of integers and display its size",
                    description="Vector size function",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Create a vector, add 5 elements, then print the first and last elements",
                    description="Vector access patterns",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.INTERMEDIATE,
                    specification="Initialize a vector with values and check if it's empty",
                    description="Vector initialization and empty check",
                    min_score=2
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.ADVANCED,
                    specification="Create a vector of student scores, add values, calculate average, and display",
                    description="Vector with calculations",
                    min_score=3
                ),
                SpecificationVariation(
                    difficulty=DifficultyLevel.EXPERT,
                    specification="Implement a vector-based dynamic array that grows, shrinks, and reports capacity vs size",
                    description="Advanced vector management",
                    min_score=3
                ),
            ]
        ),
    ]

    @classmethod
    def get_all_topics(cls) -> List[TopicWithVariations]:
        """Get all topics with variations"""
        return (
            cls.LEVEL_1_BASICS +
            cls.LEVEL_3_LOOPS +
            cls.LEVEL_7_VECTORS
        )

    @classmethod
    def get_topic_by_id(cls, topic_id: str) -> TopicWithVariations:
        """Get specific topic by ID"""
        for topic in cls.get_all_topics():
            if topic.id == topic_id:
                return topic
        return None

    @classmethod
    def get_variation_count(cls) -> Dict:
        """Get statistics on variations"""
        stats = {
            'total_topics': 0,
            'total_variations': 0,
            'by_difficulty': {
                DifficultyLevel.BEGINNER: 0,
                DifficultyLevel.INTERMEDIATE: 0,
                DifficultyLevel.ADVANCED: 0,
                DifficultyLevel.EXPERT: 0,
            }
        }

        for topic in cls.get_all_topics():
            stats['total_topics'] += 1
            stats['total_variations'] += len(topic.variations)

            for variation in topic.variations:
                stats['by_difficulty'][variation.difficulty] += 1

        return stats


def main():
    """Demo enhanced curriculum"""
    curriculum = EnhancedCurriculum()

    print("="*80)
    print("ENHANCED CURRICULUM WITH DIFFICULTY VARIATIONS")
    print("="*80)

    # Show all topics with variations
    for topic in curriculum.get_all_topics():
        print(f"\n{topic.id}: {topic.name}")
        print(f"Base Difficulty: {'⭐' * topic.base_difficulty}")
        print(f"Variations: {len(topic.variations)}")

        for level in DifficultyLevel:
            variations = topic.get_variations_by_difficulty(level)
            if variations:
                print(f"\n  {level.name}:")
                for i, var in enumerate(variations, 1):
                    print(f"    {i}. {var.specification}")
                    print(f"       Min score to pass: {var.min_score}/3")

    # Statistics
    stats = curriculum.get_variation_count()
    print("\n" + "="*80)
    print("STATISTICS")
    print("="*80)
    print(f"Total Topics: {stats['total_topics']}")
    print(f"Total Variations: {stats['total_variations']}")
    print(f"\nBy Difficulty:")
    for level, count in stats['by_difficulty'].items():
        print(f"  {level.name}: {count} variations")


if __name__ == "__main__":
    main()
