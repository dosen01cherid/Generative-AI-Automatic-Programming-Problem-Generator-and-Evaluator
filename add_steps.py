# -*- coding: utf-8 -*-
import codecs

with codecs.open('solve_problem.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Find where we display the solution and add step-by-step generation before it
# Look for the feedback display section in freestyle_giveup

old_feedback = """            window.console.log(f"Solution: {solution_expr}")
            window.console.log(f"Solution LaTeX: {solution_latex}")

            # Display the solution
            feedback_el = document.querySelector("#freestyleFeedback")
            if feedback_el:
                feedback_el.innerHTML = f\"\"\"
                <div style='color:#6366f1;background:#e0e7ff;padding:16px;border-radius:8px;border-left:4px solid #6366f1;'>
                    <div style='font-weight:700;font-size:16px;margin-bottom:12px;'>💡 Solution:</div>
                    <div style='font-size:20px;margin-bottom:8px;'>$$\\\\displaystyle {solution_latex}$$</div>
                    <div style='font-size:14px;color:#4338ca;margin-top:8px;'>You can study this solution and try a similar problem next time!</div>
                </div>
                \"\"\"

                # Re-render MathJax
                if hasattr(window, 'MathJax') and hasattr(window.MathJax, 'typesetPromise'):
                    window.MathJax.typesetPromise([feedback_el])"""

new_feedback = """            window.console.log(f"Solution: {solution_expr}")
            window.console.log(f"Solution LaTeX: {solution_latex}")

            # Generate step-by-step solution
            problem_latex = self.freestyle_problem["latex"]
            try:
                steps = self.generate_step_by_step_solution(problem_latex, parsed_expr)
                steps_html = ""
                for step in steps:
                    steps_html += '<div style="margin-bottom:12px;">'
                    steps_html += f'<div style="margin-bottom:4px;">{step["explanation"]}</div>'
                    if step.get("math") and step["math"].strip():
                        steps_html += f'<div style="font-size:18px;margin:8px 0;">$$\\\\displaystyle {step["math"]}$$</div>'
                    steps_html += '</div>'
            except Exception as step_err:
                window.console.error(f"Error generating steps: {step_err}")
                import traceback
                window.console.error(traceback.format_exc())
                steps_html = ""

            # Display the solution
            feedback_el = document.querySelector("#freestyleFeedback")
            if feedback_el:
                solution_section = f\"\"\"
                <div style='color:#6366f1;background:#e0e7ff;padding:16px;border-radius:8px;border-left:4px solid #6366f1;margin-bottom:16px;'>
                    <div style='font-weight:700;font-size:16px;margin-bottom:12px;'>💡 Solution:</div>
                    <div style='font-size:20px;margin-bottom:8px;'>$$\\\\displaystyle {solution_latex}$$</div>
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

if old_feedback in content:
    content = content.replace(old_feedback, new_feedback)
    print("OK: Added step-by-step solution generation")
else:
    print("ERROR: Could not find feedback display code")

with codecs.open('solve_problem.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
