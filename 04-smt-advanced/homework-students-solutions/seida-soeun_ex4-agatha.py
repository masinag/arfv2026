from z3 import *

s = Solver()

# Exercise 4.3: Who killed Agatha?
# You are a private investigator and you have been called to solve a crime. When you
# arrive at the crime scene, the police have already established the following facts:
# 1. Someone who lives in Dreadbury Mansion killed Aunt Agatha.
# 2. Agatha, the butler, and Charles are the only ones living in Dreadbury Mansion.
# 3. A killer always hates their victim, and is never richer than their victim.
# 4. Charles hates no one that Aunt Agatha hates.
# 5. Agatha hates everyone except for the butler.
# 6. The butler hates everyone not richer than Aunt Agatha.
# 7. The butler hates everyone Aunt Agatha hates.
# 8. No one hates everyone.
# The police have asked you to find out who killed Aunt Agatha. Can you help them?

peoples = ["agatha", "butler", "charles"]

hates = {
    (people1, people2): Bool(f"{people1}hate{people2}")
    for people1 in peoples
    for people2 in peoples
}

richer = {
    (people1, people2): Bool(f"{people1}richerthan{people2}")
    for people1 in peoples
    for people2 in peoples
}

killer = {
    people: Bool(f"{people}iskiller")
    for people in peoples
}

# 1. Someone who lives in Dreadbury Mansion killed Aunt Agatha. == possible everyone
s.add(Or(*[killer[people] for people in peoples]))

# 2. Agatha, the butler, and Charles are the only ones living in Dreadbury Mansion. == possible one of them
s.add(AtMost(*[killer[people] for people in peoples], 1))

# 3. A killer always hates their victim, and is never richer than their victim.
for people in peoples:
    s.add(
        Implies(
            killer[people],
            And(hates[people, "agatha"], Not(richer[people, "agatha"]))
        )
    )
# 4. Charles hates no one that Aunt Agatha hates.
for people in peoples:
    s.add(
        Implies(
            hates["agatha", people],
            Not(hates["charles", people])
        )
    )

# 5. Agatha hates everyone except for the butler.
s.add(
    hates["agatha", "agatha"],
    hates["agatha", "charles"],
    Not(hates["agatha", "butler"])
)

# 6. The butler hates everyone not richer than Aunt Agatha.
for people in peoples:
    s.add(
        Implies(
            Not(richer[people, "agatha"]),
            hates["butler", people]
        )
    )

# 7. The butler hates everyone Aunt Agatha hates.
for people in peoples:
    s.add(
        Implies(
            hates["agatha", people],
            hates["butler", people]
        )
    )

# 8. No one hates everyone.
for people in peoples:
    s.add(
        Not(And(*[hates[people, p] for p in peoples]))
    )

# people richer than people 2 so people 2 will not richer than people
for people in peoples:
    for p in peoples:
        s.add(
            Implies(
                richer[people, p],
                Not(richer[p, people])
            )
        )

# transitivity
for people in peoples:
    for people2 in peoples:
        for people3 in peoples:
            s.add(
                Implies(
                    And(richer[people, people2], richer[people2, people3]),
                    richer[people, people3]
                )
            )

# no one richer than themselves
for people in peoples:
    s.add(
        Not(richer[people, people])
    )

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    for people in peoples:
        if is_true(model.evaluate(killer[people], model_completion=True)):
            print("killer is:", people)
else:
    print("unsatisfiable")
