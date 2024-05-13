from z3 import *
import random
from NTL_Struct import Norm, BinaryOperation, Reminder
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)
domain = IntSort()
range_type = Event
# Declare the array with fixed length
trace = Array('trace', IntSort(), Event)
num_events= Int('num_events')

def z3_solver(formula: BinaryOperation) -> (z3.Solver,Reminder):
    trace = Const('trace', Trace)
    max_index = Int('max_index')
    match formula:
        case Norm(norm_type="O", action=action, interval_set=interval_set):
            sol=Solver()
            x=random.randint(1, 100)
            label='pt'+str(x)+action
            #label= 'j'
            i= Int(label)
            r = Reminder()
            if not formula.interval_set:  # Check if the interval set is empty
                print("No satisfiable trace exists: Empty set of interval on Obligation")  
                sol.add(BoolVal(False))
                return sol
            else:
                event_i= Select(trace, i)
                tarction=Event.action(event_i)
                ttime=Event.time_stamp(event_i)
                timed_constraints= Solver()
                for [t_min,t_max] in formula.interval_set:
                    if (t_max==float('inf')):
                        timed_constraints.add(ttime>=t_min) 
                    else:
                        timed_constraints.add(And(ttime>=t_min,ttime<=t_max ))
            if len(timed_constraints.assertions()) != 1:
                timed_constraints= Or(timed_constraints.assertions())
            else:
                timed_constraints= timed_constraints.assertions()[0]
            sol.add(Exists([i],And(0<=i, i<=num_events,tarction==action,timed_constraints)))
            r.add_element("time_stamp(trace[{}])".format(i))
            

        case Norm(norm_type="F", action=action, interval_set=interval_set) if  formula.interval_set:
            sol=Solver()
            r=Reminder()
            x=random.randint(1, 2)
            label='pt'+str(x)+action
            mapping.add_action_index(action,label)
            i= Int(label)
            event_i= Select(trace, i)
            tarction=Event.action(event_i)
            ttime=Event.time_stamp(event_i)
            timed_constraints= Solver()
            for [t_min,t_max] in formula.interval_set:
                if (t_max==float('inf')):
                    timed_constraints.add(ttime>=t_min) 
                else:
                    timed_constraints.add(And(ttime>=t_min,ttime<=t_max ))
                    max=t_max
            if len(timed_constraints.assertions()) != 1:
                timed_constraints= And(timed_constraints.assertions())
            else:
                timed_constraints= timed_constraints.assertions()[0]
            sol.add(ForAll([i], Implies(timed_constraints, And(i <= num_events, tarction != action))))
            r.add((max_value(interval_set).asString()))
            
            
        case BinaryOperation(left=left, operator=op, right=right):
            r=Reminder()
            sol_l,leftr = z3_solver(left)
            sol_r,rightr = z3_solver(right)
            sol=Solver()
            if op == "&":
                sol= sol_l
                combine_solvers_and(sol, sol_r)
            elif op == "||":
                combine_solvers_or(sol, sol_l, sol_r)
                r.add_tuple(rightr,leftr)
            if op == ";":
                sol,r = z3_solver(left,"&",(right.add(leftr)))

        case _:
            print("Unsupported formula type", file=sys.stderr)
    return sol,r
        
def combine_solvers_and(left_solver, right_solver):
    for constraint in right_solver.assertions():
        left_solver.add(constraint)
              
def combine_solvers_or(main_solver, left_solver, right_solver):
    # Create a new intermediate solver to hold combined OR conditions
    or_solver = Solver()
    lefts= left_solver.assertions()
    rights= right_solver.assertions()
    or_solver.add(Or(And(lefts), And(rights)))
    for constraint in or_solver.assertions():
        main_solver.add(constraint)
        
def combine_solvers_and(left_solver, right_solver):
    for constraint in right_solver.assertions():
        left_solver.add(constraint)

def synthetize(sol):
    num_events= Int('num_events')
    for x in range(0,10):
        (solver,r)=z3_solver(sol)
        rules=solver.assertions()
        temp_sol=Solver()
        temp_sol.add(num_events == x)
        temp_sol.add(rules)
        num_events= Int('num_events')
        i=Int('i')
        temp_sol.add(ForAll(i, Event.time_stamp(Select(trace, i)) >= 0))
        for i in range(x):
            temp_sol.add(Event.time_stamp(Select(trace, i)) < Event.time_stamp(Select(trace, i + 1)))
        for c in temp_sol.assertions():
                print(c)
        if temp_sol.check() == sat:
            m = temp_sol.model()
            event0 = Select(trace, 0)
            action0=m.evaluate(Event.action(event0)).as_string()
            if (action0==''):
                print("empty trace satisfies your formula")
            else:
                for i in range(x+1):
                    event = Select(trace, i)
                    action = m.evaluate(Event.action(event)).as_string()
                    time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
                    print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
            return
        else:
            temp_sol.reset()
            print("adding one more")
    print("No satisfiable trace exists.")
   
        





                
