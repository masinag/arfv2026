from z3 import *

s = Solver()

# Exercise 4.2: task manager
# Your PC needs to complete 5 different tasks (A, B, C, D and E) to correctly save a file.
# There are some constraints about the order execution of the tasks:
# - We can execute A after D is completed.
# - We can execute B after C and E are completed.
# - We can execute E after B or D are completed.
# - We can execute C after A is completed.
# Which is the task that will execute for last?

# largest number is last
a, b, c, d, e = Ints("a b c d e")

# set range
for task in [a, b, c, d, e]:
    s.add(
        task > 0, task <= 5,
    )

s.add(a > d)
s.add(And(b > c, b > e))
s.add(Or(e > b, e > d))
s.add(c > a)
s.add(Distinct(a, b, c, d, e))

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print(f"a: {model[a]}, b: {model[b]}, c: {model[c]}, d: {model[d]}, e: {model[e]}")
    for task in [a, b, c, d, e]:
        if model[task].as_long() == 5:
            print(f"the last task: {task}")
else:
    print("unsatisfiable")