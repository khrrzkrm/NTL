from z3 import *
from NTL_Struct import Norm, BinaryOperation
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)

trace = Const('trace', Trace)
max_index = Int('max_index')



# Define the trace as an array of events indexed by integer

def z3_solver(formula):
    constraints = AstVector()
    if isinstance(formula, Norm):
        action=formula.action
        print(action)
        if formula.norm_type=="O":
            if not formula.interval_set:  # Check if the interval set is empty
                print("No satisfiable trace exists: Empty set of interval on Obligation")  
                return
            else:
                obligation_found = False
                for i in range(2):  # Define a reasonable upper limit for event indices
                    event = Select(trace, i)
                    is_action = Event.action(event) == StringVal(action) 
                    for [t_min,t_max] in formula.interval_set:
                        if (t_max==float('inf')):
                            in_time = And(Event.time_stamp(event) >= t_min,Event.time_stamp(event) >= 0)
                            obligation_found = Or(obligation_found, And(is_action, in_time))
                        else:
                            in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max,Event.time_stamp(event) >= 0)
                            obligation_found = Or(obligation_found, And(is_action, in_time))
                    constraints.push(obligation_found)
                    #solver.push(obligation_found)
                   
        elif formula.norm_type=="F":
            if not formula.interval_set:  # Check if the interval set is empty
                print("Trivial Norm, please remove it from you formula ")
                return
            else:
                obligation_found = False
                for i in range(10):
                    event = Select(trace, i)
                    is_action = Event.action(event) == StringVal(action)
                    for [t_min,t_max] in formula.interval_set:
                        if (t_max==float('inf')):
                            in_time = And(Event.time_stamp(event) >= t_min,Event.time_stamp(event) >= 0)
                            in_time2 = And(Event.time_stamp(event) < t_min,Event.time_stamp(event) >= 0)
                            obligation_found = And(obligation_found, And(is_action, in_time2))
                        else:
                            in_time = And(Event.time_stamp(event) >= t_min,Event.time_stamp(event) <= t_max,Event.time_stamp(event) >= 0 )
                            in_time2 = And(Event.time_stamp(event) > t_min,Event.time_stamp(event) >t_max,Event.time_stamp(event) >= 0)
                            obligation_found = Or(obligation_found, And(is_action, in_time2))
                    #constraints.push(Xor(is_action, in_time))
                    constraints.push(And(Implies(is_action, Not(in_time)),obligation_found))
                    #opt.add(Implies(is_action, Not(in_time))) #beautiful buf of Z3 when action has length>1
        
    else:
        print("tba")

    return constraints
        
          
    
def synthetize(constraints):
    opt = Optimize()
    opt.add(max_index >= 0)
    for c in constraints:
        opt.add(c)
    opt.minimize(max_index)
    print(type(opt.assertions()))
    for c in opt.assertions():
        print(c)
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
                print("The empty trace "" is the minimal satisfaction formula")
 
    else:
        print("No satisfiable trace exists.")
    # solver.add(max_index == 2)
    # print("the constraint contained in the solver just before checking sat are:")
    # for c in solver.assertions():
    #     print(c)
    # if solver.check() == sat:
    #     m = solver.model()
    #     highest_index = m.evaluate(max_index).as_long()
    #     print("Solution found:")
    #     print(f"max_index = {m.evaluate(max_index)}")
    #     for i in range(highest_index + 1):
    #         event = m.evaluate(Select(trace, i), model_completion=True)
    #         action = m.evaluate(Event.action(event)).as_string()
    #         time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
    #         print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")

        # for i in range(highest_index + 1)if is_int_value(m.evaluate(max_index)) else None:
        #     event = m.evaluate(Select(trace, i))
        #     action = m.evaluate(Event.action(event)).as_string()
        #     time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
        # if action != "":
        #     print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
        # else: 
        #     print("The empty trace "" is the minimal satisfaction formula")
 
    # else:
    #     print("No satisfiable trace exists.")    
        





                
