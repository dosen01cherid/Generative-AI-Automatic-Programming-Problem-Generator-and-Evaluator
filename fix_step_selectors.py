#!/usr/bin/env python3
"""
Script to fix step selector issues in solve_problem.html
Updates selectors to include problem index: step{index}_{step_idx}
"""

import re

def fix_step_selectors():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Fix 1: Line 10427 - submit_mc_multiple selector
    # selector = f"#step{step_idx}" -> selector = f"#step{current_prob_idx}_{step_idx}"
    pattern1 = r'def submit_mc_multiple\(self, step_idx, step_data\):\s+"""Submit multiple choice multiple answers"""\s+current_prob_idx = self\.current_problem_index\s+if current_prob_idx is None:\s+window\.console\.error\("❌ No current problem index"\)\s+return\s+window\.console\.log\(f"🔍 submit_mc_multiple called with step_idx=\{step_idx\}"\)\s+# Get the step container to scope the checkbox query\s+selector = f"#step\{step_idx\}"'
    replacement1 = r'''def submit_mc_multiple(self, step_idx, step_data):
        """Submit multiple choice multiple answers"""
        current_prob_idx = self.current_problem_index
        if current_prob_idx is None:
            window.console.error("❌ No current problem index")
            return

        window.console.log(f"🔍 submit_mc_multiple called with step_idx={step_idx}")

        # Get the step container to scope the checkbox query
        selector = f"#step{current_prob_idx}_{step_idx}"'''

    if re.search(r'selector = f"#step\{step_idx\}"', content):
        # More targeted fix
        content = content.replace(
            '# Get the step container to scope the checkbox query\n        selector = f"#step{step_idx}"',
            '# Get the step container to scope the checkbox query\n        selector = f"#step{current_prob_idx}_{step_idx}"'
        )
        updates_made.append("[OK] Fixed submit_mc_multiple selector (line 10427)")

    # Fix 2: Line 11088 - labeled_inputs selector in multi-blank mode
    # problem_container.querySelectorAll(f"#step{step_idx} [data-blank-label]")
    pattern2 = r'labeled_inputs = problem_container\.querySelectorAll\(f"#step\{step_idx\} \[data-blank-label\]"\)'
    replacement2 = r'labeled_inputs = problem_container.querySelectorAll(f"#step{current_prob_idx}_{step_idx} [data-blank-label]")'
    if re.search(pattern2, content):
        content = re.sub(pattern2, replacement2, content)
        updates_made.append("[OK] Fixed labeled_inputs selector (line 11088)")

    # Fix 3: Line 11123 - all_inputs selector in single-blank mode
    # all_inputs = problem_container.querySelectorAll(f"#step{step_idx} .fill-blank-input")
    pattern3 = r'all_inputs = problem_container\.querySelectorAll\(f"#step\{step_idx\} \.fill-blank-input"\)'
    replacement3 = r'all_inputs = problem_container.querySelectorAll(f"#step{current_prob_idx}_{step_idx} .fill-blank-input")'
    if re.search(pattern3, content):
        content = re.sub(pattern3, replacement3, content)
        updates_made.append("[OK] Fixed all_inputs selector (line 11123)")

    # Fix 4: Line 11121 - debug log selector
    # window.console.log(f"🐛 DEBUG: selector = .accordion-problem[data-index='{current_prob_idx}'] #step{step_idx} .fill-blank-input")
    pattern4 = r'window\.console\.log\(f"🐛 DEBUG: selector = \.accordion-problem\[data-index=\'\{current_prob_idx\}\'\] #step\{step_idx\} \.fill-blank-input"\)'
    replacement4 = r'window.console.log(f"🐛 DEBUG: selector = .accordion-problem[data-index=\'{current_prob_idx}\'] #step{current_prob_idx}_{step_idx} .fill-blank-input")'
    if re.search(pattern4, content):
        content = re.sub(pattern4, replacement4, content)
        updates_made.append("[OK] Fixed debug log selector (line 11121)")

    # Fix 5: Line 11281 - container selector in fill-blank error handling
    # container = problem_container.querySelector(f"#step{step_idx}")
    pattern5 = r'container = problem_container\.querySelector\(f"#step\{step_idx\}"\)'
    replacement5 = r'container = problem_container.querySelector(f"#step{current_prob_idx}_{step_idx}")'
    matches = re.findall(pattern5, content)
    if matches:
        content = re.sub(pattern5, replacement5, content)
        updates_made.append(f"[OK] Fixed {len(matches)} problem_container.querySelector selector(s)")

    # Fix 6: Line 11567 - container selector in multi-blank error handling
    # container = document.querySelector(f"#step{step_idx}")
    # Need to be careful - only fix the ones that should have current_prob_idx
    pattern6 = r'container = document\.querySelector\(f"#step\{step_idx\}"\)'
    if re.search(pattern6, content):
        # This is trickier because we need current_prob_idx context
        # Let's find these and replace them
        content = content.replace(
            'container = document.querySelector(f"#step{step_idx}")',
            'container = document.querySelector(f"#step{current_prob_idx}_{step_idx}")'
        )
        updates_made.append("[OK] Fixed document.querySelector selector for container")

    # Fix 7: Line 11289 - error message selector
    # window.console.error(f"❌ Fill-Blank: Container #step{step_idx} not found!")
    pattern7 = r'window\.console\.error\(f"❌ Fill-Blank: Container #step\{step_idx\} not found!"\)'
    replacement7 = r'window.console.error(f"❌ Fill-Blank: Container #step{current_prob_idx}_{step_idx} not found!")'
    if re.search(pattern7, content):
        content = re.sub(pattern7, replacement7, content)
        updates_made.append("[OK] Fixed Fill-Blank error message selector (line 11289)")

    # Fix 8: Line 11575 - error message selector in multi-blank
    # window.console.error(f"❌ Multi-Blank: Container #step{step_idx} not found!")
    pattern8 = r'window\.console\.error\(f"❌ Multi-Blank: Container #step\{step_idx\} not found!"\)'
    replacement8 = r'window.console.error(f"❌ Multi-Blank: Container #step{current_prob_idx}_{step_idx} not found!")'
    if re.search(pattern8, content):
        content = re.sub(pattern8, replacement8, content)
        updates_made.append("[OK] Fixed Multi-Blank error message selector (line 11575)")

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
    print("Step Selector Fix Script")
    print("="*60)
    print("This script fixes step selectors to include problem index")
    print()

    try:
        count = fix_step_selectors()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
