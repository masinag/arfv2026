from z3 import *

s = Optimize()

# Exercise 6.1: Multi-objective optimization
# A small business promotes itself using two methods: traditional media ads and personal
# appearances.
# A traditional media ad campaign costs $2000, generating 2 new customers and 1
# positive rating per month. Each ad campaign takes 1 hour.
# A personal appearance costs $500, generating 2 new customers and 5 positive
# ratings. Each personal appearance takes 2 hours.
# The company wants at least 16 new customers and 28 positive ratings per month.
# Try to minimize both costs and time.

costs, time = Reals("costs time")
customer, rating, ad, appearances = Ints("customer rating ad appearances")

s.add(ad >= 0, appearances >= 0)
s.add(costs == 2000 * ad + 500 * appearances)
s.add(time == 1 * ad + 2 * appearances)
s.add(customer == 2 * ad + 2 * appearances)
s.add(rating == 1 * ad + 5 * appearances)
s.add(customer >= 16, rating >= 28)

s.minimize(costs)
s.minimize(time)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("total cost:", model.evaluate(costs))
    print("total time:", model.evaluate(time))
    print("total rating:", model.evaluate(rating))
    print("total customer:", model.evaluate(customer))
    print("total appearances:", model.evaluate(appearances))
    print("total ad:", model.evaluate(ad))
else:
    print("unsatisfiable")