#!/usr/bin/env python3
"""
Test script to verify mc-multiple answer checking logic with shuffled options.
"""

def simulate_answer_check():
    """Simulate the answer checking logic from solve_problem.html"""

    # Simulate a problem step with mc-multiple
    step_data = {
        "step_type": "multiple-choice-multiple",
        "options": [
            {"label": "A", "content": [{"type": "text", "value": "Option A content"}]},
            {"label": "B", "content": [{"type": "text", "value": "Option B content"}]},
            {"label": "C", "content": [{"type": "text", "value": "Option C content"}]},
            {"label": "D", "content": [{"type": "text", "value": "Option D content"}]},
        ],
        "correct_answers": ["A", "B", "D"]  # Original correct answers
    }

    print("=" * 60)
    print("SCENARIO 1: Options in original order")
    print("=" * 60)
    print(f"Options order: {[opt['label'] for opt in step_data['options']]}")
    print(f"Correct answers: {step_data['correct_answers']}")

    # User selects A, B, D (all correct)
    user_answers = ["A", "B", "D"]
    score = calculate_score(step_data, user_answers)
    print(f"\nUser selected: {user_answers}")
    print(f"Score: {score}%")
    print(f"Expected: 100% PASS" if score == 100 else f"Expected: 100% FAIL")

    print("\n" + "=" * 60)
    print("SCENARIO 2: Options shuffled")
    print("=" * 60)

    # Shuffle options (simulate what solve_problem.html does)
    import random
    shuffled_options = step_data['options'].copy()
    random.shuffle(shuffled_options)

    step_data_shuffled = step_data.copy()
    step_data_shuffled['options'] = shuffled_options

    print(f"Options order: {[opt['label'] for opt in step_data_shuffled['options']]}")
    print(f"Correct answers: {step_data_shuffled['correct_answers']}")

    # User selects A, B, D (still correct, but options are in different positions)
    user_answers = ["A", "B", "D"]
    score = calculate_score(step_data_shuffled, user_answers)
    print(f"\nUser selected: {user_answers}")
    print(f"Score: {score}%")
    print(f"Expected: 100% PASS" if score == 100 else f"Expected: 100% FAIL")

    print("\n" + "=" * 60)
    print("SCENARIO 3: User selects wrong answer")
    print("=" * 60)
    print(f"Options order: {[opt['label'] for opt in step_data_shuffled['options']]}")
    print(f"Correct answers: {step_data_shuffled['correct_answers']}")

    # User selects A, C (one correct, one wrong)
    user_answers = ["A", "C"]
    score = calculate_score(step_data_shuffled, user_answers)
    print(f"\nUser selected: {user_answers}")
    print(f"Score: {score}%")
    expected = (100/3) - (100/1)  # One correct out of 3 minus penalty for 1 incorrect
    expected = max(0, expected)
    print(f"Expected: {expected:.2f}%")
    print(f"Match: PASS" if abs(score - expected) < 0.01 else f"Match: FAIL")


def calculate_score(step_data, user_answers):
    """
    Replicate the scoring logic from solve_problem.html lines 12189-12233
    """
    correct_answers = step_data.get("correct_answers", [])

    if not correct_answers:
        return 0.0

    # Get all options
    all_options = step_data.get("options", [])
    total_options = len(all_options)

    if total_options == 0:
        return 0.0

    # Determine correct and incorrect option labels
    correct_labels = set(correct_answers)
    all_labels = set([opt.get("label", "") for opt in all_options])
    incorrect_labels = all_labels - correct_labels

    num_correct = len(correct_labels)
    num_incorrect = len(incorrect_labels)

    # Points distribution
    points_per_correct = 100.0 / num_correct if num_correct > 0 else 0.0
    penalty_per_incorrect = 100.0 / num_incorrect if num_incorrect > 0 else 0.0

    # Calculate score based on selections only
    score = 0.0
    user_set = set(user_answers)

    # Add points for each correct option selected
    for label in user_set:
        if label in correct_labels:
            score += points_per_correct
        elif label in incorrect_labels:
            score -= penalty_per_incorrect

    # Clamp score between 0 and 100
    score = max(0.0, min(100.0, score))

    return score


if __name__ == "__main__":
    simulate_answer_check()
