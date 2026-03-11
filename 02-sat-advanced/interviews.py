from pysmt.shortcuts import And, Or, Not, Iff, ExactlyOne, Solver, Symbol, BOOL


def print_model(model):
    for day in days:
        company = [
            cname for c, cname in companies.items() if model[day_company[f"c_{day}_{c}"]].is_true()
        ][0]
        position = [
            pname for p, pname in positions.items() if model[day_position[f"p_{day}_{p}"]].is_true()
        ][0]
        print(f"Day {day}: interview for {company} as {position}")


days = [0, 1, 2, 3]
positions = {
    "c": "copywriter",
    "g": "graphic designer",
    "s": "sales rep",
    "m": "social media",
}
companies = {
    "A": "Alpha Plus",
    "L": "Laneplex",
    "S": "Sanbox",
    "I": "Streeter Inc.",
}

day_position = {f"p_{i}_{j}": Symbol(f"p_{i}_{j}", BOOL) for i in days for j in positions}
day_company = {f"c_{i}_{j}": Symbol(f"c_{i}_{j}", BOOL) for i in days for j in companies}

assertions = []

# The Alpha Plus interview is 2 days before the copywriter one
assertions.append(
    Or(
        And(day_company["c_0_A"], day_position["p_2_c"]),
        And(day_company["c_1_A"], day_position["p_3_c"]),
    )
)

# The graphic design interview is after the Sancode interview
assertions.append(
    Or(
        And(day_company[f"c_{day_S}_S"], day_position[f"p_{day_g}_g"])
        for day_S in days
        for day_g in days
        if day_S < day_g
    )
)

# Of the interview for the sales rep position and the Laneplex
# interview, one is on Aug. 23rd and the other is on Aug. 20th
assertions.append(
    Or(
        And(day_company["c_3_L"], day_position["p_0_s"]),
        And(day_company["c_0_L"], day_position["p_3_s"]),
    )
)

# The Streeter Inc. interview is 2 days after that for Alpha Plus
assertions.append(
    Or(
        And(day_company["c_0_A"], day_company["c_2_I"]),
        And(day_company["c_1_A"], day_company["c_3_I"]),
    )
)

# No social media interview is on Aug. 23
assertions.append(Not(day_position["p_3_m"]))

# Hidden condition: every day, there is an interview for exactly one company
for day in days:
    assertions.append(ExactlyOne(day_company[f"c_{day}_{j}"] for j in companies))

# Hidden condition: each company has an interview in only one day
for company in companies:
    assertions.append(ExactlyOne(day_company[f"c_{i}_{company}"] for i in days))

# Hidden condition: every day, there is an interview for exactly one position
for day in days:
    assertions.append(ExactlyOne(day_position[f"p_{day}_{j}"] for j in positions))

# Hidden condition: each position has an interview in only one day
for position in positions:
    assertions.append(ExactlyOne(day_position[f"p_{i}_{position}"] for i in days))

# for a in assertions:
#     print(a.serialize())

with Solver("msat") as msat:
    msat.add_assertions(assertions)
    if msat.solve():
        print("Solution found!")

        msat_model = msat.get_model()
        print_model(msat_model)

        # check if the solution is unique
        negated_model = Not(And(Iff(var, val) for var, val in msat_model))
        msat.add_assertion(negated_model)
        if msat.solve():
            print("Solution is not unique!")
            print_model(msat.get_model())
        else:
            print("Solution is unique!")
    else:
        print("No solution exists")
