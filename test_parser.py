import unittest
from NTL_ParsertoAst import *
from Z3_NTL_solver import *
input_string = "O a {[101,101]}"
result=process_input(input_string)
print(type(result))
z3_solver(result)



# class TestNormParser(unittest.TestCase):
#     def test_simple_norm(self):
#         input_string = "O a {[1,5]}"
#         expected_output = "O [[1, 5]] a"  # Adjust expected output based on your AST structure and __repr__ implementations
#         self.assertEqual(process_input(input_string), expected_output)

#     def test_binary_operation(self):
#         input_string = "F b {[3,inf]}"
#         expected_output = " F [[3, float('inf')]] b"
#         self.assertEqual(process_input(input_string), expected_output)

#     def test_complex_expression(self):
#         input_string = "O a {[1,3]} || (F b {[2,4]} & O c {[5,7]})"
#         expected_output = "(O [[1, 3]] a || (F [[2, 4]] b & O [[5, 7]] c))"
#         self.assertEqual(process_input(input_string), expected_output)

#     def test_failed_parsing(self):
#         input_string = "O a [1,5]"  # Missing braces around intervals
#         expected_output = "Failed to parse the input."
#         self.assertEqual(process_input(input_string), expected_output)

# if __name__ == '__main__':
#     unittest.main()
