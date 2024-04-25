from z3 import And, Or, Not, Implies, Solver, AstVector
import sys

# Assuming Event is defined elsewhere in your module correctly
def z3_solver(formula):
    constraints = AstVector()
    
    match formula:
        case Norm(norm_type="O", action=action, interval_set=interval_set) if interval_set:
            for [t_min, t_max] in interval_set:
                for i in range(100):  # Assuming you have a predefined range or based on trace length
                    event = Select(trace, i)
                    is_action = Event.action(event) == StringVal(action)
                    in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
                    constraints.push(And(is_action, in_time))
                    
        case Norm(norm_type="F", action=action, interval_set=interval_set) if interval_set:
            for [t_min, t_max] in interval_set:
                for i in range(100):
                    event = Select(trace, i)
                    is_action = Event.action(event) == StringVal(action)
                    in_time = And(Event.time_stamp(event) >= t_min, Event.time_stamp(event) <= t_max)
                    constraints.push(Implies(is_action, Not(in_time)))
                    
        case BinaryOperation(left=left, operator=op, right=right):
            left_constraints = z3_solver(left)
            right_constraints = z3_solver(right)
            if op == "&&":
                constraints.push(And(left_constraints, right_constraints))
            elif op == "||":
                constraints.push(Or(left_constraints, right_constraints))

        case _:
            print("Unsupported formula type", file=sys.stderr)
    
    return constraints
