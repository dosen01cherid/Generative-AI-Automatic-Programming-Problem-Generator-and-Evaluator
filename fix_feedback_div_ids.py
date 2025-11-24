#!/usr/bin/env python3
"""
Script to fix feedback div ID issues in solve_problem.html
Updates feedback div IDs to include problem index: stepFeedback{index}_{step_idx}
"""

import re

def fix_feedback_div_ids():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Fix 1: Update feedback div IDs in UI creation functions
    # In create_*_ui functions, replace: id='stepFeedback{step_idx}'
    # with: id='stepFeedback{index}_{step_idx}'

    # Pattern for feedback divs in HTML templates
    pattern1 = r"<div id='stepFeedback\{step_idx\}'"
    replacement1 = r"<div id='stepFeedback{index}_{step_idx}'"
    matches1 = re.findall(pattern1, content)
    if matches1:
        content = re.sub(pattern1, replacement1, content)
        updates_made.append(f"[OK] Fixed {len(matches1)} feedback div ID(s) in UI creation")

    # Fix 2: Update querySelector calls that need current_prob_idx
    # We need to be more selective here - some already use problem_container scope

    # Pattern: querySelector(f"#stepFeedback{step_idx}") in submit functions
    # where current_prob_idx is available

    # First, let's find and replace in contexts where we have current_prob_idx
    # Pattern: problem_container.querySelector(f"#stepFeedback{step_idx}")
    pattern2 = r'problem_container\.querySelector\(f"#stepFeedback\{step_idx\}"\)'
    replacement2 = r'problem_container.querySelector(f"#stepFeedback{current_prob_idx}_{step_idx}")'
    matches2 = re.findall(pattern2, content)
    if matches2:
        content = re.sub(pattern2, replacement2, content)
        updates_made.append(f"[OK] Fixed {len(matches2)} problem_container.querySelector for feedback")

    # Pattern: document.querySelector(f"#stepFeedback{step_idx}")
    # These should also use current_prob_idx
    pattern3 = r'document\.querySelector\(f"#stepFeedback\{step_idx\}"\)'
    replacement3 = r'document.querySelector(f"#stepFeedback{current_prob_idx}_{step_idx}")'
    matches3 = re.findall(pattern3, content)
    if matches3:
        content = re.sub(pattern3, replacement3, content)
        updates_made.append(f"[OK] Fixed {len(matches3)} document.querySelector for feedback")

    # Pattern: container.querySelector(f"#stepFeedback{step_idx}")
    # These also need current_prob_idx
    pattern4 = r'container\.querySelector\(f"#stepFeedback\{step_idx\}"\)'
    replacement4 = r'container.querySelector(f"#stepFeedback{current_prob_idx}_{step_idx}")'
    matches4 = re.findall(pattern4, content)
    if matches4:
        content = re.sub(pattern4, replacement4, content)
        updates_made.append(f"[OK] Fixed {len(matches4)} container.querySelector for feedback")

    # Fix 3: Update feedback_div.id assignments when creating new feedback divs
    # Pattern: feedback_div.id = f"stepFeedback{step_idx}"
    pattern5 = r'feedback_div\.id = f"stepFeedback\{step_idx\}"'
    replacement5 = r'feedback_div.id = f"stepFeedback{current_prob_idx}_{step_idx}"'
    matches5 = re.findall(pattern5, content)
    if matches5:
        content = re.sub(pattern5, replacement5, content)
        updates_made.append(f"[OK] Fixed {len(matches5)} feedback_div.id assignment(s)")

    # Fix 4: Update any .querySelector calls with just step_idx that should have index
    # Pattern with 'if problem_container else None' context
    pattern6 = r'problem_container\.querySelector\(f"#stepFeedback\{step_idx\}"\) if problem_container else None'
    replacement6 = r'problem_container.querySelector(f"#stepFeedback{current_prob_idx}_{step_idx}") if problem_container else None'
    # This was already handled by pattern2, but let's be explicit

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
        print(f"\nTotal update categories: {len(updates_made)}")
    else:
        print("\nNo changes needed - all patterns already updated!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Feedback Div ID Fix Script")
    print("="*60)
    print("This script fixes feedback div IDs to include problem index")
    print()

    try:
        count = fix_feedback_div_ids()
        print(f"\nScript completed successfully! ({count} update categories)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
