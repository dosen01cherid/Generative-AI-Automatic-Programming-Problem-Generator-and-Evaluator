# -*- coding: utf-8 -*-
import codecs

with codecs.open('solve_problem.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the normalization with proper equation solving
old = "solution_expr = self.math_parser.normalize_expr(self.freestyle_problem[\"parsed\"])"
new = """parsed_expr = self.freestyle_problem["parsed"]

            # Check if it's an equation to solve
            if isinstance(parsed_expr, sp.Equality):
                # Solve the equation
                var = list(parsed_expr.free_symbols)[0] if parsed_expr.free_symbols else None
                if var:
                    solutions = sp.solve(parsed_expr, var)
                    window.console.log(f"Solutions: {solutions}")
                    solution_expr = solutions
                else:
                    solution_expr = parsed_expr
            else:
                # Not an equation - just normalize
                solution_expr = self.math_parser.normalize_expr(parsed_expr)"""

if old in content:
    content = content.replace(old, new)
    print("OK: Replaced equation solving logic")
else:
    print("ERROR: Could not find code to replace")

# Replace how solution_latex is generated
old2 = "solution_latex = sp.latex(solution_expr)"
new2 = """# Build solution display
            if isinstance(parsed_expr, sp.Equality) and isinstance(solution_expr, list):
                var = list(parsed_expr.free_symbols)[0]
                if len(solution_expr) == 1:
                    solution_latex = f"{sp.latex(var)} = {sp.latex(solution_expr[0])}"
                elif len(solution_expr) > 1:
                    solution_parts = [f"{sp.latex(var)} = {sp.latex(sol)}" for sol in solution_expr]
                    solution_latex = " \\\\text{ or } ".join(solution_parts)
                else:
                    solution_latex = "\\\\text{No solution}"
            else:
                solution_latex = sp.latex(solution_expr)"""

if old2 in content:
    content = content.replace(old2, new2)
    print("OK: Replaced solution latex generation")
else:
    print("ERROR: Could not find solution latex code")

with codecs.open('solve_problem.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Done!")
