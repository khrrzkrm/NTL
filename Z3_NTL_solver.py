from z3 import *
import random
from NTL_Struct import Norm, BinaryOperation
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)
domain = IntSort()
range_type = Event
# Declare the array with fixed length
trace = Array('trace', domain, range_type)
num_events= Int('num_events')
class ActionIndexMapping:
    def __init__(self):
        # Initialize an empty dictionary to store the action indices
        self.mapping = {}

    def add_action_index(self, action, index):
        # Add or update the action with the new index
        if action in self.mapping:
            # Append the index to the list if it's not already there
            if index not in self.mapping[action]:
                self.mapping[action].append(index)
        else:
            # Create a new entry with the index in a list
            self.mapping[action] = [index]

    def get_indices(self, action):
        # Return a copy of the list of indices for the action
        return self.mapping.get(action, [])
    def print_all(self):
        """Prints all actions and their associated indices."""
        for action, indices in self.mapping.items():
            print(f"Action: {action}, Indices: {indices}")
    def extract(self):
        """Returns a list of all indices from all actions."""
        labels = []
        for action, indices in self.mapping.items():
            labels.extend(indices)
        return labels


def z3_solver(formula):
    mapping = ActionIndexMapping()
    trace = Const('trace', Trace)
    max_index = Int('max_index')
    match formula:
        case Norm(norm_type="O", action=action, interval_set=interval_set):
            sol=Solver()
            x=random.randint(1, 2)
            label='pt'+str(x)+action
            #label= 'j'
            mapping.add_action_index(action,label)
            i= Int(label)
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
            

        case Norm(norm_type="F", action=action, interval_set=interval_set) if  formula.interval_set:
            sol=Solver()
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
            if len(timed_constraints.assertions()) != 1:
                timed_constraints= And(timed_constraints.assertions())
            else:
                timed_constraints= timed_constraints.assertions()[0]
            sol.add(ForAll([i], Implies(timed_constraints, And(i <= num_events, tarction != action))))

            
        case BinaryOperation(left=left, operator=op, right=right):
            sol_l = z3_solver(left)
            sol_r = z3_solver(right)
            if op == "&":
                sol=Solver()
                sol= sol_l
                combine_solvers_and(sol, sol_r)
            elif op == "||":
                sol=Solver()
                combine_solvers_or(sol, sol_l, sol_r)

        case _:
            print("Unsupported formula type", file=sys.stderr)
    return sol
        
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

def synthetize(sol):
    for x in range(1,8):
        print(x)
        rules=sol.assertions()
        temp_sol=Solver()
        temp_sol.add(rules)
        num_events= Int('num_events')
        temp_sol.add(num_events == x)
        
        timestamps = [Event.time_stamp(Select(trace, i)) for i in range(x)]
        temp_sol.add(Distinct(timestamps))
        for i in range(x-1):
            temp_sol.add(Event.time_stamp(Select(trace, i)) >=0)
    #sol.add(ordering_constraint)
        for i in range(x - 1):
            temp_sol.add(Event.time_stamp(Select(trace, i)) < Event.time_stamp(Select(trace, i + 1)))
        for c in temp_sol.assertions():
                print(c)
        if temp_sol.check() == sat:
            m = temp_sol.model()
            print("Satisfiable trace with minimum length:")
            for i in range(x):
                event = Select(trace, i)
                action = m.evaluate(Event.action(event)).as_string()
                time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
                print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
            return
        else:
            temp_sol.reset()
            print("adding one more")
    print("No satisfiable trace exists.")
   
        





                
