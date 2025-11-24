#!/usr/bin/env python3
"""
Script to fix incorrect 'index' parameter usage in UI recreation calls
When reshuffling, the code calls create_*_ui(container, index, ...) but
'index' variable doesn't exist in submit functions - should use current_prob_idx
"""

import re

def fix_index_parameter_calls():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Fix 1: In submit_mc_multiple, line ~10592
    # self.create_mc_multiple_ui(container, index, step_idx, step_data, desc_html, total_steps)
    # Should be: self.create_mc_multiple_ui(container, current_prob_idx, step_idx, step_data, desc_html, total_steps)
    pattern1 = r'self\.create_mc_multiple_ui\(container, index, step_idx, step_data, desc_html, total_steps\)'
    replacement1 = r'self.create_mc_multiple_ui(container, current_prob_idx, step_idx, step_data, desc_html, total_steps)'
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        updates_made.append("[OK] Fixed create_mc_multiple_ui call in submit_mc_multiple (shuffle)")

    # Fix 2: In submit_multi_mc, similar issue
    # self.create_multi_mc_ui(container, index, step_idx, step_data, desc_html, total_steps)
    pattern2 = r'self\.create_multi_mc_ui\(container, index, step_idx, step_data, desc_html, total_steps\)'
    replacement2 = r'self.create_multi_mc_ui(container, current_prob_idx, step_idx, step_data, desc_html, total_steps)'
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        updates_made.append("[OK] Fixed create_multi_mc_ui call in submit_multi_mc (shuffle)")

    # Fix 3: Check for any other create_*_ui calls with 'index' in submit functions
    # Pattern: self.create_*_ui(container, index,
    pattern3 = r'self\.create_\w+_ui\(container, index,'
    matches = re.findall(pattern3, content)
    if matches:
        print(f"\nFound {len(matches)} additional create_*_ui calls with 'index' parameter:")
        for match in matches:
            print(f"  - {match}")

        # Replace all occurrences
        content = re.sub(r'(self\.create_\w+_ui\(container,) index,', r'\1 current_prob_idx,', content)
        updates_made.append(f"[OK] Fixed {len(matches)} additional create_*_ui call(s)")

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
        print("\nNo changes needed - all patterns already updated!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Index Parameter Fix Script")
    print("="*60)
    print("Fixes incorrect 'index' usage in UI recreation during reshuffling")
    print()

    try:
        count = fix_index_parameter_calls()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
