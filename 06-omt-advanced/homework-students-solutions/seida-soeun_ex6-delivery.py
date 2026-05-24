from z3 import *

s = Optimize()

# Exercise 6.2: Delivery
# A company must deliver goods from a central depot to three warehouses: A, B, and C.
# There are two transport scenarios: Normal Traffic and Heavy Traffic.
# Delivery Costs (per unit):
# Warehouse     Normal Traffic  Heavy Traffic
# A             $10             $21
# B             $15             $18
# C             $20             $15
# Let xA,xB,xC be the number of units sent to warehouses A, B, and C.
# The company requires that: 100 ≤ xA +xB +xC ≤ 150
# Use OptiMathSAT to find the number of units to minimize the worst-case delivery cost.

xan, xah, xbn, xbh, xcn, xch, normal, heavy, cost = Ints("xan xah xbn xbh xcn xch normal heavy cost")

units = [xan, xah, xbn, xbh, xcn, xch]
total = xan + xah + xbn + xbh + xcn + xch


s.add(total >= 100, total <= 150)
for unit in units:
    s.add(unit > 0)

s.add(normal == xan * 10 + xbn * 15 + xcn * 20)
s.add(heavy == xah * 21 + xbh * 18 + xch * 15)

s.add(cost >= normal, cost >= heavy)

s.minimize(cost)

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    print("warehouse a with normal traffic:", model.evaluate(xan))
    print("warehouse a with heavy traffic:", model.evaluate(xah))
    print("warehouse b with normal traffic:", model.evaluate(xbn))
    print("warehouse b with heavy traffic:", model.evaluate(xbh))
    print("warehouse c with normal traffic:", model.evaluate(xcn))
    print("warehouse c with heavy traffic:", model.evaluate(xch))
    print("normal traffic cost:", model.evaluate(normal))
    print("heavy traffic cost:", model.evaluate(heavy))
    print("cost:", model.evaluate(cost))
    print("total unit:", model.evaluate(total))
else:
    print("unsatisfiable")


