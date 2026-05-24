from z3 import *

s = Solver()

# Four students took a test where every question had two possible answers, A or B. Each question was worth 10
# points, for a total of 100 points. There is no penalty for giving a wrong answer. The students’ test results were
# posted as seen below:

# mary: 70
# 1  2  3  4  5  6  7  8  9  10
# b  b  a  b  a  b  b  a  b  b

# dan: 50
# 1  2  3  4  5  6  7  8  9  10
# b  a  a  a  b  a  b  a  a  a

# lisa: 30
# 1  2  3  4  5  6  7  8  9  10
# b  a  a  a  b  b  b  a  b  a

# john: ?
# 1  2  3  4  5  6  7  8  9  10
# b  b  a  a  a  b  b  a  a  a

# As you can see, the teacher forgot to tally John’s score. John was heading to the teacher’s office when Mary
# called him back, saying they could figure out his score using the results from the other tests. Can you figure out
# John’s score?
# Use MathSAT to encode the problem as a SMT problem and find the solution. Once obtained, report it on
# as a comment at the end of the file. Is the answer key reported as a solution unique (meaning that there is no
# other possible answer assignment reaching the same score)? Add some constraints to test its uniqueness and
# write in a comment the result:
# • If the solution is unique, write how you assumed it.
# • If the solution is not unique, write how you assumed it and report a second solution in the comments.

q1a, q1b, q2a, q2b, q3a, q3b, q4a, q4b, q5a, q5b, q6a, q6b, q7a, q7b, q8a, q8b, q9a, q9b, q10a, q10b = Ints("q1a q1b q2a q2b q3a q3b q4a q4b q5a q5b q6a q6b q7a q7b q8a q8b q9a q9b q10a q10b")

questions = [q1a, q1b, q2a, q2b, q3a, q3b, q4a, q4b, q5a, q5b, q6a, q6b, q7a, q7b, q8a, q8b, q9a, q9b, q10a, q10b]

pairs = [
    (q1a, q1b),
    (q2a, q2b),
    (q3a, q3b),
    (q4a, q4b),
    (q5a, q5b),
    (q6a, q6b),
    (q7a, q7b),
    (q8a, q8b),
    (q9a, q9b),
    (q10a, q10b)
]

for a, b in pairs:
    s.add(
        Or(
            And(a == 10, b == 0),
            And(a == 0, b == 10)
        )
    )

# mary: 70
# 1  2  3  4  5  6  7  8  9  10
# b  b  a  b  a  b  b  a  b  b
s.add(q1b + q2b + q3a + q4b + q5a + q6b + q7b + q8a + q9b + q10b == 70)

# dan: 50
# 1  2  3  4  5  6  7  8  9  10
# b  a  a  a  b  a  b  a  a  a
s.add(q1b + q2a + q3a + q4a + q5b + q6a + q7b + q8a + q9a + q10a == 50)

# lisa: 30
# 1  2  3  4  5  6  7  8  9  10
# b  a  a  a  b  b  b  a  b  a
s.add(q1b + q2a + q3a + q4a + q5b + q6b + q7b + q8a + q9b + q10a == 30)

# john: ?
# 1  2  3  4  5  6  7  8  9  10
# b  b  a  a  a  b  b  a  a  a
john_score = q1b + q2b + q3a + q4a + q5a + q6b + q7b + q8a + q9a + q10a

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("john score:", model.evaluate(john_score))
    print("possible score in each question:", [
        "a" if model.evaluate(a).as_long() == 10 else "b"
        for a, b in pairs
    ])
    second_model = []
    for question in questions:
        second_model.append(question != model.evaluate(question))
    s.add(Or(second_model))
    if s.check() == unsat:
        print("unique")
    else:
        model2 = s.model()
        print("not unique")
        print("john score:", model2.evaluate(john_score))
        print("possible score in each question:", [
            "a" if model2.evaluate(a).as_long() == 10 else "b"
            for a, b in pairs
        ])

else:
    print("unsatisfiable")