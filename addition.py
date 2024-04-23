from pyparsing import *

# Define the grammar
integer = pyparsing_common.integer
operand = integer | '(' + infixNotation(integer, [
    ('+', 2, opAssoc.LEFT),
]) + ')'

# Parse the input formula
# Parse the input formula
def parse_expression(input_string):
    try:
        return operand.parseString(input_string, parseAll=True)[0]
    except ParseException as pe:
        print("Parsing error:", str(pe))
        return None


# Define AST node classes
class Integer:
    def __init__(self, value):
        self.value = value

class Addition:
    def __init__(self, left, right):
        self.left = left
        self.right = right

# Generate AST from parsed expression
def generate_ast(parsed_expr):
    if isinstance(parsed_expr, ParseResults):
        if len(parsed_expr) == 1:
            return generate_ast(parsed_expr[0])
        else:
            operator = parsed_expr[1]
            if operator == '+':
                left = generate_ast(parsed_expr[0])
                right = generate_ast(parsed_expr[2])
                return Addition(left, right)
    else:
        return Integer(parsed_expr)

# Main function
def main():
    input_string = input("Enter your expression: ")
    parsed_expr = parse_expression(input_string)
    if parsed_expr:
        print("Parsed Expression:", parsed_expr)
        ast = generate_ast(parsed_expr)
        print("AST:", ast)
    else:
        print("Failed to parse the input.")

if __name__ == "__main__":
    main()
