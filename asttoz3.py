from pyparsing import Literal, ParserElement

# Optional: Set default whitespace characters if not already set
ParserElement.setDefaultWhitespaceChars(' \t\r\n')

# Define the parser for 'inf'
infinity = Literal("inf").setParseAction(lambda _: float('inf'))

# Test the parser
def test_infinity():
    result = infinity.parseString("inf", parseAll=True)
    print("Parsed value:", result[0])
    print("Type of parsed value:", type(result[0]))

test_infinity()