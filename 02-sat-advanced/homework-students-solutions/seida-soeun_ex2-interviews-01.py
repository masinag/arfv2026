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
position_day_company = {
    (position, day, company): Bool(f"{position}{day}{company}")
    for position in positions
    for day in days
    for company in companies
}

# The Alpha Plus interview is 2 days before the copywriter one
s.add(
    Or(
        And(
            # for all positions - day 20 or 21 - alphaplus
            Or(position_day_company[position, str(day), "alphaplus"] for position in positions),
            # copywriter - day 22 or 23 - for all companies
            Or(position_day_company["copywriter", str(day + 2), company] for company in companies)
        )
        for day in [20, 21]
    )
)

# The graphic design interview is after the Sancode interview, possible after one, two, or three days
s.add(
    Or(
        And(
            # for all positions - day 20 or 21 or 22 - sancode
            Or(position_day_company[position, str(day), "sancode"] for position in positions),
            # graphicdesign - day 21 or 22 or 23 - alphaplus
            Or(
                position_day_company["graphicdesign", str(possibleday), company]
                for possibleday in range(day + 1, 24)
                for company in companies
            )
        )
        for day in [20, 21, 22]
    )
)

# Of the interview for the sales rep position and the Laneplex interview, one is on Aug. 23rd and the other is on Aug. 20th
s.add(
    Or(
        And(
            Or(position_day_company["salesrep", "20", company] for company in companies),
            Or(position_day_company[position, "23", "laneplex"] for position in positions)
        ),
        And(
            Or(position_day_company["salesrep", "23", company] for company in companies),
            Or(position_day_company[position, "20", "laneplex"] for position in positions)
        )
    )
)

# The Streeter Inc. interview is 2 days after that for Alpha Plus
s.add(
    Or(
        And(
            # # for all positions - day 20 or 21 - laneplex
            Or(position_day_company[position, str(day), "alphaplus"] for position in positions),
            # for all positions - day 22 or 23 - streeterinc
            Or(position_day_company[position, str(day + 2), "streeterinc"] for position in positions),
        )
        for day in [20, 21]
    )
)

# No social media interview is on Aug. 23rd
s.add(
    # socialmedia - day 23 - for all companies
    *[Not(position_day_company["socialmedia", "23", company]) for company in companies]
)

# one position happen only once
for position in positions:
    s.add(
        PbEq(
            [(position_day_company[position, day, company], 1)
             for day in days
             for company in companies],
            1
        )
    )

# one day happen only once
for day in days:
    s.add(
        PbEq(
            [(position_day_company[position, day, company], 1)
             for position in positions
             for company in companies],
            1
        )
    )

# one company happen only once
for company in companies:
    s.add(
        PbEq(
            [(position_day_company[position, day, company], 1)
             for position in positions
             for day in days],
            1
        )
    )

if s.check() == sat:
    print("satisfiable")
    m = s.model()

    for day in days:
        for position in positions:
            for company in companies:
                if is_true(m[position_day_company[position, day, company]]):
                    print(f"Aug. {day}: {position}, {company}")
else:
    print("unsatisfiable")
