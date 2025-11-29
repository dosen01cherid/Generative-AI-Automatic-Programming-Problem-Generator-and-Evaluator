#!/usr/bin/env python3
"""
Script to wire up reset button event handlers
"""

import re

def wire_reset_buttons():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find where export button handler is registered and add reset handlers after it
    # Pattern: export_btn = document.querySelector("#exportProgressBtn")...
    export_handler_pattern = r'(# Export button\s+export_btn = document\.querySelector\("#exportProgressBtn"\).*?export_btn\.addEventListener\("click", create_proxy\(lambda e: self\.export_progress\(e\)\)\))'

    if re.search(export_handler_pattern, content, re.DOTALL):
        if 'resetAllBtn' not in content or content.find('resetAllBtn') > content.find('export_btn = document'):
            # Find position after export button handler
            match = re.search(r'export_btn\.addEventListener\("click", create_proxy\(lambda e: self\.export_progress\(e\)\)\)', content)
            if match:
                insert_pos = match.end()

                reset_handlers = '''

        # Reset buttons
        reset_all_btn = document.querySelector("#resetAllBtn")
        if reset_all_btn:
            def handle_reset_all(e):
                confirmed = window.confirm(
                    "⚠️ WARNING: This will delete ALL your saved answers and progress!\\n\\n"
                    "This action cannot be undone.\\n\\n"
                    "Are you sure you want to continue?"
                )
                if confirmed:
                    self.reset_all_answers()
            reset_all_btn.addEventListener("click", create_proxy(handle_reset_all))
            window.console.log("✅ Reset All button handler attached")

        reset_current_btn = document.querySelector("#resetCurrentProblemBtn")
        if reset_current_btn:
            def handle_reset_current(e):
                current_prob_idx = self.current_problem_index
                if current_prob_idx is None:
                    window.alert("⚠️ Please open a problem first")
                    return

                confirmed = window.confirm(
                    f"⚠️ This will reset Problem {current_prob_idx + 1}\\n\\n"
                    "All answers and progress for this problem will be deleted.\\n\\n"
                    "Continue?"
                )
                if confirmed:
                    self.reset_current_problem()
            reset_current_btn.addEventListener("click", create_proxy(handle_reset_current))
            window.console.log("✅ Reset Current Problem button handler attached")

        # Update storage info when reset page is opened
        window.console.log("✅ Reset button handlers registered")'''

                content = content[:insert_pos] + reset_handlers + content[insert_pos:]
                updates_made.append("[OK] Added reset button event handlers")

    # Add storage info update when navigating to reset page
    # Find the navigation handler section
    if 'data-page="reset"' in content:
        nav_handler_pattern = r'(navItems\.forEach\(.*?function.*?\{.*?navItems\.forEach.*?classList\.remove.*?\n.*?item\.classList\.add.*?\n.*?const page = item\.getAttribute.*?\n.*?pages\.forEach.*?classList\.remove.*?\n.*?targetPage = document\.querySelector.*?\n.*?targetPage\.classList\.add)'

        # Find where pages are shown/hidden and add storage update for reset page
        if 'update_storage_info' in content and 'if (page === "reset")' not in content:
            # Find where page switching happens
            page_switch_pattern = r'(targetPage\.classList\.add\("active"\))'
            match = re.search(page_switch_pattern, content)
            if match:
                insert_pos = match.end()
                storage_update_code = '''

                // Update storage info when opening reset page
                if (page === "reset" && window.app) {
                  setTimeout(() => {
                    window.app.update_storage_info();
                  }, 100);
                }'''

                content = content[:insert_pos] + storage_update_code + content[insert_pos:]
                updates_made.append("[OK] Added storage info update on reset page open")

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
        print("\nNo changes needed - Reset button handlers already wired!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Wire Reset Buttons Script")
    print("="*60)
    print("Wires up event handlers for reset buttons")
    print()

    try:
        count = wire_reset_buttons()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
