from flask import Flask, render_template, request
import sympy as sp
import random

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def newton_raphson():
    if request.method == "POST":
        equation_str = request.form.get("equation")
        x_tolerance = int(request.form.get("tolerance"))
        yakınsama = int(request.form.get("precision"))
        tolerance = 10 ** -x_tolerance

        x = sp.symbols('x')
        try:
            equation = sp.sympify(equation_str)
            derivative = sp.diff(equation, x)
        except Exception as e:
            return render_template("index.html", error=f"Hata: {e}")

        max_iterations = 100
        roots = []

        for _ in range(10):
            x0 = random.randint(-10, 10)
            for iteration in range(max_iterations):
                f_x0 = equation.evalf(subs={x: x0})
                f_prime_x0 = derivative.evalf(subs={x: x0})

                if abs(f_prime_x0) < 1e-10:
                    break

                x1 = x0 - f_x0 / f_prime_x0

                if abs(x1 - x0) < tolerance:
                    root_rounded = round(x1, yakınsama)
                    if not any(abs(root_rounded - r) < tolerance for r in roots):
                        roots.append(root_rounded)
                    break

                x0 = x1

        positive_roots = [r for r in roots if r > 0]
        negative_roots = [r for r in roots if r < 0]

        return render_template(
            "index.html",
            equation=equation,
            derivative=derivative,
            positive_roots=positive_roots,
            negative_roots=negative_roots,
        )

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True)
