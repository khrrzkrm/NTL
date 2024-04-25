from z3 import *

Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)

trace = Const('trace', Trace)
pt1a = Int('pt1a')
pt2b = Int('pt2b')
solver = Solver()

# Adding constraints on index ranges to ensure they are within valid trace bounds
solver.add(pt1a >= 0, pt1a < 10)
solver.add(pt2b >= 0, pt2b < 10)

solver.add(Event.action(Select(trace, pt1a)) == StringVal("a"))
solver.add(And(Event.time_stamp(Select(trace, pt1a)) >= 3, Event.time_stamp(Select(trace, pt1a)) <= 5))

solver.add(Event.action(Select(trace, pt2b)) == StringVal("b"))
solver.add(And(Event.time_stamp(Select(trace, pt2b)) >= 7, Event.time_stamp(Select(trace, pt2b)) <= 9))

solver.add(pt1a != pt2b)  # Ensuring different indices for a and b

if solver.check() == sat:
    model = solver.model()
    a_index = model[pt1a]
    b_index = model[pt2b]
    print("Satisfiable trace with minimum length:")
    print(f"Event at index {a_index}: Action = 'a', Time Stamp = {model.evaluate(Event.time_stamp(Select(trace, a_index)))}")
    print(f"Event at index {b_index}: Action = 'b', Time Stamp = {model.evaluate(Event.time_stamp(Select(trace, b_index)))}")
else:
    print("Unsatisfiable")
