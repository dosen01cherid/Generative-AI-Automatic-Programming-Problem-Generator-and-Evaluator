# -*- coding: utf-8 -*-
"""Fix freestyle_giveup to use proper equation solving with step-by-step solution"""

import codecs

# Read the file
with codecs.open('solve_problem.html', 'r', encoding='utf-8') as f:
    content = f.read()

print("Fixing equation solver in freestyle_giveup...")

# The current code at line ~17017-17019 does:
# solution_expr = self.math_parser.normalize_expr(self.freestyle_problem["parsed"])
# solution_latex = sp.latex(solution_expr)

# We need to replace it to:
# 1. Detect if it's an equation (has sp.Equality)
# 2. If yes, solve it and show all solutions
# 3. Also generate step-by-step solution

old_code = """            # Get the solution by normalizing the problem
            solution_expr = self.math_parser.normalize_expr(self.freestyle_problem["parsed"])
            solution_latex = sp.latex(solution_expr)

            window.console.log(f"Solution: {solution_expr}")
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

new_code = """            # Get the parsed expression
            parsed_expr = self.freestyle_problem["parsed"]
            problem_latex = self.freestyle_problem["latex"]

            # Check if it's an equation to solve
            if isinstance(parsed_expr, sp.Equality):
                # It's an equation - solve it!
                var = list(parsed_expr.free_symbols)[0] if parsed_expr.free_symbols else None

                if var:
                    try:
                        solutions = sp.solve(parsed_expr, var)

                        window.console.log(f"Solutions: {solutions}")

                        # Build solution display
                        if len(solutions) == 1:
                            solution_latex = f"{sp.latex(var)} = {sp.latex(solutions[0])}"
                        elif len(solutions) > 1:
                            solution_parts = [f"{sp.latex(var)} = {sp.latex(sol)}" for sol in solutions]
                            solution_latex = " \\\\text{ or } ".join(solution_parts)
                        else:
                            solution_latex = "\\\\text{No solution}"

                        solution_expr = solutions  # Store all solutions
                    except Exception as solve_err:
                        window.console.error(f"Error solving equation: {solve_err}")
                        solution_latex = sp.latex(parsed_expr)
                        solution_expr = parsed_expr
                else:
                    solution_latex = sp.latex(parsed_expr)
                    solution_expr = parsed_expr
            else:
                # Not an equation - just simplify/normalize
                solution_expr = self.math_parser.normalize_expr(parsed_expr)
                solution_latex = sp.latex(solution_expr)

            window.console.log(f"Solution: {solution_expr}")
            window.console.log(f"Solution LaTeX: {solution_latex}")

            # Generate step-by-step solution
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

# Replace the code
if old_code in content:
    content = content.replace(old_code, new_code)
    print("✓ Successfully replaced equation solving code")
else:
    print("✗ Could not find exact match for old code")
    print("Trying partial replacement...")

    # Try replacing just the key part
    partial_old = "solution_expr = self.math_parser.normalize_expr(self.freestyle_problem[\"parsed\"])"
    partial_new = """parsed_expr = self.freestyle_problem["parsed"]
            problem_latex = self.freestyle_problem["latex"]

            # Check if it's an equation to solve
            if isinstance(parsed_expr, sp.Equality):
                # It's an equation - solve it!
                var = list(parsed_expr.free_symbols)[0] if parsed_expr.free_symbols else None

                if var:
                    try:
                        solutions = sp.solve(parsed_expr, var)

                        window.console.log(f"Solutions: {solutions}")

                        # Build solution display
                        if len(solutions) == 1:
                            solution_latex = f"{sp.latex(var)} = {sp.latex(solutions[0])}"
                        elif len(solutions) > 1:
                            solution_parts = [f"{sp.latex(var)} = {sp.latex(sol)}" for sol in solutions]
                            solution_latex = " \\\\text{ or } ".join(solution_parts)
                        else:
                            solution_latex = "\\\\text{No solution}"

                        solution_expr = solutions
                    except Exception as solve_err:
                        window.console.error(f"Error solving equation: {solve_err}")
                        solution_latex = sp.latex(parsed_expr)
                        solution_expr = parsed_expr
                else:
                    solution_latex = sp.latex(parsed_expr)
                    solution_expr = parsed_expr
            else:
                # Not an equation - just simplify/normalize
                solution_expr = self.math_parser.normalize_expr(parsed_expr)"""

    if partial_old in content:
        content = content.replace(partial_old, partial_new)
        print("✓ Partial replacement successful")
    else:
        print("✗ Could not find code to replace")

# Write the fixed content
with codecs.open('solve_problem.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("\nFile updated successfully!")
