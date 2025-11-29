#!/usr/bin/env python3
"""
Script to fix reset_all_answers to preserve the problem set
Only answers and progress should be cleared, NOT the problem set itself
"""

import re

def fix_reset_preserve_problem_set():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find and replace the reset_all_answers localStorage clearing code
    old_pattern = r'''            # Clear specific localStorage keys \(matching actual keys used in save_to_storage\)
            window\.localStorage\.removeItem\('problem_solver_problem_set'\)
            window\.localStorage\.removeItem\('problem_solver_states'\)
            window\.localStorage\.removeItem\('problem_solver_current_index'\)
            window\.localStorage\.removeItem\('score_display_manager'\)
            window\.localStorage\.removeItem\('score_edits'\)
            window\.localStorage\.removeItem\('score_tracker_state'\)
            window\.localStorage\.removeItem\('credit_data'\)
            window\.localStorage\.removeItem\('problem_solver_data'\)  # Old format'''

    new_pattern = r'''            # Clear only answer/progress keys - PRESERVE the problem set!
            # DO NOT remove 'problem_solver_problem_set' - that's the problem set itself
            window.localStorage.removeItem('problem_solver_states')  # User answers
            window.localStorage.removeItem('problem_solver_current_index')  # Current position
            window.localStorage.removeItem('score_display_manager')  # Score display
            window.localStorage.removeItem('score_edits')  # Score edits
            window.localStorage.removeItem('score_tracker_state')  # Score tracker
            window.localStorage.removeItem('credit_data')  # Credit data'''

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        updates_made.append("[OK] Fixed reset to preserve problem set")
    else:
        # Try regex approach
        pattern = r'# Clear specific localStorage keys.*?window\.localStorage\.removeItem\(\'problem_solver_data\'\)  # Old format'

        if re.search(pattern, content, re.DOTALL):
            replacement = '''# Clear only answer/progress keys - PRESERVE the problem set!
            # DO NOT remove 'problem_solver_problem_set' - that's the problem set itself
            window.localStorage.removeItem('problem_solver_states')  # User answers
            window.localStorage.removeItem('problem_solver_current_index')  # Current position
            window.localStorage.removeItem('score_display_manager')  # Score display
            window.localStorage.removeItem('score_edits')  # Score edits
            window.localStorage.removeItem('score_tracker_state')  # Score tracker
            window.localStorage.removeItem('credit_data')  # Credit data'''

            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            updates_made.append("[OK] Fixed reset to preserve problem set (regex)")

    # Check if any changes were made
    if content != original_content:
        print(f"\nWriting updated content to {file_path}...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("\n" + "="*60)
        print("Updates completed successfully!")
        print("="*60)
        for update in updates_made:
            print(update)
        print(f"\nTotal updates: {len(updates_made)}")
        print("\nNOTE: Problem set will now be preserved when resetting!")
    else:
        print("\nNo changes made - pattern not found!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Fix Reset to Preserve Problem Set")
    print("="*60)
    print("Removes problem_solver_problem_set from reset list")
    print("Only answers and progress will be cleared, not the problems")
    print()

    try:
        count = fix_reset_preserve_problem_set()
        print(f"\nScript completed! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
