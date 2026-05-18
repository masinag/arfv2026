from z3 import *

# Exercise 2.4: Receptionist
# You are a receptionist in a prestigious hotel and you are waiting for 5 new guests.
# There are 5 available rooms, but you don’t know their preferences about the room
# they want to book until the last moment:
# - Guest A would like to choose room 1 or 2.
# - Guest B would like to choose a room with an even number.
# - Guest C would like the first room.
# - Guest D has the same behavior as user B.
# - Guest E would like one of the external rooms.
# Supposing the guests come one after the other, is there a moment where it is not
# possible to help every guest? How many guests can be sorted without problems?

rooms = [room for room in range(1, 6)]
guests = [guest for guest in ["A", "B", "C", "D", "E"]]

preference = {
    "A": [1, 2],
    "B": [2, 4],
    "C": [1],
    "D": [2, 4],
    "E": [1, 5]
}

for model in range(1, len(guests)+ 1):
    s = Solver()
    print("possible model: ", model)
    possible = True
    current_guest = guests[:model]
    guest_room = {
        (guest, room): Bool(f"guest{guest}room{room}")
        for guest in current_guest
        for room in rooms
    }

    # one room, one guest
    for guest in current_guest:
        s.add(
            AtMost(*[guest_room[guest, room] for room in rooms], 1),
            Or(*[guest_room[guest, room] for room in preference[guest]])
        )

    # one guest, one room
    for room in rooms:
        s.add(
            AtMost(
                *[guest_room[guest, room] for guest in current_guest], 1
            )
        )
    print("possible model with guest", current_guest)
    if s.check() == sat:
        print("satisfiable")

        possible_model = s.model()

        for guest in current_guest:
            for room in rooms:
                if is_true(possible_model.evaluate(guest_room[guest, room], model_completion=True)):
                    print("guest: ", guest, "room: ", room)

    else:
        print("unsatisfiable")
        print("problem with guest", current_guest)
        print(model - 1, "guests can be sorted without problems")
        break




