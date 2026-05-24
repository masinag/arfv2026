from z3 import *

s = Optimize()

# You are the owner of one of the most prestigious concert halls in New York. In the last days you received a lot of
# requests from different bands to book the hall on the 4th of July and you are unsure about being able to accept
# them all. Some organization rules are the following:
# • Bands can book the hall from 18.00 to 24.00.
# • Bands can reserve one or more slots of 1 hours, the slots being 18.00-19.00, 19.00-20.00, 20.00-21.00
# and so on.
# This is the list of all the requests received until now:
# • The Beagles: from 19.00 to 21.00 or from 22.00 to 24.00
# • AC/DC++: 3consecutive hours, no matter when.
# • Rolling Stonks: from 18.00 to 19.00 or from 23.00 to 24.00
# • Kanji West: 1 hour among all the slots, excluding the first slot and the last one.
# Use OptiMathSAT to encode the problem as a SAT problem (make sure not to use non-Boolean data types)
# and see if you can satisfy the requests of all the customers.
# • If you can satisfy everyone, write a comment reporting the valid schedule.
# • Otherwise slightly modify the problem so that you can return a schedule where the maximum amount
# of bands can perform live. Take into account that AC/DC++ must perform no matter what, given their
# popularity.

schedules = ["18to19", "19to20", "20to21", "21to22", "22to23", "23to24"]
bands = ["thebeagles", "acdcplusplus", "rollingstonks", "kanjiwest"]

band_schedule = {
    (band, schedule): Bool(f"band{band}schedule{schedule}")
    for band in bands
    for schedule in schedules
}

accept = {
    band: Bool(f"acceptband{band}")
    for band in bands
}

s.add(accept["acdcplusplus"])

# one schedule, one band
for schedule in schedules:
    s.add(
        AtMost(*[band_schedule[band, schedule] for band in bands], 1)
    )

# band is not accepted so no slot
for band in bands:
    for schedule in schedules:
        s.add(
            Implies(Not(accept[band]), Not(band_schedule[band, schedule]))
        )

# The Beagles: from 19.00 to 21.00 or from 22.00 to 24.00
s.add(
    Implies(
        accept["thebeagles"],
        And(
            Or(
                And(band_schedule["thebeagles", "19to20"], band_schedule["thebeagles", "20to21"]),
                And(band_schedule["thebeagles", "22to23"], band_schedule["thebeagles", "23to24"])
            ),
            PbEq([(band_schedule["thebeagles", schedule], 1) for schedule in schedules], 2)
        )
    )
)

# AC/DC++: 3consecutive hours, no matter when.
s.add(
    Implies(
        accept["acdcplusplus"],
        And(
            Or(
                And(
                    band_schedule["acdcplusplus", "18to19"],
                    band_schedule["acdcplusplus", "19to20"],
                    band_schedule["acdcplusplus", "20to21"]
                ),
                And(
                    band_schedule["acdcplusplus", "19to20"],
                    band_schedule["acdcplusplus", "20to21"],
                    band_schedule["acdcplusplus", "21to22"]
                ),
                And(
                    band_schedule["acdcplusplus", "20to21"],
                    band_schedule["acdcplusplus", "21to22"],
                    band_schedule["acdcplusplus", "22to23"]
                ),
                And(
                    band_schedule["acdcplusplus", "21to22"],
                    band_schedule["acdcplusplus", "22to23"],
                    band_schedule["acdcplusplus", "23to24"],
                )
            ),
            PbEq([(band_schedule["acdcplusplus", schedule], 1) for schedule in schedules], 3)
        )
    )
)

# Rolling Stonks: from 18.00 to 19.00 or from 23.00 to 24.00
s.add(
    Implies(
        accept["rollingstonks"],
        And(
            Or(band_schedule["rollingstonks", "18to19"], band_schedule["rollingstonks", "23to24"]),
            PbEq([(band_schedule["rollingstonks", schedule], 1) for schedule in schedules], 1)
        )
    )
)

# Kanji West: 1 hour among all the slots, excluding the first slot and the last one.
s.add(
    Implies(
        accept["kanjiwest"],
        And(
            Or(
                band_schedule["kanjiwest", "19to20"],
                band_schedule["kanjiwest", "20to21"],
                band_schedule["kanjiwest", "21to22"],
                band_schedule["kanjiwest", "22to23"]
            ),
            PbEq([(band_schedule["kanjiwest", schedule], 1) for schedule in schedules], 1)
        )
    )
)

s.maximize(Sum(If(accept[band], 1, 0) for band in bands))

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    for band in bands:
        if is_true(model.evaluate(accept[band], model_completion=True)):
            print("band accepted:", band)

    for band in bands:
        for schedule in schedules:
            if is_true(model.evaluate(band_schedule[band, schedule], model_completion=True)):
                print(f"band {band} with schedule {schedule}")
else:
    print("unsatisfiable")

# the total booking is 7h but the available slot only 6h so would be unsatisfiable
