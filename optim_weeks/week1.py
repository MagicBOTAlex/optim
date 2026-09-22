import numpy as np
import matplotlib.pyplot as plt
import sympy as sp

# 1. Symbolic definitions and derivations with SymPy
x = sp.Symbol("x_1", positive=True)
x2 = sp.Symbol("x_2", positive=True)
f_sym = x - sp.log(x)
df_sym = sp.diff(f_sym, x)  # 1 - 1/x
d2f_sym = sp.diff(df_sym, x)  # 1/x**2


g_sym = 8 * x + 12 * x2 + x**2 - 2 * x2**2
g_dx1 = sp.diff(g_sym, x)
g_dx2 = sp.diff(g_sym, x2)
g_dx1_num = sp.lambdify((x, x2), g_dx1, "numpy")
g_dx2_num = sp.lambdify((x, x2), g_dx2, "numpy")

print(g_dx1)
print(g_dx2)

# Find critical points and minimizer symbolically
critical_points = sp.solve(sp.Eq(df_sym, 0), x)
x_star = critical_points[0]
f_min = f_sym.subs(x, x_star)

print(f"f(x)   = {f_sym}")
print(f"f'(x)  = {df_sym}")
print(f"f''(x) = {d2f_sym}")
print(f"Minimizer x* = {x_star}, Minimum value f(x*) = {f_min}")

# Convert symbolic expressions to numerical functions for plotting
f_num = sp.lambdify(x, f_sym, "numpy")
df_num = sp.lambdify(x, df_sym, "numpy")
d2f_num = sp.lambdify(x, d2f_sym, "numpy")

# 2. Domain setup: 0 < x <= 2 with spacing 0.01
x_vals = np.arange(0.01, 2.01, 0.01)

# 3. Subplots creation
fig, axs = plt.subplots(1, 4, figsize=(15, 4.5))

# Plot f(x)
axs[0].plot(x_vals, f_num(x_vals), color="tab:blue", lw=2)
axs[0].plot(float(x_star), float(f_min), "ro", label=f"Min $(1, 1)$")
axs[0].set_title(r"$f(x) = x - \ln(x)$")
axs[0].set_xlabel("$x$")
axs[0].set_ylabel("$y$")
axs[0].set_ylim(0.5, 5)
axs[0].grid(True)
axs[0].legend()

# Plot f'(x)
axs[1].plot(x_vals, df_num(x_vals), color="tab:orange", lw=2)
axs[1].axhline(0, color="gray", linestyle="--", lw=1)
axs[1].plot(float(x_star), 0, "ro", label=r"$x^* = 1$")
axs[1].set_title(r"$f'(x) = 1 - \frac{1}{x}$")
axs[1].set_xlabel("$x$")
axs[1].set_ylabel("$y$")
axs[1].set_ylim(-5, 2)
axs[1].grid(True)
axs[1].legend()

# Plot f''(x)
axs[2].plot(x_vals, d2f_num(x_vals), color="tab:green", lw=2)
axs[2].set_title(r"$f''(x) = \frac{1}{x^2}$")
axs[2].set_xlabel("$x$")
axs[2].set_ylabel("$y$")
axs[2].set_ylim(0, 10)
axs[2].grid(True)

# Plot gradients
X1, X2 = np.meshgrid(np.linspace(-8, 2, 15), np.linspace(0, 6, 15))
U = g_dx1_num(X1, X2)
V = g_dx2_num(X1, X2)
axs[3].quiver(X1, X2, U, V, color="tab:purple")
axs[3].plot(-4, 3, "ro", label=r"Saddle $(-4, 3)$")
axs[3].set_title(r"$f''(x) = \frac{1}{x^2}$")
axs[3].set_xlabel("$x$")
axs[3].set_ylabel("$y$")
axs[3].set_ylim(0, 10)
axs[3].grid(True)

plt.tight_layout()
plt.show()
