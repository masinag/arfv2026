from z3 import *

s = Solver()

# Exercise 3.2: intersecting lines
# Given two points in the Euclidean space A = (1, 3/2) and B = (1/2, 7),find:
# - the equation of the line passing through them,
# - the values xi and yi where the line intersects the x and y axes, respectively.

# equation form y = ax + b

a = Real("a")
b = Real("b")

xi = Real("xi")
yi = Real("yi")

s.add(
    a * RealVal("1") + b == RealVal("3/2"),
    a * RealVal("1/2") + b == RealVal("7")
)

s.add(
    # 0 = ax + b
    RealVal("0") == a * xi + b,
    # y = a0 + b
    yi == a * RealVal("0") + b
)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("model: ", model)
    print(f"y = {model[a]}x + {model[b]}")
    print(f"in the line intersects the x and y axes, x0 = {model[xi]}, y0 = {model[yi]}")
else:
    print("unsatisfiable")
