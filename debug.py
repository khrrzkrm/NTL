from pyparsing import Word, nums, alphas, Suppress, Literal, Group, Forward, Optional, delimitedList, oneOf, ParseException

class Norm:
    def __init__(self, operator, action, intervals):
        self.operator = operator
        self.action = action
        self.intervals = intervals

class LogicalOperator:
    def __init__(self, operator):
        self.operator = operator

class Formula:
    def __init__(self, left, logical_operator, right=None):
        self.left = left
        self.logical_operator = logical_operator
        self.right = right

def generate_ast(parsed_formula):
    print("Parsed Formula:", parsed_formula)
    if isinstance(parsed_formula, list):
        if len(parsed_formula) == 3:  # Term or nested formula without parentheses
            if isinstance(parsed_formula[0], str):  # Operator
                operator = parsed_formula[0]
                action = parsed_formula[1]
                intervals = parsed_formula[2]
                return Norm(operator, action, intervals)
            else:  # Logical operator
                left = generate_ast(parsed_formula[0])
                logical_operator = parsed_formula[1]
                right = generate_ast(parsed_formula[2])
                return Formula(left, LogicalOperator(logical_operator), right)
        elif len(parsed_formula) == 1:  # Single term
            return generate_ast(parsed_formula[0])
        elif len(parsed_formula) == 5:  # Nested formula with parentheses
            if isinstance(parsed_formula[1], list):
                return generate_ast(parsed_formula[1]) if parsed_formula[1][0] != '(' else generate_ast(parsed_formula[2])
            else:
                return generate_ast(parsed_formula[0])
    else:
        return parsed_formula  # Return leaf node




def main():
    # Define tokens
    integer = Word(nums)
    operator = Literal('O') | Literal('F')
    action = Word(alphas)
    logical_operator = oneOf('& ||')
    inf_symbol = Literal('inf')
    interval = Suppress('[') + integer.setParseAction(lambda t: int(t[0])) + Suppress(',') + (integer | inf_symbol).setParseAction(lambda t: float('inf') if t[0] == 'inf' else int(t[0])) + Suppress(']')
    interval.setParseAction(lambda t: (t[0], t[1]) if t[0] <= t[1] else ParseException("Interval must satisfy a <= b"))
    interval_set = Suppress('{') + delimitedList(interval, ',') + Suppress('}')

    # Define grammar for term
    term = Forward()
    term <<= Group(operator + action + interval_set) | Group('(' + term + logical_operator + term + ')')

    # Define grammar for formula
    formula = Forward()
    formula <<= term + Optional(logical_operator + formula)

    # Prompt user to enter a formula
    input_formula = input("Enter your formula: ")

    # Parse input using the defined grammar
    parsed_formula = formula.parseString(input_formula)

    # Generate AST
    ast = generate_ast(parsed_formula)

    # Print AST
    print("AST:", ast)

if __name__ == "__main__":
    main()
