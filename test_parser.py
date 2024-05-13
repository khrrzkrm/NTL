import unittest
from reminder import *
from NTL_ParsertoAst import *
from z3_precise import *
from NTL_Struct import BinaryOperation
#from Z3_NTL_solver import *


input_string = "((  O e {[1,3]} || F b {[1,inf]} ) ; O d {[1,3]} );  O w {[1,3]}"
#input_string = "(O a{[1,4]} & (O b {[8,8]} || F c {[11,15]}) & F c {[11,14]}); O d {[4,5]}"
# parsing= parse_norms(input_string)
# print(parsing)
parsed= process_input(input_string)
# # z=count_obligations(parsed)
# # print("num events:",z)
print(parsed)
synthetize(parsed)


#for z3 precise
#result=process_input(input_string)
# print(str(result))
# synthetize(result,4)


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
