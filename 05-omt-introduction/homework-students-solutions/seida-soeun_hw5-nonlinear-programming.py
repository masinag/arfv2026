from z3 import *

s = Optimize()

# Homework 5.2: Nonlinear Programming
# Find two non-negative numbers x and y so that:
# - Their sum is 9.
# - The product of one number and the square of the other number is a maximum in
# the range(0,200).

x, y = Reals('x y')

product = x * y * y # y * x * x

s.add(x + y == 9)
s.add(x >= 0, y >= 0)
s.add(product >= 0, product < 200)

s.maximize(product)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("x:", model.evaluate(x))
    print("y:", model.evaluate(y))
    print("product:", model.evaluate(product))
else:
    print("unsatisfiable")
