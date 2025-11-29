#!/usr/bin/env python3
"""
Script to add JavaScript event handlers for reset functionality
"""

import re

def add_reset_handlers():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find where other button handlers are registered (after exportProgressBtn)
    # Look for the export button handler
    export_handler_pattern = r'(app\.setup_export_handler\(\).*?$)'

    # Add reset button handlers after export handler setup
    if 'setup_reset_handlers' not in content:
        # Find setup_export_handler call and add reset handlers after it
        match = re.search(r'app\.setup_export_handler\(\)', content, re.MULTILINE)
        if match:
            insert_pos = match.end()
            reset_handler_call = '\n        app.setup_reset_handlers()\n        app.update_storage_info()'

            content = content[:insert_pos] + reset_handler_call + content[insert_pos:]
            updates_made.append("[OK] Added reset handlers call in initialization")

    # Add the setup_reset_handlers method to the Python class
    if 'def setup_reset_handlers' not in content:
        # Find a good place - after setup_export_handler
        export_method_pos = content.find('def setup_export_handler(self):')
        if export_method_pos > 0:
            # Find the end of setup_export_handler method (next def or class end)
            next_def_pos = content.find('\n    def ', export_method_pos + 1)
            if next_def_pos > 0:
                reset_handler_method = '''
    def setup_reset_handlers(self):
        """Setup event handlers for reset buttons"""
        # Reset All button
        reset_all_btn = document.querySelector("#resetAllBtn")
        if reset_all_btn:
            def handle_reset_all(e):
                # Show confirmation dialog
                confirmed = window.confirm(
                    "⚠️ WARNING: This will delete ALL your saved answers and progress!\\n\\n"
                    "This action cannot be undone.\\n\\n"
                    "Are you sure you want to continue?"
                )
                if confirmed:
                    self.reset_all_answers()
            reset_all_btn.addEventListener("click", create_proxy(handle_reset_all))
            window.console.log("✅ Reset All handler attached")

        # Reset Current Problem button
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
            window.console.log("✅ Reset Current Problem handler attached")

    def update_storage_info(self):
        """Update the storage info display"""
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
                content = content[:next_def_pos] + reset_handler_method + content[next_def_pos:]
                updates_made.append("[OK] Added setup_reset_handlers method")

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
        print("\nNo changes needed - Reset handlers already exist!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Add Reset Handlers Script")
    print("="*60)
    print("Adds event handlers for reset functionality")
    print()

    try:
        count = add_reset_handlers()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
