#!/usr/bin/env python3
"""
Script to fix localStorage keys in reset_all_answers method
The keys being removed don't match the actual keys being used in the app
"""

import re

def fix_reset_localstorage_keys():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find the reset_all_answers method and replace the localStorage removal code
    old_pattern = r'''            # Clear specific localStorage keys
            js\.localStorage\.removeItem\('problem_states'\)
            js\.localStorage\.removeItem\('compressed_problem_set'\)
            js\.localStorage\.removeItem\('edited_problems'\)
            js\.localStorage\.removeItem\('score_display_states'\)
            js\.localStorage\.removeItem\('historical_edits'\)
            js\.localStorage\.removeItem\('score_tracker_session'\)
            js\.localStorage\.removeItem\('credit_count'\)
            js\.localStorage\.removeItem\('pending_timer'\)'''

    new_pattern = r'''            # Clear specific localStorage keys (matching actual keys used in save_to_storage)
            window.localStorage.removeItem('problem_solver_problem_set')
            window.localStorage.removeItem('problem_solver_states')
            window.localStorage.removeItem('problem_solver_current_index')
            window.localStorage.removeItem('score_display_manager')
            window.localStorage.removeItem('score_edits')
            window.localStorage.removeItem('score_tracker_state')
            window.localStorage.removeItem('credit_data')
            window.localStorage.removeItem('problem_solver_data')  # Old format
            window.localStorage.removeItem('score_edits')  # Legacy
            window.localStorage.removeItem('score_tracker_state')  # Legacy'''

    if old_pattern in content:
        content = content.replace(old_pattern, new_pattern)
        updates_made.append("[OK] Fixed localStorage keys in reset_all_answers")
    else:
        # Try alternative approach with regex
        pattern = r'# Clear specific localStorage keys\s+js\.localStorage\.removeItem\(\'problem_states\'\).*?js\.localStorage\.removeItem\(\'pending_timer\'\)'

        if re.search(pattern, content, re.DOTALL):
            replacement = '''# Clear specific localStorage keys (matching actual keys used in save_to_storage)
            window.localStorage.removeItem('problem_solver_problem_set')
            window.localStorage.removeItem('problem_solver_states')
            window.localStorage.removeItem('problem_solver_current_index')
            window.localStorage.removeItem('score_display_manager')
            window.localStorage.removeItem('score_edits')
            window.localStorage.removeItem('score_tracker_state')
            window.localStorage.removeItem('credit_data')
            window.localStorage.removeItem('problem_solver_data')  # Old format'''

            content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            updates_made.append("[OK] Fixed localStorage keys (regex method)")

    # Also fix the get_storage_info method to use correct key
    old_get_pattern = r"problem_states_str = js\.localStorage\.getItem\('problem_states'\)"
    new_get_pattern = r"problem_states_str = window.localStorage.getItem('problem_solver_states')"

    if re.search(old_get_pattern, content):
        content = re.sub(old_get_pattern, new_get_pattern, content)
        updates_made.append("[OK] Fixed localStorage key in get_storage_info")

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
    else:
        print("\nNo changes made - pattern not found!")
        print("Searching for current pattern...")
        if 'def reset_all_answers' in content:
            idx = content.find('def reset_all_answers')
            print(f"\nFound reset_all_answers at position {idx}")
            print("Context:")
            print(content[idx:idx+800])

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Fix Reset localStorage Keys Script")
    print("="*60)
    print("Fixes localStorage keys to match actual keys used in app")
    print()

    try:
        count = fix_reset_localstorage_keys()
        print(f"\nScript completed! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
