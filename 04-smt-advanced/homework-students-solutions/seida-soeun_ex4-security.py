from z3 import *

s = Solver()

# Exercise 4.2: Check Security... Again
# This code that analyzes a 5-digit number in [10000,99999] with distinct digits:
# int check_security(num) {
# security = 4
# if (num is multiple of 3 or 5, but not both)
# security = security- 1
# if (the sum of digits is a multiple of 10)
# security = security- 1
# if (the number is palindrome)
# security = security- 1
# if (the digits are in ascending order (including equality))
# security = security- 1
# return security
# }
# Is there an input that provides the security value 2. Answer using MathSAT.

a, b, c, d, e = Ints("a b c d e")

number = 10000 * a + 1000 * b + 100 * c + 10 * d + e

# range
s.add(number >= 10000, number <= 99999)

# possible
for digit in [a, b, c, d, e]:
    s.add(digit >= 0, digit <= 9)

# avoid first digit 0
s.add(a != 0)

# with distinct digits
s.add(Distinct(a, b, c, d, e))

security = 4

# if (num is multiple of 3 or 5, but not both)
condition1 = Xor(number % 3 == 0, number % 5 == 0)
# if (the sum of digits is a multiple of 10)
condition2 = Sum([a, b, c, d, e]) % 10 == 0
# if (the number is palindrome)
condition3 = And(a == e, b == d)
# if (the digits are in ascending order (including equality))
condition4 = And(a <= b, b <= c, c <= d, d <= e)
# security value 2
s.add(
    security - If(condition1, 1, 0)
    - If(condition2, 1, 0)
    - If(condition3, 1, 0)
    - If(condition4, 1, 0)
    == 2
)
if s.check() == sat:
    model = s.model()
    print("satisfiable")
    print("number:", model.evaluate(number))

    print("condition1:", model.evaluate(condition1))
    print("condition2:", model.evaluate(condition2))
    print("condition3:", model.evaluate(condition3))
    print("condition4:", model.evaluate(condition4))
else:
    print("unsatisfiable")
