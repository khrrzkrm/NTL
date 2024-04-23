from z3 import *

# Define the Event type with action and time_stamp
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()

# Define the trace as an array of events indexed by integer
Trace = ArraySort(IntSort(), Event)

# Use the Optimize solver for minimization
opt = Optimize()

def get_input():
    input_constraints = []
    print("Enter your constraints in the format 'O/F t_min t_max action'. Type 'end' to finish.")
    while True:
        inp = input("Enter constraint (or 'end' to finish): ")
        if inp.lower() == "end":
            break
        parts = inp.split()
        if len(parts) != 4:
            print("Invalid input format. Please follow the format 'O/F t_min t_max action'.")
            continue
        op, t_min, t_max, action = parts
        if op not in ['O', 'F'] or not t_min.isdigit() or not t_max.isdigit():
            print("Invalid operation or time bounds. Please correct and try again.")
            continue
        input_constraints.append((op, int(t_min), int(t_max), action))
    return input_constraints

input_constraints = get_input()

# Trace and variables
trace = Const('trace', Trace)
max_index = Int('max_index')
opt.add(max_index >= 0)  # Ensure at least one event exists

# Process constraints
for op, t_min, t_max, action in input_constraints:
    if op == "O":
        obligation_found = False
        for i in range(100):  # Define a reasonable upper limit for event indices
            event = Select(trace, i)
            is_action = Event.action(event) == StringVal(action)
            in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
            obligation_found = Or(obligation_found, And(is_action, in_time))
            opt.add_soft(Implies(is_action, i <= max_index))
        opt.add(obligation_found)

    elif op == "F":
        for i in range(100):
            event = Select(trace, i)
            is_action = Event.action(event) == StringVal(action)
            in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
            opt.add(Implies(is_action, Not(in_time)))

# Minimize the maximum index used in the trace
opt.minimize(max_index)

# Solve and output the trace
if opt.check() == sat:
    m = opt.model()
    highest_index = m.evaluate(max_index).as_long()
    print("Satisfiable trace with minimum length:")
    for i in range(highest_index + 1):
        event = m.evaluate(Select(trace, i))
        action = m.evaluate(Event.action(event)).as_string()
        time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
        if action != "":
            print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
else:
    print("No satisfiable trace exists.")
