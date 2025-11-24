#!/usr/bin/env python3
"""
Script to add a "Reset Answers" menu item to the left panel navigation
This allows users to clear all autosaved answers from localStorage
"""

import re

def add_reset_menu():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Step 1: Add navigation menu item after "Submit Progress"
    nav_menu_pattern = r'(<div class="nav-item" data-page="export">.*?</div>)\s*</nav>'

    new_nav_item = '''<div class="nav-item" data-page="export">
            <span class="nav-icon">📤</span>
            <span>Submit Progress</span>
          </div>
          <div class="nav-item" data-page="reset" style="border-top: 1px solid #e5e7eb; margin-top: 8px; padding-top: 8px;">
            <span class="nav-icon">🔄</span>
            <span>Reset Answers</span>
          </div>
        </nav>'''

    if re.search(nav_menu_pattern, content, re.DOTALL):
        content = re.sub(
            r'(<div class="nav-item" data-page="export">.*?</div>)\s*</nav>',
            new_nav_item,
            content,
            flags=re.DOTALL
        )
        updates_made.append("[OK] Added Reset Answers navigation item")

    # Step 2: Add Reset Page HTML after Export Page
    export_page_pattern = r'(<!-- Export Page -->.*?</div>\s*</div>)\s*(</main>)'

    reset_page_html = '''<!-- Export Page -->
        <div id="exportPage" class="page">
          <div class="panel">
            <h3>📤 Submit Progress</h3>
            <button id="exportProgressBtn" class="btn" style="background: #10b981">📤 Export to File</button>

            <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #e5e7eb;">
              <h4 style="margin-bottom: 12px; color: #374151;">📱 Share via Messaging App</h4>
              <div style="display: flex; gap: 12px; flex-wrap: wrap;">
                <button id="shareWhatsAppBtn" class="btn" style="background: #25D366; color: white; flex: 1; min-width: 150px; display: flex; align-items: center; justify-content: center; gap: 8px;">'''

    if 'id="resetPage"' not in content:
        # Find the closing of exportPage and add resetPage before </main>
        reset_page = '''
        <!-- Reset Page -->
        <div id="resetPage" class="page">
          <div class="panel">
            <h3>🔄 Reset Answers</h3>
            <p style="margin-bottom: 16px; color: #6b7280;">
              This will clear all your saved answers and progress from the browser's local storage.
              <strong>This action cannot be undone.</strong>
            </p>

            <div style="background: #fef2f2; border: 2px solid #fca5a5; border-radius: 8px; padding: 16px; margin-bottom: 20px;">
              <h4 style="color: #dc2626; margin: 0 0 8px 0;">⚠️ Warning</h4>
              <p style="margin: 0; color: #991b1b; font-size: 14px;">
                Resetting will delete:
              </p>
              <ul style="margin: 8px 0 0 0; color: #991b1b; font-size: 14px;">
                <li>All problem answers</li>
                <li>All step completion status</li>
                <li>All attempt history and scores</li>
                <li>Timer data</li>
              </ul>
            </div>

            <div style="display: flex; gap: 12px; flex-direction: column;">
              <button id="resetAllBtn" class="btn" style="background: #dc2626; color: white; padding: 16px; font-size: 16px; font-weight: 600;">
                🗑️ Reset All Answers
              </button>

              <button id="resetCurrentProblemBtn" class="btn" style="background: #f59e0b; color: white; padding: 14px;">
                🔄 Reset Current Problem Only
              </button>
            </div>

            <div style="margin-top: 20px; padding-top: 20px; border-top: 2px solid #e5e7eb;">
              <h4 style="margin-bottom: 12px; color: #374151;">📊 Current Storage Info</h4>
              <div id="storageInfo" style="background: #f9fafb; border-radius: 8px; padding: 16px; font-family: monospace; font-size: 13px; color: #374151;">
                Loading storage information...
              </div>
            </div>
          </div>
        </div>
'''

        # Insert before </main>
        content = re.sub(
            r'(\s*</main>)',
            reset_page + r'\1',
            content
        )
        updates_made.append("[OK] Added Reset Page HTML")

    # Step 3: Add Python handler methods (find the class definition and add methods)
    # Find a good place to add the reset methods - after save_to_storage method
    if 'def reset_all_answers' not in content:
        save_method_end = content.find('def load_from_storage(self):')
        if save_method_end > 0:
            reset_methods = '''
    def reset_all_answers(self):
        """Reset all answers and progress"""
        import js
        try:
            window.console.log("🔄 Resetting all answers...")

            # Clear specific localStorage keys
            js.localStorage.removeItem('problem_states')
            js.localStorage.removeItem('compressed_problem_set')
            js.localStorage.removeItem('edited_problems')
            js.localStorage.removeItem('score_display_states')
            js.localStorage.removeItem('historical_edits')
            js.localStorage.removeItem('score_tracker_session')
            js.localStorage.removeItem('credit_count')
            js.localStorage.removeItem('pending_timer')

            window.console.log("✅ All localStorage data cleared")

            # Reset internal state
            self.problem_states = {}
            self.solve_states = {}
            if hasattr(self, 'step_timers'):
                self.step_timers = {}

            window.alert("✅ All answers and progress have been reset!\\n\\nPlease reload the page to start fresh.")

        except Exception as e:
            window.console.error(f"❌ Reset failed: {e}")
            window.alert(f"❌ Reset failed: {e}")

    def reset_current_problem(self):
        """Reset only the current problem's answers"""
        import js
        try:
            current_prob_idx = self.current_problem_index
            if current_prob_idx is None:
                window.alert("⚠️ No problem is currently open")
                return

            window.console.log(f"🔄 Resetting problem {current_prob_idx}...")

            # Remove from problem_states
            if current_prob_idx in self.problem_states:
                del self.problem_states[current_prob_idx]

            # Remove from solve_states
            if current_prob_idx in self.solve_states:
                del self.solve_states[current_prob_idx]

            # Save updated state
            self.save_to_storage()

            window.console.log(f"✅ Problem {current_prob_idx} reset")
            window.alert(f"✅ Problem {current_prob_idx + 1} has been reset!\\n\\nPlease reload the problem to start fresh.")

        except Exception as e:
            window.console.error(f"❌ Reset failed: {e}")
            window.alert(f"❌ Reset failed: {e}")

    def get_storage_info(self):
        """Get information about current localStorage usage"""
        import js
        try:
            info = {
                "problems_count": len(self.problem_states),
                "total_steps": sum(len(steps) for steps in self.problem_states.values()),
                "completed_problems": sum(1 for prob_idx in self.problem_states if self.is_problem_complete(prob_idx))
            }

            # Get localStorage sizes
            try:
                problem_states_str = js.localStorage.getItem('problem_states')
                if problem_states_str:
                    info["problem_states_size"] = len(problem_states_str)
            except:
                info["problem_states_size"] = 0

            return info
        except Exception as e:
            window.console.error(f"Error getting storage info: {e}")
            return {}

    '''

            content = content[:save_method_end] + reset_methods + content[save_method_end:]
            updates_made.append("[OK] Added reset handler methods to Python class")

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
        print("\nNo changes needed - Reset menu already exists or patterns not found!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Add Reset Menu Script")
    print("="*60)
    print("Adds a Reset Answers menu item to the left navigation panel")
    print()

    try:
        count = add_reset_menu()
        print(f"\nScript completed successfully! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
