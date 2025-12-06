# -*- coding: utf-8 -*-
import codecs

with codecs.open('solve_problem.html', 'r', encoding='utf-8') as f:
    content = f.read()

old = """            if feedback_el:
                feedback_el.innerHTML = f\"\"\"
                <div style='color:#6366f1;background:#e0e7ff;padding:16px;border-radius:8px;border-left:4px solid #6366f1;'>
                    <div style='font-weight:700;font-size:16px;margin-bottom:12px;'>💡 Solution:</div>
                    <div style='font-size:20px;margin-bottom:8px;'>$$\\displaystyle {solution_latex}$$</div>
                    <div style='font-size:14px;color:#4338ca;margin-top:8px;'>You can study this solution and try a similar problem next time!</div>
                </div>
                \"\"\"

                # Re-render MathJax
                if hasattr(window, 'MathJax') and hasattr(window.MathJax, 'typesetPromise'):
                    window.MathJax.typesetPromise([feedback_el])"""

new = """            if feedback_el:
                solution_section = f\"\"\"
                <div style='color:#6366f1;background:#e0e7ff;padding:16px;border-radius:8px;border-left:4px solid #6366f1;margin-bottom:16px;'>
                    <div style='font-weight:700;font-size:16px;margin-bottom:12px;'>💡 Solution:</div>
                    <div style='font-size:20px;margin-bottom:8px;'>$$\\displaystyle {solution_latex}$$</div>
                </div>
                \"\"\"

                if steps_html:
                    feedback_el.innerHTML = solution_section + f\"\"\"
                    <div style='background:#f0f9ff;padding:16px;border-radius:8px;border-left:4px solid #3b82f6;'>
                        <div style='font-weight:700;font-size:16px;margin-bottom:12px;color:#1e40af;'>📚 Step-by-Step Solution:</div>
                        {steps_html}
                    </div>
                    \"\"\"
                else:
                    feedback_el.innerHTML = solution_section

                # Re-render MathJax
                if hasattr(window, 'MathJax') and hasattr(window.MathJax, 'typesetPromise'):
                    window.MathJax.typesetPromise([feedback_el])"""

if old in content:
    content = content.replace(old, new)
    print("OK: Updated feedback HTML")
else:
    print("ERROR: Could not find HTML")

with codecs.open('solve_problem.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
