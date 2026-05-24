from z3 import *

s = Solver()

# Homework 2.3: Puzzle Baron
# Adapt the code written for Exercise 2.1 to solve similar puzzles from the following
# website: https://logic.puzzlebaron.com/.
# - To obtain an exercises almost identical to the one shown in class select the “3×4
# grid” and the “challenging” difficulty.
# - Adapt the code to manage a “3×5” grid.

# Active Clues
# 1. Loretta was either the presenter who spoke for 17 minutes or the student who spoke for 8 minutes.
# 2. Willie spoke 6 minutes more than the student who gave the presentation on President Fillmore.
# 3. Peggy spoke for 5 minutes.
# 4. Of the presenter who spoke for 14 minutes and the student who spoke for 17 minutes,
# one talked about President Washington and the other was Theodore.
# 5. The student who gave the presentation on President Washington spoke 6 minutes more than
# the student who gave the presentation on President Lincoln.
# 6. Theodore was either the presenter who gave the presentation on President Fillmore
# or the presenter who spoke for 17 minutes.
# 7. The student who spoke for 17 minutes didn't talk about President Coolidge.

# /*      this exercise is incomplete       */
presenters = ["loretta", "willie", "peggy", "theodore"]
durations = [5, 8, 14, 17]
topics = ["presidentwashington", "presidentfillmore", "presidentcoolidge", "presidentlincoln"]

presenter_duration = {
    (presenter, duration): Bool(f"presenter{presenter}_duration{duration}")
    for presenter in presenters
    for duration in durations
}

topic_duration = {
    (topic, duration): Bool(f"topic{topic}_duration{duration}")
    for topic in topics
    for duration in durations
}

presenter_topic = {
    (presenter, topic): Bool(f"presenter{presenter}_topic{topic}")
    for presenter in presenters
    for topic in topics
}

# one presenter, one duration
for presenter in presenters:
    s.add(
        AtMost(*[presenter_duration[presenter, duration] for duration in durations], 1),
        Or(*[presenter_duration[presenter, duration] for duration in durations])
    )
    # one presenter, one topic
    s.add(
        AtMost(*[presenter_topic[presenter, topic] for topic in topics], 1),
        Or(*[presenter_topic[presenter, topic] for topic in topics])
    )

# one topic, one duration
for topic in topics:
    s.add(
        AtMost(*[topic_duration[topic, duration] for duration in durations], 1),
        Or(*[topic_duration[topic, duration] for duration in durations])
    )
    # one topic, one presenter
    s.add(
        AtMost(*[presenter_topic[presenter, topic] for presenter in presenters], 1),
        Or(*[presenter_topic[presenter, topic] for presenter in presenters])
    )

# one duration, one topic
for duration in durations:
    s.add(
        AtMost(*[topic_duration[topic, duration] for topic in topics], 1),
        Or(*[topic_duration[topic, duration] for topic in topics])
    )
    # one duration, one presenter
    s.add(
        AtMost(*[presenter_duration[presenter, duration] for presenter in presenters], 1),
        Or(*[presenter_duration[presenter, duration] for presenter in presenters])
    )

# connect table
for presenter in presenters:
    for topic in topics:
        for duration in durations:
            s.add(
                Implies(
                    And(
                        presenter_duration[presenter, duration],
                        presenter_topic[presenter, topic],
                    ),
                    topic_duration[topic, duration],
                )
            )

# 1. Loretta was either the presenter who spoke for 17 minutes or the student who spoke for 8 minutes.
s.add(
    Or(presenter_duration["loretta", 17], presenter_duration["loretta", 8])
)

# 2. Willie spoke 6 minutes more than the student who gave the presentation on President Fillmore.
s.add(
    And(
        presenter_duration["willie", 14], topic_duration["presidentfillmore", 8]
    )
)

# 3. Peggy spoke for 5 minutes.
s.add(presenter_duration["peggy", 5])

# 4. Of the presenter who spoke for 14 minutes and the student who spoke for 17 minutes,
# one talked about President Washington and the other was Theodore.
s.add(
    Or(
        And(topic_duration["presidentwashington", 14], presenter_duration["theodore", 17]),
        And(topic_duration["presidentwashington", 17], presenter_duration["theodore", 14]),
    )
)

# 5. The student who gave the presentation on President Washington spoke 6 minutes more than
# the student who gave the presentation on President Lincoln.
s.add(
    And(topic_duration["presidentwashington", 14], topic_duration["presidentlincoln", 8]),
)

# 6. Theodore was either the presenter who gave the presentation on President Fillmore
# or the presenter who spoke for 17 minutes.
s.add(
    Or(presenter_topic["theodore", "presidentfillmore"], presenter_duration["theodore", 17])
)

# 7. The student who spoke for 17 minutes didn't talk about President Coolidge.
s.add(Not(topic_duration["presidentcoolidge", 17]))

if s.check() == sat:
    print("satisfiable")
    model = s.model()
    for presenter in presenters:
        valid_duration = None
        valid_topic = None
        for duration in durations:
            valid = is_true(model.evaluate(presenter_duration[presenter, duration], model_completion=True))
            if valid:
                valid_duration = duration
        for topic in topics:
            valid = is_true(model.evaluate(presenter_topic[presenter, topic], model_completion=True))
            if valid:
                valid_topic = topic
        print(f"presenter {presenter}, topic {valid_topic}, duration {valid_duration}")
else:
    print("unsatisfiable")
