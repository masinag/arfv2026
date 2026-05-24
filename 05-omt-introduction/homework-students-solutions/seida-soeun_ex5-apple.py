from z3 import *

s = Optimize()

# Exercise 5.1: Selling Apples
# An orchard has 50 apple trees, each producing 800 apples per year.
# Planting an additional tree reduces output per tree by 10 apples per year.
# How many trees should be added to maximize total output?

number_tree_add = Int("number_tree_add")

total_trees = number_tree_add + 50
producing = 800 - (10 * number_tree_add)
total_apple = total_trees * producing

s.add(number_tree_add >= 0)
s.add(producing >= 0)

s.maximize(total_apple)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("tree should be added:", model.evaluate(number_tree_add))
    print("total tree:", model.evaluate(total_trees))
    print("total apple:", model.evaluate(total_apple))
else:
    print("unsatisfiable")


