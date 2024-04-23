from z3 import *
from NTL_Struct import *
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)
opt = Optimize()
trace = Const('trace', Trace)
max_index = Int('max_index')
opt.add(max_index >= 0)

# Define the trace as an array of events indexed by integer

def z3_solver(formula):
    if isinstance(formula, Norm):
        action=formula.action
        if formula.norm_type=="O":
            obligation_found = False
            for i in range(100):  # Define a reasonable upper limit for event indices
                event = Select(trace, i)
                is_action = Event.action(event) == StringVal(action)
                for [t_min,t_max] in formula.interval_set:
                    if (t_max==float('inf')):
                        in_time = Event.time_stamp(event) >= t_min
                        obligation_found = Or(obligation_found, And(is_action, in_time))
                    else:
                        in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
                        obligation_found = Or(obligation_found, And(is_action, in_time))
                opt.add(obligation_found)
        elif op == "F":
            for i in range(100):
                event = Select(trace, i)
                is_action = Event.action(event) == StringVal(action)
                for [t_min,t_max] in formula.interval_set:
                    if (t_max==inf):
                        in_time = Event.time_stamp(event) >= t_min
                    else:
                        in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
                    opt.add(Implies(is_action, Not(in_time)))
        else: print("norms missing")
    else:
        print("TBA")
    opt.minimize(max_index)

# Solve and output the trace
    if opt.check() == sat:
        m = opt.model()
        highest_index = m.evaluate(max_index).as_long()
        print("Satisfiable trace with minimum length:")
        for i in range(highest_index + 1):
            event = m.evaluate(Select(trace, i))
            action = m.evaluate(Event.action(event)).as_string()
            time_stamp = Event.time_stamp(event)
            if action != "":
                print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
    else:
        print("No satisfiable trace exists.")




                
