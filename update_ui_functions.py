#!/usr/bin/env python3
"""
Script to update function signatures and calls in solve_problem.html
Adds 'index' parameter to UI creation methods for consistency
"""

import re

def update_solve_problem_html():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # 1. Update function signature for create_mc_multiple_ui
    pattern1 = r'def create_mc_multiple_ui\(self, step_div, step_idx,'
    replacement1 = r'def create_mc_multiple_ui(self, step_div, index, step_idx,'
    if re.search(pattern1, content):
        content = re.sub(pattern1, replacement1, content)
        updates_made.append("✓ Updated create_mc_multiple_ui signature")

    # 2. Update function signature for create_fill_blank_ui
    pattern2 = r'def create_fill_blank_ui\(self, step_div, step_idx,'
    replacement2 = r'def create_fill_blank_ui(self, step_div, index, step_idx,'
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        updates_made.append("✓ Updated create_fill_blank_ui signature")

    # 3. Update function signature for create_multi_mc_ui
    pattern3 = r'def create_multi_mc_ui\(self, step_div, step_idx,'
    replacement3 = r'def create_multi_mc_ui(self, step_div, index, step_idx,'
    if re.search(pattern3, content):
        content = re.sub(pattern3, replacement3, content)
        updates_made.append("✓ Updated create_multi_mc_ui signature")

    # 4. Update function signature for create_truefalse_ui
    pattern4 = r'def create_truefalse_ui\(self, step_div, step_idx,'
    replacement4 = r'def create_truefalse_ui(self, step_div, index, step_idx,'
    if re.search(pattern4, content):
        content = re.sub(pattern4, replacement4, content)
        updates_made.append("✓ Updated create_truefalse_ui signature")

    # 5. Update call site for create_mc_multiple_ui (line ~10582)
    # Pattern: self.create_mc_multiple_ui(container, step_idx, step_data, ...
    # Need to add index before step_idx
    pattern5 = r'self\.create_mc_multiple_ui\(container, step_idx, step_data,'
    replacement5 = r'self.create_mc_multiple_ui(container, index, step_idx, step_data,'
    if re.search(pattern5, content):
        content = re.sub(pattern5, replacement5, content)
        updates_made.append("✓ Updated create_mc_multiple_ui call site (shuffle)")

    # 6. Update call site for create_multi_mc_ui (line ~10815)
    pattern6 = r'self\.create_multi_mc_ui\(container, step_idx, step_data,'
    replacement6 = r'self.create_multi_mc_ui(container, index, step_idx, step_data,'
    if re.search(pattern6, content):
        content = re.sub(pattern6, replacement6, content)
        updates_made.append("✓ Updated create_multi_mc_ui call site (shuffle)")

    # Check if any changes were made
    if content != original_content:
        print(f"\nWriting updated content to {file_path}...")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)

        print("\n" + "="*60)
        print("Updates completed successfully!")
        print("="*60)
        for update in updates_made:
            # Use ASCII-compatible checkmark for Windows console
            print(update.replace('✓', '[OK]'))
        print(f"\nTotal updates: {len(updates_made)}")
    else:
        print("\nNo changes needed - all patterns already updated!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("UI Function Update Script")
    print("="*60)
    print("This script adds 'index' parameter to UI creation methods")
    print()

    try:
        count = update_solve_problem_html()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
