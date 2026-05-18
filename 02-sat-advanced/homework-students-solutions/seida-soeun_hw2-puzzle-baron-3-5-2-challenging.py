from z3 import *

s = Solver()

# Homework 2.3: Puzzle Baron
# Adapt the code written for Exercise 2.1 to solve similar puzzles from the following
# website: https://logic.puzzlebaron.com/.
# - To obtain an exercises almost identical to the one shown in class select the “3×4
# grid” and the “challenging” difficulty.
# - Adapt the code to manage a “3×5” grid.

# Active Clues
# 1. Of the aqueduct starting in Castelloro and the aqueduct starting in Doravella,
# one was built in 110 AD and the other ends in Montavello.
# 2. The aqueduct ending in Petricosa was built 100 years after the aqueduct starting in Bassaverde.
# 3. The aqueduct starting in Doravella was built 100 years after the structure starting in Aureliana.
# 4. The structure ending in Orviano was either the structure starting in Aureliana or
# the aqueduct starting in Iscavento.
# 5. The structure starting in Doravella was built sometime before the aqueduct ending in Terravino.

towns = ["aureliana", "bassaverde", "castelloro", "doravella", "iscavento"]
years = [10, 60, 110, 160, 210]
endings = ["montavello", "orviano", "petricosa", "terravino", "vallicello"]

town_year = {
    (town, year): Bool(f"town{town}_year{year}")
    for town in towns
    for year in years
}

town_ending = {
    (town, ending): Bool(f"town{town}_ending{ending}")
    for town in towns
    for ending in endings
}

year_ending = {
    (year, ending): Bool(f"year{year}_ending{ending}")
    for year in years
    for ending in endings
}

# one town, one year
for town in towns:
    s.add(
        AtMost(*[town_year[town, year] for year in years], 1),
        Or(*[town_year[town, year] for year in years])
    )
    # one town, one ending
    s.add(
        AtMost(*[town_ending[town, ending] for ending in endings], 1),
        Or(*[town_ending[town, ending] for ending in endings])
    )

# one year, one town
for year in years:
    s.add(
        AtMost(*[town_year[town, year] for town in towns], 1),
        Or(*[town_year[town, year] for town in towns])
    )
    # one year, one ending
    s.add(
        AtMost(*[year_ending[year, ending] for ending in endings], 1),
        Or(*[year_ending[year, ending] for ending in endings])
    )

# one ending, one town
for ending in endings:
    s.add(
        AtMost(*[town_ending[town, ending] for town in towns], 1),
        Or(*[town_ending[town, ending] for town in towns])
    )
    # one ending, one year
    s.add(
        AtMost(*[year_ending[year, ending] for year in years], 1),
        Or(*[year_ending[year, ending] for year in years])
    )

# connect table
for town in towns:
    for ending in endings:
        for year in years:
            s.add(
                Implies(
                    And(town_year[town, year], town_ending[town, ending]),
                    year_ending[year, ending],
                )
            )

# 1. Of the aqueduct starting in Castelloro and the aqueduct starting in Doravella,
# one was built in 110 AD and the other ends in Montavello.
s.add(
    Or(
        And(town_year["castelloro", 110], town_ending["doravella", "montavello"]),
        And(town_year["doravella", 110], town_ending["castelloro", "montavello"]),
    )
)

# 2. The aqueduct ending in Petricosa was built 100 years after the aqueduct starting in Bassaverde.
s.add(
    Or(
        And(year_ending[110, "petricosa"], town_year["bassaverde", 10]),
        And(year_ending[160, "petricosa"], town_year["bassaverde", 60]),
        And(year_ending[210, "petricosa"], town_year["bassaverde", 110])
    )
)

# 3. The aqueduct starting in Doravella was built 100 years after the structure starting in Aureliana.
s.add(
    Or(
        And(town_year["doravella", 110], town_year["aureliana", 10]),
        And(town_year["doravella", 160], town_year["aureliana", 60]),
        And(town_year["doravella", 210], town_year["aureliana", 110])
    )
)

# 4. The structure ending in Orviano was either the structure starting in Aureliana or
# the aqueduct starting in Iscavento.
s.add(
    Or(town_ending["aureliana", "orviano"], town_ending["iscavento", "orviano"])
)

# 5. The structure starting in Doravella was built sometime before the aqueduct ending in Terravino.
s.add(
    Or(
        *[And(town_year["doravella", doravella_year], year_ending[terravino_year, "terravino"])
          for doravella_year in years
          for terravino_year in years
          if doravella_year < terravino_year
          ]
    )
)

if s.check() == sat:
    model = s.model()
    print("satisfiable")
    second_model = []
    for town in towns:
        valid_ending = None
        valid_year = None
        for ending in endings:
            valid = is_true(model.evaluate(town_ending[town, ending], model_completion=True))
            if valid:
                valid_ending = ending
            second_model.append(town_ending[town, ending] != valid)
        for year in years:
            valid = is_true(model.evaluate(town_year[town, year], model_completion=True))
            if valid:
                valid_year = year
            second_model.append(town_year[town, year] != valid)
        print(f"town: {town}, year: {valid_year}, ending: {valid_ending}")
    s.add(Or(second_model))
    if s.check() == unsat:
        print("unique")
    else:
        print("not unique")
        print("second model:", s.model())
else:
    print("unsatisfiable")
