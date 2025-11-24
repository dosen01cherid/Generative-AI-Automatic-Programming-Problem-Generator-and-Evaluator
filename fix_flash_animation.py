#!/usr/bin/env python3
"""
Script to fix flashing notification animation in mc-multiple requireCorrect handling
The issue: When UI is recreated, feedback is added with flash class already present,
preventing the CSS animation from triggering.

Solution: Add flash class after a brief delay to trigger animation.
"""

import re

def fix_flash_animation():
    file_path = "solve_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # Find the section where feedback is displayed for requireCorrect error
    # We need to change how the flash-incorrect class is applied

    # Pattern: The current code sets innerHTML with flash-incorrect class already present
    old_pattern = r"""                feedback_div\.innerHTML = error_html

                # Remove flashing class after animation completes
                def remove_flash_mc_req\(\):
                    flash_div = feedback_div\.querySelector\("\.flash-incorrect"\)
                    if flash_div:
                        flash_div\.classList\.remove\("flash-incorrect"\)
                window\.setTimeout\(create_proxy\(remove_flash_mc_req\), 3000\)
                window\.console\.log\("✅ Displayed requireCorrect error message to user"\)"""

    # New pattern: Set innerHTML without flash class, then add it after a delay
    new_pattern = r"""                # Set innerHTML first (without flash-incorrect class temporarily)
                temp_error_html = error_html.replace("class='flash-incorrect'", "class='temp-no-flash'")
                feedback_div.innerHTML = temp_error_html

                # Add flash class after brief delay to trigger animation
                def add_flash_class():
                    flash_div = feedback_div.querySelector(".temp-no-flash")
                    if flash_div:
                        flash_div.classList.remove("temp-no-flash")
                        flash_div.classList.add("flash-incorrect")
                        window.console.log("✅ Added flash-incorrect class to trigger animation")
                window.setTimeout(create_proxy(add_flash_class), 50)

                # Remove flashing class after animation completes
                def remove_flash_mc_req():
                    flash_div = feedback_div.querySelector(".flash-incorrect")
                    if flash_div:
                        flash_div.classList.remove("flash-incorrect")
                window.setTimeout(create_proxy(remove_flash_mc_req), 3050)
                window.console.log("✅ Displayed requireCorrect error message to user")"""

    if re.search(re.escape(old_pattern), content):
        content = content.replace(old_pattern, new_pattern)
        updates_made.append("[OK] Fixed flash animation triggering for mc-multiple requireCorrect")
    else:
        print("Pattern not found - trying alternative approach...")

        # Alternative: Just look for the specific line and fix it differently
        # Find the line where innerHTML is set
        pattern1 = r'(feedback_div\.innerHTML = error_html\s+# Remove flashing class)'
        if re.search(pattern1, content):
            # Insert code to trigger animation properly
            replacement = r'''# Set innerHTML without flash class initially
                temp_html = error_html.replace("flash-incorrect", "temp-no-flash")
                feedback_div.innerHTML = temp_html

                # Trigger animation by adding flash class after element is rendered
                def trigger_flash():
                    elem = feedback_div.querySelector(".temp-no-flash")
                    if elem:
                        elem.classList.remove("temp-no-flash")
                        elem.classList.add("flash-incorrect")
                window.setTimeout(create_proxy(trigger_flash), 50)

                # Remove flashing class'''

            content = re.sub(pattern1, replacement, content)
            updates_made.append("[OK] Fixed flash animation (alternative method)")

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
        print("\nNo changes made - pattern not found or already fixed!")
        print("Let me show you what I was looking for...")
        # Search for the area
        if "feedback_div.innerHTML = error_html" in content:
            idx = content.find("feedback_div.innerHTML = error_html")
            print(f"\nFound at position {idx}")
            print("Context:")
            print(content[max(0, idx-200):idx+400])

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Flash Animation Fix Script")
    print("="*60)
    print("Fixes flash animation not triggering in mc-multiple requireCorrect")
    print()

    try:
        count = fix_flash_animation()
        print(f"\nScript completed! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
