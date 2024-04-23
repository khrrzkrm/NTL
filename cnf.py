from pyparsing import *
from z3 import *

# Define the Event datatype in Z3
Event = Datatype('Event')
Event.declare('mk_event', ('action', StringSort()), ('time_stamp', IntSort()))
Event = Event.create()

# Grammar definitions
integer = pyparsing_common.integer
action = Word(alphas)  # Actions are alphabetic
interval = Suppress('[') + Group(integer + Suppress(',') + integer) + Suppress(']')
intervals = Suppress('{') + Group(delimitedList(interval)) + Suppress('}')
norm_type = oneOf("O F")
norm = Group(norm_type + action + intervals)

# Logical operators and expression handling
expr = infixNotation(norm, [
    (Literal("&"), 2, opAssoc.LEFT),
    (Literal("||"), 2, opAssoc.LEFT),
])

def parse(input_string):
    try:
        # Adding verbose diagnostics
        result = expr.parseString(input_string, parseAll=True)
        print("Parsing succeeded.")
        return result
    except ParseException as pe:
        print("Parsing error: ", pe)
        print("Location: ", pe.loc)
        print("Line: ", pe.lineno, "Column: ", pe.col)
        print("Input around error: ", input_string[max(0, pe.loc - 10):pe.loc + 10])
        return None

# Example usage
input_data = "O a {[1,3], [5,7]} & F b {[2,4]}"
result = parse(input_data)
if result:
    print("Parsed successfully:", result.asList())
else:
    print("Failed to parse input.")
