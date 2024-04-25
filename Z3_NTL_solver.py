from z3 import *
import random
from NTL_Struct import Norm, BinaryOperation
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()
Trace = ArraySort(IntSort(), Event)


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
    num_events=10
    trace = Const('trace', Trace)
    max_index = Int('max_index')
    match formula:
        case Norm(norm_type="O", action=action, interval_set=interval_set):
            opt=Optimize()
            x=random.randint(1, 2)
            label='pt'+str(x)+action
            mapping.add_action_index(action,label)
            i= Int(label)
            if not formula.interval_set:  # Check if the interval set is empty
                print("No satisfiable trace exists: Empty set of interval on Obligation")  
                opt.add(BoolVal(False))
                return opt
            else:
                event_i= Select(trace, i)
                tarction=Event.action(event_i)
                ttime=Event.time_stamp(event_i)
                timed_constraints= Optimize()
                for [t_min,t_max] in formula.interval_set:
                    if (t_max==float('inf')):
                        timed_constraints.add(ttime>=t_min) 
                    else:
                        timed_constraints.add(And(ttime>=t_min,ttime<=t_max ))
            timed_constraints= Or(timed_constraints.assertions())
            opt.add(And((i<num_events),tarction==action,timed_constraints))
        case BinaryOperation(left=left, operator=op, right=right):
            opt_l = z3_solver(left)
            opt_r = z3_solver(right)
            if op == "&":
                opt=Optimize()
                opt= opt_l
                combine_solvers_and(opt, opt_r)
            elif op == "||":
                opt=Optimize()
                combine_solvers_or(opt, opt_l, opt_r)

        case _:
            print("Unsupported formula type", file=sys.stderr)
    #mapping.print_all()
    indicess=mapping.extract()
    print(indicess)
    opt.add(Distinct(*indicess))
    return opt
        
def combine_solvers_and(left_solver, right_solver):
    for constraint in right_solver.assertions():
        left_solver.add(constraint)    
              

            # else:
            #     for i in range(num_events):  # Define a reasonable upper limit for event indices
            #         event = Select(trace, i)
            #         is_action = Event.action(event) == StringVal(action) 
            #         for [t_min,t_max] in formula.interval_set:
            #             if (t_max==float('inf')):
            #                 in_time = And(Event.time_stamp(event) >= t_min,Event.time_stamp(event) >= 0)
            #                 obligation_found = Or(obligation_found, And(is_action, in_time))
            #             else:
            #                 in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
            #             for c in in_times.assertions():
            #                 print(c)
            #             obligation_found = Or(obligation_found, And(is_action),Or(in_times.assertions()))
            #         opt.add(obligation_found)
                    
                   
#         case Norm(norm_type="F", action=action, interval_set=interval_set) if interval_set:
#             opt=Optimize()
#             if not formula.interval_set:  # Check if the interval set is empty
#                 print("Trivial Norm, please remove it from you formula ")
#                 return opt.add(BoolVal(True))
#             else:
#                 not_in_time_all = True
#                 obligation_found = False
#                 for i in range(num_events):
#                     event = Select(trace, i)
#                     is_action = Event.action(event) == StringVal(action)
#                     for [t_min,t_max] in formula.interval_set:
#                         if (t_max==float('inf')):
#                             in_time = And(Event.time_stamp(event) >= t_min)
#                             not_in_time_all = And(not_in_time_all, Not(in_time))
#                         else:
#                             in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
#                             in_time2 = Or(Event.time_stamp(event) < t_min, Event.time_stamp(event) > t_max)
#                             obligation_found = Or(obligation_found, And(is_action, in_time2))
#                             not_in_time_all = And(not_in_time_all, Not(in_time))    
#                     #constraints.push(Xor(is_action, in_time))
#                         opt.add(Or(Implies(is_action, not_in_time_all), obligation_found))
#                         #constraints.push(Implies(is_action, not_in_time_all))
#                     opt.add(Event.time_stamp(event) >= 0)
#                     #opt.add(Implies(is_action, Not(in_time))) #beautiful buf of Z3 when action has length>1
        

    

def combine_solvers_or(main_solver, left_solver, right_solver):
    # Create a new intermediate solver to hold combined OR conditions
    or_solver = Optimize()
    lefts= left_solver.assertions()
    rights= right_solver.assertions()
    or_solver.add(Or(And(lefts), And(rights)))
    for constraint in or_solver.assertions():
        main_solver.add(constraint)

def synthetize(opt):
    num_events=1
    max_index = Int('max_index')
    trace = Array('trace', IntSort(), Event)
    # timestamps = [Event.time_stamp(Select(trace, i)) for i in range(num_events)]
    # opt.add(Distinct(timestamps))
    for c in opt.assertions():
        print(c)
    opt.minimize(max_index)     
    if opt.check() == sat:
        m = opt.model()
        highest_index = m.evaluate(max_index).as_long()
        if highest_index == -1:
            print("empty trace satisifies the formula")
        elif highest_index >-1:
            print("Satisfiable trace with minimum length:")
            for i in range(highest_index + 1):
                event = m.evaluate(Select(trace, i))
                action = m.evaluate(Event.action(event)).as_string()
                time_stamp = m.evaluate(Event.time_stamp(event)).as_long()
                print(f"Event {i}: Action = {action}, Time Stamp = {time_stamp}")
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
        





                
