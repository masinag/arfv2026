from pysmt.shortcuts import And, Or, Symbol, BOOL, ExactlyOne, Solver, write_smtlib
from pysmt.solvers.msat import MathSAT5Solver


guests = list("ABCDE")
rooms = list("12345")

xx = {f"x_{g}_{r}": Symbol(f"x_{g}_{r}", BOOL) for g in guests for r in rooms}


def print_model(model, last_guest_arrived):
    assignment = {}
    for g in guests:
        room = [r for r in rooms if model[xx[f"x_{g}_{r}"]].is_true()]
        assert len(room) == 1
        room = room[0]
        assignment[g] = room
        if g == last_guest_arrived:
            break
    print(", ".join(f"{g} -> {r}" for g, r in assignment.items()))


def print_core(core):
    print("\n".join(map(lambda v: f"- {v}", core)))
    # print(core)


assertions = []
guests_preferences = []

# Every guest goes in exactly one room
for g in guests:
    assertions.append(
        (
            ExactlyOne(xx[f"x_{g}_{r}"] for r in rooms),
            f"guest {g} goes in exactly one room",
        )
    )

# Every room hosts exactly one guest
for r in rooms:
    assertions.append(
        (
            ExactlyOne(xx[f"x_{g}_{r}"] for g in guests),
            f"room {r} hosts exactly one guest",
        )
    )


guests_preferences.append(
    (Or(xx["x_A_1"], xx["x_A_2"]), "Guest A would like to choose room 1 or 2.")
)


guests_preferences.append(
    (
        Or(xx["x_B_2"], xx["x_B_4"]),
        "Guest B would like to choose a room with an even number.",
    )
)

guests_preferences.append((xx["x_C_1"], "Guest C would like the first room."))

guests_preferences.append(
    (Or(xx["x_D_2"], xx["x_D_4"]), "Guest D has the same behavior as user B.")
)

guests_preferences.append(
    (
        Or(xx["x_E_1"], xx["x_E_5"]),
        "Guest E would like one of the external rooms.",
    )
)

write_smtlib(And(a[0] for a in assertions), "reception.smt2")


with Solver("msat", unsat_cores_mode="named") as msat:
    msat: MathSAT5Solver
    for assertion, name in assertions:
        msat.add_assertion(assertion, named=name)
    for g, (ass, name) in zip(guests, guests_preferences):
        msat.push()
        msat.add_assertion(ass, named=name)
        if msat.solve():
            print(
                f"Guest {g} can be satisfied",
                end=" ",
            )
            print_model(msat.get_model(), g)
        else:
            print(
                f"Guest {g} cannot be satisfied, because of: ",
            )
            print_core(msat.get_named_unsat_core())
            break
