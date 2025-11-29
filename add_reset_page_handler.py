#!/usr/bin/env python3
"""
Script to add reset page handler to show_page method
"""

import re

def add_reset_page_handler():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find the show_page method where freestyle initialization happens
    # Add similar logic for reset page
    if 'page_name == "reset"' not in content:
        # Pattern: Find the freestyle initialization block and add reset after it
        pattern = r'(if page_name == "freestyle":\s+def delayed_init\(\):\s+self\.ensure_freestyle_initialized\(\)\s+window\.setTimeout\(create_proxy\(delayed_init\), 100\))\s+(self\.close_sidebar\(None\))'

        if re.search(pattern, content):
            replacement = r'''\1

        if page_name == "reset":
          def delayed_update():
              self.update_storage_info()
          window.setTimeout(create_proxy(delayed_update), 100)

        \2'''

            content = re.sub(pattern, replacement, content)
            updates_made.append("[OK] Added reset page handler to show_page method")
        else:
            # Try alternative approach - find all occurrences
            # There might be multiple show_page methods
            pattern2 = r'(if page_name == "freestyle":\n\s+# Use setTimeout.*?\n\s+def delayed_init\(\):\n\s+self\.ensure_freestyle_initialized\(\)\n\s+window\.setTimeout\(create_proxy\(delayed_init\), 100\))\n\n(\s+self\.close_sidebar\(None\))'

            if re.search(pattern2, content):
                replacement2 = r'''\1

        if page_name == "reset":
            def delayed_update():
                self.update_storage_info()
            window.setTimeout(create_proxy(delayed_update), 100)

\2'''

                content = re.sub(pattern2, replacement2, content)
                updates_made.append("[OK] Added reset page handler (method 2)")

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
        print("\nNo changes needed - reset page handler already exists or pattern not found!")
        # Debug: show what we're looking for
        print("\nSearching for pattern context...")
        if 'if page_name == "freestyle":' in content:
            idx = content.find('if page_name == "freestyle":')
            print(f"Found freestyle check at position {idx}")
            print("Context:")
            print(content[idx:idx+400])

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Add Reset Page Handler Script")
    print("="*60)
    print("Adds reset page handler to update storage info")
    print()

    try:
        count = add_reset_page_handler()
        print(f"\nScript completed! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
