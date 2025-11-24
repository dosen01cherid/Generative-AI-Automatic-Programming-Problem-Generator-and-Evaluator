#!/usr/bin/env python3
"""
Script to wire storage info update to reset page navigation
"""

import re

def wire_storage_info_to_nav():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find the navigation JavaScript code where pages are switched
    # Look for the part where targetPage.classList.add("active") is called
    # This is in the navigation event listener

    if 'page === "reset"' not in content:
        # Strategy: Find the navigation click handler and add reset page check
        # Look for pattern where page is shown
        patterns = [
            # Pattern 1: After targetPage is made active
            (r'(targetPage\.classList\.add\("active"\);?)(\s*})(\s*}\);)',
             r'\1\2\n\n          // Update storage info when opening reset page\n          if (page === "reset" && window.app) {\n            setTimeout(() => {\n              window.app.update_storage_info();\n            }, 100);\n          }\3'),

            # Pattern 2: After pages are hidden/shown
            (r'(pages\.forEach\(p => p\.classList\.remove\("active"\)\);?\s*if \(targetPage\) \{\s*targetPage\.classList\.add\("active"\);?)(\s*})',
             r'\1\n\n          // Update storage info when opening reset page\n          if (page === "reset" && window.app) {\n            setTimeout(() => {\n              window.app.update_storage_info();\n            }, 100);\n          }\2'),
        ]

        for pattern, replacement in patterns:
            if re.search(pattern, content, re.DOTALL):
                content = re.sub(pattern, replacement, content, flags=re.DOTALL)
                updates_made.append("[OK] Added storage info update to navigation handler")
                break

        # If still not found, try a more generic approach
        if not updates_made:
            # Find the JavaScript section with navigation
            nav_pattern = r'(navItems\.forEach.*?addEventListener.*?const page = item\.getAttribute\("data-page"\);)'
            match = re.search(nav_pattern, content, re.DOTALL)

            if match:
                # Find the end of this event handler (look for closing braces)
                start = match.end()
                # Look for where targetPage.classList.add is called
                section = content[start:start+2000]  # Look ahead
                add_active_match = re.search(r'targetPage\.classList\.add\("active"\);?', section)

                if add_active_match:
                    insert_pos = start + add_active_match.end()

                    storage_check = '''

          // Update storage info when opening reset page
          if (page === "reset" && window.app) {
            setTimeout(() => {
              window.app.update_storage_info();
            }, 100);
          }'''

                    content = content[:insert_pos] + storage_check + content[insert_pos:]
                    updates_made.append("[OK] Added storage info update to navigation (generic method)")

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
        print("\nNo changes needed - navigation handler already exists!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Wire Storage Info to Navigation Script")
    print("="*60)
    print("Adds storage info update when reset page is opened")
    print()

    try:
        count = wire_storage_info_to_nav()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
