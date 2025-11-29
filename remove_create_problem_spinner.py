#!/usr/bin/env python3
"""
Script to remove the loading spinner/overlay from create_problem.html
"""

import re

def remove_create_problem_spinner():
    file_path = "create_problem.html"

    print(f"Reading {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    original_content = content
    updates_made = []

    # 1. Comment out the loading overlay HTML
    overlay_html_pattern = r'(  <!-- Loading Overlay -->\s*<div id="loadingOverlay">.*?</div>\s*</div>)'

    if re.search(overlay_html_pattern, content, re.DOTALL):
        replacement = r'''  <!-- Loading Overlay - DISABLED
  <div id="loadingOverlay">
    <div class="spinner"></div>
    <div class="loading-text">Initializing Problem Creator...</div>
    <div id="loadingStatus"><div>⏳ Starting up...</div></div>
  </div>
  -->'''

        content = re.sub(overlay_html_pattern, replacement, content, flags=re.DOTALL)
        updates_made.append("[OK] Commented out loading overlay HTML")

    # 2. Comment out the CSS for loading overlay (optional, but cleaner)
    css_pattern = r'(/\* Loading overlay \*/\s*#loadingOverlay \{[^}]+\})'

    if re.search(css_pattern, content, re.DOTALL):
        content = re.sub(
            css_pattern,
            r'/* Loading overlay - DISABLED \1 */',
            content,
            flags=re.DOTALL
        )
        updates_made.append("[OK] Commented out loading overlay CSS")

    # 3. Comment out the spinner CSS
    spinner_css_pattern = r'(\.spinner \{[^}]+\})'

    if re.search(spinner_css_pattern, content, re.DOTALL):
        content = re.sub(
            spinner_css_pattern,
            r'/* DISABLED - .spinner { ... } */',
            content,
            flags=re.DOTALL
        )
        updates_made.append("[OK] Commented out spinner CSS")

    # 4. Comment out the code that removes the overlay
    remove_overlay_pattern = r'(    overlay = document\.querySelector\("#loadingOverlay"\)\s+if overlay:\s+overlay\.style\.opacity = "0"\s+window\.setTimeout\(create_proxy\(lambda: overlay\.remove\(\)\), 400\))'

    if re.search(remove_overlay_pattern, content, re.DOTALL):
        content = re.sub(
            remove_overlay_pattern,
            r'''    # Loading overlay removal - DISABLED (overlay removed from HTML)
    # overlay = document.querySelector("#loadingOverlay")
    # if overlay:
    #     overlay.style.opacity = "0"
    #     window.setTimeout(create_proxy(lambda: overlay.remove()), 400)''',
            content,
            flags=re.DOTALL
        )
        updates_made.append("[OK] Commented out overlay removal code")

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
        print("\nNOTE: Loading spinner will no longer be displayed!")
    else:
        print("\nNo changes made - patterns not found or already disabled!")

    return len(updates_made)

if __name__ == "__main__":
    print("="*60)
    print("Remove Create Problem Loading Spinner")
    print("="*60)
    print("Removes the whirling progress circle from create_problem.html")
    print()

    try:
        count = remove_create_problem_spinner()
        print(f"\nScript completed! ({count} updates)")
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
