#!/usr/bin/env python3
"""
Script to add update_storage_info method and wire it to reset page navigation
"""

import re

def add_storage_info_updater():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # 1. Add update_storage_info method after get_storage_info
    if 'def update_storage_info' not in content:
        # Find get_storage_info method end
        pattern = r'(def get_storage_info\(self\):.*?return \{\})\s*\n'
        match = re.search(pattern, content, re.DOTALL)

        if match:
            insert_pos = match.end()

            update_method = '''
    def update_storage_info(self):
        """Update the storage info display on reset page"""
        info_div = document.querySelector("#storageInfo")
        if not info_div:
            return

        try:
            info = self.get_storage_info()

            size_kb = info.get("problem_states_size", 0) / 1024

            html = f"""
                <div style='margin-bottom: 8px;'><strong>Problems with saved data:</strong> {info.get('problems_count', 0)}</div>
                <div style='margin-bottom: 8px;'><strong>Total steps saved:</strong> {info.get('total_steps', 0)}</div>
                <div style='margin-bottom: 8px;'><strong>Completed problems:</strong> {info.get('completed_problems', 0)}</div>
                <div><strong>Storage size:</strong> {size_kb:.2f} KB</div>
            """

            info_div.innerHTML = html
            window.console.log("✅ Storage info updated")
        except Exception as e:
            info_div.innerHTML = f"<div style='color: #dc2626;'>Error loading storage info: {e}</div>"
            window.console.error(f"Error updating storage info: {e}")

'''
            content = content[:insert_pos] + update_method + content[insert_pos:]
            updates_made.append("[OK] Added update_storage_info method")

    # 2. Add navigation handler to call update_storage_info when reset page is opened
    # Look for where pages are switched in the navigation
    if 'page === "reset"' not in content:
        # Find the page switching logic
        pattern = r'(targetPage\.classList\.add\("active"\))'
        match = re.search(pattern, content)

        if match:
            insert_pos = match.end()

            nav_handler = '''

            // Update storage info when opening reset page
            if (page === "reset" && window.app) {
              setTimeout(() => {
                window.app.update_storage_info();
              }, 100);
            }'''

            content = content[:insert_pos] + nav_handler + content[insert_pos:]
            updates_made.append("[OK] Added reset page navigation handler to update storage info")

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
        print("\nNo changes needed - update_storage_info already exists!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Add Storage Info Updater Script")
    print("="*60)
    print("Adds update_storage_info method and wires it to reset page")
    print()

    try:
        count = add_storage_info_updater()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
