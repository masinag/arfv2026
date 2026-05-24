from z3 import *

s = Solver()

# Bill has 4 job interviews this week (Aug. 20th, 21st, 22nd, 23rd), each for a different
# position (copywriter, graphic design, sales rep, and social media) at a different
# company (Alpha Plus, Laneplex, Sancode, Streeter Inc.). Knowing that:
# - The Alpha Plus interview is 2 days before the copywriter one
# - The graphic design interview is after the Sancode interview
# - Of the interview for the sales rep position and the Laneplex interview, one is on
# Aug. 23rd and the other is on Aug. 20th
# - The Streeter Inc. interview is 2 days after that for Alpha Plus
# - No social media interview is on Aug. 23rd
# Match each job position to its day and company.

positions = ["copywriter", "graphicdesign", "salesrep", "socialmedia"]
days = ["20", "21", "22", "23"]
companies = ["alphaplus", "laneplex", "sancode", "streeterinc"]

# map position to day and company to day, the middle mapping is day
day_position = {
    (day, position): Bool(f"{day}_{position}")
    for position in positions
    for day in days
}

day_company = {
    (day, company): Bool(f"{day}_{company}")
    for company in companies
    for day in days
}

# The Alpha Plus interview is 2 days before the copywriter one
s.add(
    Or([
        And(
            day_company[str(day), "alphaplus"], day_position[str(day + 2), "copywriter"]
        )
        for day in [20, 21]
    ])
)

# The graphic design interview is after the Sancode interview, possible after one, two, or three days
s.add(
    Or([
        And(
            day_company[str(day), "sancode"], day_position[str(graphic_design_day), "graphicdesign"]
        )
        for day in [20, 21, 22]
        for graphic_design_day in range(day + 1, 24)
    ])
)

# Of the interview for the sales rep position and the Laneplex interview, one is on Aug. 23rd and the other is on Aug. 20th
s.add(
    Or(
        # possible only one day can happen will prevent in next step
        And(day_company["20", "laneplex"], day_position["23", "salesrep"]),
        And(day_company["23", "laneplex"], day_position["20", "salesrep"])
    )
)

# The Streeter Inc. interview is 2 days after that for Alpha Plus
s.add(
    Or([
        And(
            day_company[str(day), "alphaplus"], day_company[str(day + 2), "streeterinc"]
        )
        for day in [20, 21]
    ])

)

# No social media interview is on Aug. 23rd
s.add(
    Not(day_position["23", "socialmedia"])
)

# one position, one day
for position in positions:
    s.add(
        AtMost(
            *[day_position[day, position] for day in days], 1
        ),
        Or(
            *[day_position[day, position] for day in days]
        )
    )

# one company, one day
for company in companies:
    s.add(
        AtMost(
            *[day_company[day, company] for day in days], 1
        ),
        Or(
            *[day_company[day, company] for day in days]
        )
    )
# one day, one company # one day, one position
for day in days:
    s.add(
        AtMost(
            *[day_company[day, company] for company in companies], 1
        ),
        Or(
            *[day_company[day, company] for company in companies]
        ),
        AtMost(
            *[day_position[day, position] for position in positions], 1
        ),
        Or(
            *[day_position[day, position] for position in positions]
        )
    )

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    second_model = []
    for day in days:
        interview_position = None
        interview_company = None

        for position in positions:
            valid = is_true(model.evaluate(day_position[day, position], model_completion=True))

            if valid:
                interview_position = position

            # add other else that differ in first check
            second_model.append(day_position[day, position] != valid)
        for company in companies:
            valid = is_true(model.evaluate(day_company[day, company], model_completion=True))

            if valid:
                interview_company = company

            # add other else that differ in first check
            second_model.append(day_company[day, company] != valid)
        print(f"{day}, {interview_position}, {interview_company}")

    # check unique, add variable that differ from first model
    s.add(Or(second_model))
    if s.check() == sat:
        print("not unique")
        print("second model:", s.model())
    else:
        print("unique")
else:
    print("unsatisfiable")
