"""
C++ Curriculum Progression
---------------------------
Structured learning path from beginner to advanced C++ concepts.
Used for generating progressive fill-in-the-blank questions.
"""

import sys
import io
from typing import List, Dict
from dataclasses import dataclass

# Fix encoding for Windows console
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')


@dataclass
class Topic:
    """Represents a curriculum topic"""
    id: str
    name: str
    description: str
    difficulty: int  # 1-5 (1=beginner, 5=advanced)
    prerequisites: List[str]  # List of topic IDs that should be learned first
    examples: List[str]  # Example prompts for question generation


class CppCurriculum:
    """
    Complete C++ curriculum organized by difficulty level.
    Follows standard CS1/CS2 progression.
    """

    # Level 1: Absolute Beginners (Week 1-2)
    LEVEL_1_BASICS = [
        Topic(
            id="L1_01",
            name="Hello World",
            description="First C++ program with cout",
            difficulty=1,
            prerequisites=[],
            examples=[
                "Print 'Hello World' to console",
                "Print your name using cout",
                "Display a welcome message",
            ]
        ),
        Topic(
            id="L1_02",
            name="Basic Output",
            description="Using cout and endl",
            difficulty=1,
            prerequisites=["L1_01"],
            examples=[
                "Print multiple lines with cout and endl",
                "Display numbers using cout",
                "Print text and numbers together",
            ]
        ),
        Topic(
            id="L1_03",
            name="Integer Variables",
            description="Declaring and using int variables",
            difficulty=1,
            prerequisites=["L1_02"],
            examples=[
                "Declare and initialize an integer variable",
                "Perform addition with two integers",
                "Store user's age in a variable",
            ]
        ),
        Topic(
            id="L1_04",
            name="Basic Arithmetic",
            description="Addition, subtraction, multiplication, division",
            difficulty=1,
            prerequisites=["L1_03"],
            examples=[
                "Calculate sum of two numbers",
                "Find average of three numbers",
                "Convert temperature Celsius to Fahrenheit",
            ]
        ),
        Topic(
            id="L1_05",
            name="Basic Input",
            description="Using cin for input",
            difficulty=1,
            prerequisites=["L1_03"],
            examples=[
                "Read an integer from user with cin",
                "Input two numbers and display their sum",
                "Get user's age and display it",
            ]
        ),
    ]

    # Level 2: Basic Programming (Week 3-4)
    LEVEL_2_CONTROL = [
        Topic(
            id="L2_01",
            name="If Statements",
            description="Basic conditional logic",
            difficulty=2,
            prerequisites=["L1_03", "L1_04"],
            examples=[
                "Check if a number is positive",
                "Determine if age is adult or child",
                "Compare two numbers and print the larger",
            ]
        ),
        Topic(
            id="L2_02",
            name="If-Else Statements",
            description="Two-way conditional branching",
            difficulty=2,
            prerequisites=["L2_01"],
            examples=[
                "Check if number is even or odd",
                "Determine pass or fail based on score",
                "Check if year is leap year",
            ]
        ),
        Topic(
            id="L2_03",
            name="Nested If Statements",
            description="Multiple level conditions",
            difficulty=2,
            prerequisites=["L2_02"],
            examples=[
                "Grade calculator (A, B, C, D, F)",
                "Determine largest of three numbers",
                "Check eligibility with multiple conditions",
            ]
        ),
        Topic(
            id="L2_04",
            name="Switch Statements",
            description="Multi-way branching",
            difficulty=2,
            prerequisites=["L2_02"],
            examples=[
                "Menu selection with switch",
                "Day of week converter",
                "Calculator with switch for operations",
            ]
        ),
        Topic(
            id="L2_05",
            name="Boolean Variables",
            description="Using bool type and logical operators",
            difficulty=2,
            prerequisites=["L2_01"],
            examples=[
                "Check multiple conditions with AND",
                "Use OR for alternative conditions",
                "Toggle a boolean flag",
            ]
        ),
    ]

    # Level 3: Loops (Week 5-6)
    LEVEL_3_LOOPS = [
        Topic(
            id="L3_01",
            name="For Loops",
            description="Counted iteration",
            difficulty=2,
            prerequisites=["L1_03"],
            examples=[
                "Print numbers from 1 to 10",
                "Calculate sum of first N numbers",
                "Print multiplication table",
            ]
        ),
        Topic(
            id="L3_02",
            name="While Loops",
            description="Conditional iteration",
            difficulty=2,
            prerequisites=["L2_01"],
            examples=[
                "Count down from 10 to 0",
                "Read numbers until negative",
                "Validate input with while loop",
            ]
        ),
        Topic(
            id="L3_03",
            name="Do-While Loops",
            description="Post-test loops",
            difficulty=2,
            prerequisites=["L3_02"],
            examples=[
                "Menu that runs at least once",
                "Input validation with do-while",
                "Repeat until user says stop",
            ]
        ),
        Topic(
            id="L3_04",
            name="Nested Loops",
            description="Loops within loops",
            difficulty=3,
            prerequisites=["L3_01"],
            examples=[
                "Print a pattern of stars",
                "Generate multiplication table grid",
                "Print triangle of numbers",
            ]
        ),
        Topic(
            id="L3_05",
            name="Break and Continue",
            description="Loop control statements",
            difficulty=2,
            prerequisites=["L3_01", "L3_02"],
            examples=[
                "Exit loop when condition met with break",
                "Skip even numbers with continue",
                "Find first prime number",
            ]
        ),
    ]

    # Level 4: Functions (Week 7-8)
    LEVEL_4_FUNCTIONS = [
        Topic(
            id="L4_01",
            name="Void Functions",
            description="Functions with no return value",
            difficulty=3,
            prerequisites=["L1_01"],
            examples=[
                "Create a greeting function",
                "Function to print a separator line",
                "Display menu function",
            ]
        ),
        Topic(
            id="L4_02",
            name="Return Functions",
            description="Functions that return values",
            difficulty=3,
            prerequisites=["L4_01"],
            examples=[
                "Function to calculate square of number",
                "Function to find maximum of two numbers",
                "Calculate area of circle function",
            ]
        ),
        Topic(
            id="L4_03",
            name="Function Parameters",
            description="Passing arguments to functions",
            difficulty=3,
            prerequisites=["L4_02"],
            examples=[
                "Function with multiple parameters",
                "Calculate power function (base, exponent)",
                "Distance calculation with two points",
            ]
        ),
        Topic(
            id="L4_04",
            name="Function Overloading",
            description="Multiple functions with same name",
            difficulty=3,
            prerequisites=["L4_03"],
            examples=[
                "Overload max function for 2 and 3 parameters",
                "Print function for different types",
                "Calculate area for different shapes",
            ]
        ),
        Topic(
            id="L4_05",
            name="Reference Parameters",
            description="Passing by reference",
            difficulty=3,
            prerequisites=["L4_03"],
            examples=[
                "Swap two numbers using references",
                "Modify variable in function with reference",
                "Function to get multiple return values",
            ]
        ),
    ]

    # Level 5: Arrays (Week 9-10)
    LEVEL_5_ARRAYS = [
        Topic(
            id="L5_01",
            name="Array Declaration",
            description="Creating and initializing arrays",
            difficulty=3,
            prerequisites=["L1_03"],
            examples=[
                "Declare and initialize integer array",
                "Create array of student scores",
                "Array of first 10 prime numbers",
            ]
        ),
        Topic(
            id="L5_02",
            name="Array Iteration",
            description="Looping through arrays",
            difficulty=3,
            prerequisites=["L5_01", "L3_01"],
            examples=[
                "Print all elements of array",
                "Calculate sum of array elements",
                "Find maximum value in array",
            ]
        ),
        Topic(
            id="L5_03",
            name="Array Search",
            description="Finding elements in arrays",
            difficulty=3,
            prerequisites=["L5_02"],
            examples=[
                "Linear search in array",
                "Find if value exists in array",
                "Count occurrences of value",
            ]
        ),
        Topic(
            id="L5_04",
            name="Multi-dimensional Arrays",
            description="2D arrays and matrices",
            difficulty=4,
            prerequisites=["L5_02", "L3_04"],
            examples=[
                "Create and display 2D array",
                "Calculate sum of matrix elements",
                "Print matrix in grid format",
            ]
        ),
        Topic(
            id="L5_05",
            name="Array Algorithms",
            description="Common array operations",
            difficulty=4,
            prerequisites=["L5_03"],
            examples=[
                "Reverse an array",
                "Bubble sort implementation",
                "Find second largest element",
            ]
        ),
    ]

    # Level 6: Strings (Week 11-12)
    LEVEL_6_STRINGS = [
        Topic(
            id="L6_01",
            name="String Basics",
            description="Using C++ string class",
            difficulty=3,
            prerequisites=["L1_02"],
            examples=[
                "Declare and initialize string variable",
                "Concatenate two strings",
                "Get string length",
            ]
        ),
        Topic(
            id="L6_02",
            name="String Input/Output",
            description="Reading and displaying strings",
            difficulty=3,
            prerequisites=["L6_01", "L1_05"],
            examples=[
                "Read a line of text with getline",
                "Print string character by character",
                "Input full name with spaces",
            ]
        ),
        Topic(
            id="L6_03",
            name="String Operations",
            description="Common string manipulations",
            difficulty=3,
            prerequisites=["L6_01"],
            examples=[
                "Extract substring from string",
                "Find character position in string",
                "Replace part of string",
            ]
        ),
        Topic(
            id="L6_04",
            name="String Algorithms",
            description="Working with string data",
            difficulty=4,
            prerequisites=["L6_03", "L3_01"],
            examples=[
                "Count vowels in string",
                "Check if string is palindrome",
                "Convert string to uppercase",
            ]
        ),
        Topic(
            id="L6_05",
            name="String Comparison",
            description="Comparing and sorting strings",
            difficulty=3,
            prerequisites=["L6_01"],
            examples=[
                "Compare two strings alphabetically",
                "Check if strings are equal",
                "Sort array of strings",
            ]
        ),
    ]

    # Level 7: Vectors (Week 13-14)
    LEVEL_7_VECTORS = [
        Topic(
            id="L7_01",
            name="Vector Basics",
            description="Introduction to vector container",
            difficulty=3,
            prerequisites=["L5_01"],
            examples=[
                "Create and initialize vector",
                "Add elements with push_back",
                "Get vector size",
            ]
        ),
        Topic(
            id="L7_02",
            name="Vector Iteration",
            description="Looping through vectors",
            difficulty=3,
            prerequisites=["L7_01", "L3_01"],
            examples=[
                "Print all vector elements with for loop",
                "Calculate sum of vector elements",
                "Use range-based for loop with vector",
            ]
        ),
        Topic(
            id="L7_03",
            name="Vector Operations",
            description="Common vector methods",
            difficulty=3,
            prerequisites=["L7_01"],
            examples=[
                "Insert element at specific position",
                "Remove element with erase",
                "Clear entire vector",
            ]
        ),
        Topic(
            id="L7_04",
            name="Vector Algorithms",
            description="Using STL algorithms with vectors",
            difficulty=4,
            prerequisites=["L7_02"],
            examples=[
                "Sort vector using sort function",
                "Find element in vector",
                "Reverse vector elements",
            ]
        ),
        Topic(
            id="L7_05",
            name="2D Vectors",
            description="Vectors of vectors",
            difficulty=4,
            prerequisites=["L7_01", "L5_04"],
            examples=[
                "Create 2D vector (vector of vectors)",
                "Access 2D vector elements",
                "Dynamic matrix with vectors",
            ]
        ),
    ]

    # Level 8: Classes (Week 15-16)
    LEVEL_8_CLASSES = [
        Topic(
            id="L8_01",
            name="Class Basics",
            description="Defining simple classes",
            difficulty=4,
            prerequisites=["L4_01"],
            examples=[
                "Create a simple Student class",
                "Define Rectangle class with dimensions",
                "Class with data members",
            ]
        ),
        Topic(
            id="L8_02",
            name="Constructors",
            description="Initializing objects",
            difficulty=4,
            prerequisites=["L8_01"],
            examples=[
                "Class with default constructor",
                "Constructor with parameters",
                "Multiple constructors (overloading)",
            ]
        ),
        Topic(
            id="L8_03",
            name="Public and Private",
            description="Access specifiers and encapsulation",
            difficulty=4,
            prerequisites=["L8_01"],
            examples=[
                "Class with private data and public methods",
                "Getter and setter methods",
                "Encapsulated bank account class",
            ]
        ),
        Topic(
            id="L8_04",
            name="Member Functions",
            description="Methods inside classes",
            difficulty=4,
            prerequisites=["L8_01", "L4_02"],
            examples=[
                "Class with calculation methods",
                "Member function to display object data",
                "Const member functions",
            ]
        ),
        Topic(
            id="L8_05",
            name="Multiple Objects",
            description="Creating and using multiple instances",
            difficulty=4,
            prerequisites=["L8_02"],
            examples=[
                "Create array of objects",
                "Vector of custom objects",
                "Compare two objects",
            ]
        ),
    ]

    # Level 9: Advanced Containers (Week 17-18)
    LEVEL_9_CONTAINERS = [
        Topic(
            id="L9_01",
            name="Map Container",
            description="Key-value pairs with map",
            difficulty=4,
            prerequisites=["L7_01"],
            examples=[
                "Create map for student names and scores",
                "Count word frequency with map",
                "Phone book using map",
            ]
        ),
        Topic(
            id="L9_02",
            name="Set Container",
            description="Unique elements with set",
            difficulty=4,
            prerequisites=["L7_01"],
            examples=[
                "Remove duplicates using set",
                "Check membership with set",
                "Union and intersection of sets",
            ]
        ),
        Topic(
            id="L9_03",
            name="Queue Container",
            description="FIFO data structure",
            difficulty=4,
            prerequisites=["L7_01"],
            examples=[
                "Implement waiting queue",
                "Process tasks in order with queue",
                "BFS using queue",
            ]
        ),
        Topic(
            id="L9_04",
            name="Stack Container",
            description="LIFO data structure",
            difficulty=4,
            prerequisites=["L7_01"],
            examples=[
                "Check balanced parentheses with stack",
                "Reverse string using stack",
                "Undo functionality with stack",
            ]
        ),
        Topic(
            id="L9_05",
            name="Container Selection",
            description="Choosing the right container",
            difficulty=4,
            prerequisites=["L9_01", "L9_02", "L9_03", "L9_04"],
            examples=[
                "Compare vector vs list performance",
                "When to use map vs unordered_map",
                "Container complexity comparison",
            ]
        ),
    ]

    # Level 10: Advanced Topics (Week 19-20)
    LEVEL_10_ADVANCED = [
        Topic(
            id="L10_01",
            name="Pointers Basics",
            description="Introduction to pointers",
            difficulty=5,
            prerequisites=["L1_03"],
            examples=[
                "Declare and initialize pointer",
                "Dereference pointer to get value",
                "Pointer to array",
            ]
        ),
        Topic(
            id="L10_02",
            name="File I/O",
            description="Reading and writing files",
            difficulty=4,
            prerequisites=["L6_02"],
            examples=[
                "Write text to file with ofstream",
                "Read file line by line with ifstream",
                "Append to existing file",
            ]
        ),
        Topic(
            id="L10_03",
            name="Exception Handling",
            description="Try-catch blocks",
            difficulty=4,
            prerequisites=["L4_02"],
            examples=[
                "Basic try-catch for division by zero",
                "Throw custom exception",
                "Handle file opening errors",
            ]
        ),
        Topic(
            id="L10_04",
            name="Templates",
            description="Generic programming",
            difficulty=5,
            prerequisites=["L4_04"],
            examples=[
                "Template function for max",
                "Generic swap function",
                "Template class for pair",
            ]
        ),
        Topic(
            id="L10_05",
            name="Lambda Expressions",
            description="Anonymous functions",
            difficulty=5,
            prerequisites=["L4_02", "L7_04"],
            examples=[
                "Simple lambda for sorting",
                "Lambda with capture",
                "Use lambda with STL algorithms",
            ]
        ),
    ]

    @classmethod
    def get_all_topics(cls) -> List[Topic]:
        """Get all curriculum topics"""
        return (
            cls.LEVEL_1_BASICS +
            cls.LEVEL_2_CONTROL +
            cls.LEVEL_3_LOOPS +
            cls.LEVEL_4_FUNCTIONS +
            cls.LEVEL_5_ARRAYS +
            cls.LEVEL_6_STRINGS +
            cls.LEVEL_7_VECTORS +
            cls.LEVEL_8_CLASSES +
            cls.LEVEL_9_CONTAINERS +
            cls.LEVEL_10_ADVANCED
        )

    @classmethod
    def get_by_difficulty(cls, difficulty: int) -> List[Topic]:
        """Get topics by difficulty level (1-5)"""
        return [t for t in cls.get_all_topics() if t.difficulty == difficulty]

    @classmethod
    def get_by_level(cls, level: int) -> List[Topic]:
        """Get topics by curriculum level (1-10)"""
        levels = [
            cls.LEVEL_1_BASICS,
            cls.LEVEL_2_CONTROL,
            cls.LEVEL_3_LOOPS,
            cls.LEVEL_4_FUNCTIONS,
            cls.LEVEL_5_ARRAYS,
            cls.LEVEL_6_STRINGS,
            cls.LEVEL_7_VECTORS,
            cls.LEVEL_8_CLASSES,
            cls.LEVEL_9_CONTAINERS,
            cls.LEVEL_10_ADVANCED,
        ]
        if 1 <= level <= 10:
            return levels[level - 1]
        return []

    @classmethod
    def get_topic_by_id(cls, topic_id: str) -> Topic:
        """Get specific topic by ID"""
        for topic in cls.get_all_topics():
            if topic.id == topic_id:
                return topic
        return None

    @classmethod
    def get_learning_path(cls, start_level: int = 1, end_level: int = 10) -> List[Topic]:
        """Get sequential learning path"""
        topics = []
        for level in range(start_level, end_level + 1):
            topics.extend(cls.get_by_level(level))
        return topics

    @classmethod
    def print_curriculum(cls):
        """Print complete curriculum structure"""
        print("\n" + "="*80)
        print("C++ CURRICULUM PROGRESSION")
        print("="*80)

        levels = [
            ("Level 1: Basics (Week 1-2)", cls.LEVEL_1_BASICS),
            ("Level 2: Control Flow (Week 3-4)", cls.LEVEL_2_CONTROL),
            ("Level 3: Loops (Week 5-6)", cls.LEVEL_3_LOOPS),
            ("Level 4: Functions (Week 7-8)", cls.LEVEL_4_FUNCTIONS),
            ("Level 5: Arrays (Week 9-10)", cls.LEVEL_5_ARRAYS),
            ("Level 6: Strings (Week 11-12)", cls.LEVEL_6_STRINGS),
            ("Level 7: Vectors (Week 13-14)", cls.LEVEL_7_VECTORS),
            ("Level 8: Classes (Week 15-16)", cls.LEVEL_8_CLASSES),
            ("Level 9: Advanced Containers (Week 17-18)", cls.LEVEL_9_CONTAINERS),
            ("Level 10: Advanced Topics (Week 19-20)", cls.LEVEL_10_ADVANCED),
        ]

        for level_name, topics in levels:
            print(f"\n{level_name}")
            print("-" * 80)
            for topic in topics:
                stars = "⭐" * topic.difficulty
                prereq_str = ", ".join(topic.prerequisites) if topic.prerequisites else "None"
                print(f"  {topic.id}: {topic.name} {stars}")
                print(f"      {topic.description}")
                print(f"      Prerequisites: {prereq_str}")
                print(f"      Examples: {len(topic.examples)} variations")


def main():
    """Demo curriculum"""
    curriculum = CppCurriculum()

    # Print full curriculum
    curriculum.print_curriculum()

    # Statistics
    all_topics = curriculum.get_all_topics()
    print("\n" + "="*80)
    print("CURRICULUM STATISTICS")
    print("="*80)
    print(f"Total Topics: {len(all_topics)}")
    print(f"Total Example Variations: {sum(len(t.examples) for t in all_topics)}")
    print(f"\nDifficulty Distribution:")
    for diff in range(1, 6):
        topics = curriculum.get_by_difficulty(diff)
        print(f"  Level {diff} {'⭐'*diff}: {len(topics)} topics")

    # Sample learning path
    print("\n" + "="*80)
    print("SAMPLE LEARNING PATH (First 2 weeks)")
    print("="*80)
    path = curriculum.get_learning_path(1, 2)
    for i, topic in enumerate(path, 1):
        print(f"{i}. {topic.name} - {topic.description}")


if __name__ == "__main__":
    main()
