import unittest
from NTL_ParsertoAst import *
from Z3_NTL_solver import *
input_string = " O a {[3,5]} & O b {[7,9]}"
result=process_input(input_string)

print(str(result))
synthetize(z3_solver(result))


# class TestNormParser(unittest.TestCase):
#     def test_simple_EmptyNorm(self):
#         input_string = "O a {[]}"
#         expected_output = "O [] a"  
#         self.assertEqual(str(process_input(input_string)), expected_output)
#     def test_simple_ContainsEmptyinterval(self):
#         input_string = "O a {[], [4,5]}"
#         expected_output = "O [[4, 5]] a"  
#         self.assertEqual(str(process_input(input_string)), expected_output)    
#     def test_simple_norm(self):
#         input_string = "O a {[1,5]}"
#         expected_output = "O [[1, 5]] a"  
#         self.assertEqual(str(process_input(input_string)), expected_output)
#     def test_complex_2depth(self):
#         input_string = "O a {[1,3]} || (F b {[2,4]} & O c {[5,7]})"
#         expected_output = "(O [[1, 3]] a || (F [[2, 4]] b & O [[5, 7]] c))"
#         self.assertEqual(str(process_input(input_string)), expected_output)
#     def test_complex_depth(self):
#         input_string = "O a {[1,3]} || ((F b {[2,4]} & O c {[5,7]}) || O a {[1,3],[7,inf]})"
#         expected_output = "(O [[1, 3]] a || ((F [[2, 4]] b & O [[5, 7]] c) || O [[1, 3], [7, inf]] a))"
#         self.assertEqual(str(process_input(input_string)), expected_output)    

#     def test_failed_parsing(self):
#         input_string = "O a [1,5]"  # Missing braces around intervals
#         expected_output = "Failed to parse the input."
#         self.assertEqual(process_input(input_string), expected_output)

# if __name__ == '__main__':
#      unittest.main()
