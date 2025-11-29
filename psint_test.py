import pytest
from src.exceptions import ParseException, TypeMismatchException, UnmatchedBracketException, ZeroDivisionException, IndexOutOfRangeException
from src.parsers import boolean_parser, number_parser, code_block_parser, tokenize_input
import src.operations as ops
from src import config
from src.config import init_config
from src.ps_dict import PSDict

##-----------------------------------------------
# Parser Testing
class TestBooleanParsing:
    """Tests for parsing booleans"""
    def test_parse_true(self):
        result = boolean_parser("true")
        assert result is True
    
    def test_parse_false(self):
        result = boolean_parser("false")
        assert result is False

    def test_parse_rand(self):
        with pytest.raises(ParseException):
            boolean_parser("rand")

class TestNumberParsing:
    """Tests for parsing numbers"""
    def test_parse_int(self):
        result = number_parser(1)
        assert isinstance(result, int) and result == 1
    
    def test_parse_neg_int(self):
        result = number_parser(-1)
        assert isinstance(result, int) and result == -1

    def test_parse_float(self):
        result = number_parser(1.1)
        assert isinstance(result, float) and result == 1.1

    def test_parse_neg_float(self):
        result = number_parser(-1.1)
        assert isinstance(result, float) and result == -1.1

    def test_parse_non_num(self):
        with pytest.raises(ParseException):
            number_parser("one")

class TestCodeBlockParsing:
    """Tests for parsing code blocks"""
    def test_parse_code_block(self):
        result = code_block_parser("{ 1 add }")
        assert result == ["1", "add"]

    def test_parse_missing_bracket(self):
        with pytest.raises(ParseException):
            code_block_parser("{")
    
    def test_parse_empty_code_block(self):
        result = code_block_parser("{}")
        assert len(result) == 0

class TestTokenizeInput:
    """Tests input tokenizer"""
    def test_tokenize_code_block(self):
        result = tokenize_input("/inc {1 add } def")
        assert len(result) == 3 and result[0] == "/inc" and result[1] == "{1 add }" and result[2] == "def"
    
    def test_tokenize_empty(self):
        result = tokenize_input("")
        assert len(result) == 0
    
    def test_tokenize_single(self):
        result = tokenize_input("1")
        assert len(result) == 1 and result[0] == "1"
    
    def test_tokenize_two(self):
        result = tokenize_input("1 2")
        assert len(result) == 2 and result[0] == "1" and result[1] == "2"
    
    def test_tokenize_empty_code_block(self):
        result = tokenize_input("{}")
        assert len(result) == 1 and result[0] == "{}"
    
    def test_tokenize_unmatched_bracket(self):
        with pytest.raises(UnmatchedBracketException):
            tokenize_input("{")

##-----------------------------------------------
# Operator Testing
class TestAddOperator:
    """Tests for sub operator"""
    def test_add_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        ops.add_oper()
        assert config.oper_stack == [3]
    
    def test_add_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
           ops.add_oper()
    
    def test_add_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.add_oper()
    
    def test_add_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        ops.add_oper()
        assert config.oper_stack == [1,5]
    
    def test_add_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        ops.add_oper()
        assert config.oper_stack == [2]
    
    def test_add_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            ops.add_oper()

class TestSubOperator:
    """Tests for sub operator"""
    def test_sub_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([2,1])
        ops.sub_oper()
        assert config.oper_stack == [1]
    
    def test_sub_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            ops.sub_oper()
    
    def test_sub_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.sub_oper()
    
    def test_sub_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        ops.sub_oper()
        assert config.oper_stack == [1,-1]
    
    def test_sub_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        ops.sub_oper()
        assert config.oper_stack == [-4]
    
    def test_sub_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            ops.sub_oper()

class TestMulOperator:
    """Tests for mul operator"""
    def test_mul_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        ops.mul_oper()
        assert config.oper_stack == [2]
    
    def test_mul_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            ops.mul_oper()
    
    def test_mul_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.mul_oper()
    
    def test_mul_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        ops.mul_oper()
        assert config.oper_stack == [1,6]
    
    def test_mul_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        ops.mul_oper()
        assert config.oper_stack == [-3]
    
    def test_mul_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            ops.mul_oper()

class TestEqualOperator:
    """Tests the = operators"""
    def test_pop_single_element(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        ops.equal_oper()
        assert len(config.oper_stack) == 0
    
    def test_pop_two_elements(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        ops.equal_oper()
        assert len(config.oper_stack) == 1

    def test_pop_on_empty(self):
        config.oper_stack.clear()
        config.oper_stack.extend([])
        with pytest.raises(TypeMismatchException):
            ops.equal_oper()

class TestDivOperator:
    def test_div_basic(self):
        config.oper_stack.clear()
        config.oper_stack.extend([6, 3])
        ops.div_oper()
        assert config.oper_stack == [2.0]
    
    def test_div_fraction(self):
        config.oper_stack.clear()
        config.oper_stack.extend([7, 2])
        ops.div_oper()
        assert config.oper_stack == [3.5]

    def test_div_zero(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, 0])
        with pytest.raises(ZeroDivisionException):
            ops.div_oper()

    def test_div_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, "hello"])
        with pytest.raises(TypeMismatchException):
            ops.div_oper()

class TestIdivOperator:
    def test_idiv_positive(selfself):
        config.oper_stack.clear()
        config.oper_stack.extend([7, 3])
        ops.idiv_oper()
        assert config.oper_stack == [2]
    
    def test_idiv_negative_mixed(selfself):
        config.oper_stack.clear()
        config.oper_stack.extend([-7, 3])
        ops.idiv_oper()
        assert config.oper_stack == [-2]

    def test_idiv_negative_both(selfself):
        config.oper_stack.clear()
        config.oper_stack.extend([-7, -3])
        ops.idiv_oper()
        assert config.oper_stack == [2]

    def test_idiv_zero_div(selfself):
        config.oper_stack.clear()
        config.oper_stack.extend([1, 0])
        with pytest.raises(ZeroDivisionException):
            ops.idiv_oper()

class TestModOperator:
    def test_mod_basic(self):
        config.oper_stack.clear()
        config.oper_stack.extend([5, 3])
        ops.mod_oper()
        assert config.oper_stack == [2]

    def test_mod_negative_dividend(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-5, 3])
        ops.mod_oper()
        assert config.oper_stack == [-2]

    def test_mod_negative_divisor(self):
        config.oper_stack.clear()
        config.oper_stack.extend([5, -3])
        ops.mod_oper()
        assert config.oper_stack == [2]

    def test_mod_negative_both(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-5, -3])
        ops.mod_oper()
        assert config.oper_stack == [-2]

    def test_mod_zero_divisor(self):
        config.oper_stack.clear()
        config.oper_stack.extend([5, 0])
        with pytest.raises(ZeroDivisionException):
            ops.mod_oper()

    def test_mod_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.extend([5, 3.2])
        with pytest.raises(TypeMismatchException):
            ops.mod_oper()

class TestAbsOperator:
    def test_abs_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(-5)
        ops.abs_oper()
        assert config.oper_stack == [5]

    def test_abs_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.14)
        ops.abs_oper()
        assert config.oper_stack == [3.14]

    def test_abs_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append(0)
        ops.abs_oper()
        assert config.oper_stack == [0]

    def test_abs_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.abs_oper()

    def test_abs_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.abs_oper()

class TestNegOperator:
    def test_neg_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        ops.neg_oper()
        assert config.oper_stack == [-5]

    def test_neg_negative_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(-7)
        ops.neg_oper()
        assert config.oper_stack == [7]
    
    def test_neg_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(2.5)
        ops.neg_oper()
        assert config.oper_stack == [-2.5]
    
    def test_neg_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append(0)
        ops.neg_oper()
        assert config.oper_stack == [0]

    def test_neg_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.neg_oper()

    def test_neg_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.neg_oper()

class TestCeilingOperator:
    def test_ceiling_positive_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.2)
        ops.ceiling_oper()
        assert config.oper_stack == [4]

    def test_ceiling_positive_exact(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.0)
        ops.ceiling_oper()
        assert config.oper_stack == [3]

    def test_ceiling_negative_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.2)
        ops.ceiling_oper()
        assert config.oper_stack == [-3]

    def test_ceiling_negative_exact(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.0)
        ops.ceiling_oper()
        assert config.oper_stack == [-3]

    def test_ceiling_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.ceiling_oper()

    def test_ceiling_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.ceiling_oper()

class TestFloorOperator:
    def test_floor_positive_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.7)
        ops.floor_oper()
        assert config.oper_stack == [3]
    
    def test_floor_positive_exact(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.0)
        ops.floor_oper()
        assert config.oper_stack == [3]

    def test_floor_negative_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.7)
        ops.floor_oper()
        assert config.oper_stack == [-4]
    
    def test_floor_negative_exact(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.0)
        ops.floor_oper()
        assert config.oper_stack == [-3]

    def test_floor_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.floor_oper()

    def test_floor_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.floor_oper()

class TestRoundOperator:
    def test_round_positive(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.2)
        ops.round_oper()
        assert config.oper_stack == [3]

    def test_round_positive_half(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.5)
        ops.round_oper()
        assert config.oper_stack == [4]

    def test_round_negative(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.2)
        ops.round_oper()
        assert config.oper_stack == [-3]

    def test_round_negative_half(self):
        config.oper_stack.clear()
        config.oper_stack.append(-3.5)
        ops.round_oper()
        assert config.oper_stack == [-4]

    def test_round_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append(0)
        ops.round_oper()
        assert config.oper_stack == [0]

    def test_round_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.round_oper()

    def test_round_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.round_oper()

class TestSqrtOperator:
    """Tests the sqrt operator"""
    def test_sqrt_positive_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(4)
        ops.sqrt_oper()
        assert config.oper_stack == [2.0]

    def test_sqrt_positive_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(2.25)
        ops.sqrt_oper()
        assert config.oper_stack == [1.5]

    def test_sqrt_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append(0)
        ops.sqrt_oper()
        assert config.oper_stack == [0.0]

    def test_sqrt_negative(self):
        config.oper_stack.clear()
        config.oper_stack.append(-4)
        with pytest.raises(TypeMismatchException):
            ops.sqrt_oper()

    def test_sqrt_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.sqrt_oper()

    def test_sqrt_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.sqrt_oper()

class TestDefOperator:
    """Tests the def operator"""
    def test_def_on_empty(self):
        config.oper_stack.clear()
        config.oper_stack.extend([])
        with pytest.raises(TypeMismatchException):
            ops.def_oper()
        
    def test_def_on_single(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            ops.def_oper()
    
    def test_def_on_non_named_constant_as_key(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        with pytest.raises(TypeMismatchException):
            ops.def_oper()

    def test_def_on_named_constant_as_key(self):
        init_config()
        config.oper_stack.clear()
        config.oper_stack.extend(['/x', 2])
        ops.def_oper()
        assert config.dict_stack[-1]['x'] == 2
    
    def test_def_on_constant_as_key(self):
        config.oper_stack.clear()
        config.oper_stack.extend([2, "/x"])
        with pytest.raises(TypeMismatchException):
            ops.def_oper()

class TestLengthOperator:
    def test_length_string(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        ops.length_oper()
        assert config.oper_stack == [5]

    def test_length_empty_string(self):
        config.oper_stack.clear()
        config.oper_stack.append("")
        ops.length_oper()
        assert config.oper_stack == [0]

    def test_length_dict(self):
        config.oper_stack.clear()
        d = PSDict()
        d['a'] = 1
        d['b'] = 2
        config.oper_stack.append(d)
        ops.length_oper()
        assert config.oper_stack == [2]

    def test_length_empty_dict(self):
        config.oper_stack.clear()
        d = PSDict()
        config.oper_stack.append(d)
        ops.length_oper()
        assert config.oper_stack == [0]

    def test_length_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(42)
        with pytest.raises(TypeMismatchException):
            ops.length_oper()

    def test_length_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.length_oper()

class TestGetOperator:
    def test_get_string(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(1)
        ops.get_oper()
        assert config.oper_stack == [ord('e')]

    def test_get_string_first_last(self):
        config.oper_stack.clear()
        config.oper_stack.append("hi")
        config.oper_stack.append(0)
        ops.get_oper()
        assert config.oper_stack == [ord('h')]

        config.oper_stack.append("hi")
        config.oper_stack.append(1)
        ops.get_oper()
        assert config.oper_stack[-1] == ord('i')

    def test_get_string_out_of_bounds(self):
        config.oper_stack.clear()
        config.oper_stack.append("hi")
        config.oper_stack.append(5)
        with pytest.raises(IndexOutOfRangeException):
            ops.get_oper()

    def test_get_string_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(123)
        config.oper_stack.append(0)
        with pytest.raises(TypeMismatchException):
            ops.get_oper()

    def test_get_string_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.get_oper()

class TestGetIntervalOperator:
    def test_getinterval_basic(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello world")
        config.oper_stack.append(6)  # index
        config.oper_stack.append(5)  # count
        ops.getinterval_oper()
        assert config.oper_stack == ["world"]

    def test_getinterval_start_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(0)
        config.oper_stack.append(2)
        ops.getinterval_oper()
        assert config.oper_stack == ["he"]

    def test_getinterval_full_string(self):
        config.oper_stack.clear()
        s = "hello"
        config.oper_stack.append(s)
        config.oper_stack.append(0)
        config.oper_stack.append(len(s))
        ops.getinterval_oper()
        assert config.oper_stack == [s]

    def test_getinterval_out_of_range(self):
        config.oper_stack.clear()
        config.oper_stack.append("hi")
        config.oper_stack.append(1)
        config.oper_stack.append(5)
        with pytest.raises(IndexOutOfRangeException):
            ops.getinterval_oper()

    def test_getinterval_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(42)
        config.oper_stack.append(0)
        config.oper_stack.append(1)
        with pytest.raises(TypeMismatchException):
            ops.getinterval_oper()  

    def test_getinterval_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.getinterval_oper()

class TestPutIntervalOperator:
    def test_putinterval_basic(self):
        config.oper_stack.clear()
        config.oper_stack.append("abcde")   # target
        config.oper_stack.append(2)         # index
        config.oper_stack.append("XY")      # source
        ops.putinterval_oper()
        assert config.oper_stack == ["abXYe"]

    def test_putinterval_start_zero(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(0)
        config.oper_stack.append("HE")
        ops.putinterval_oper()
        assert config.oper_stack == ["HEllo"]

    def test_putinterval_full_replacement(self):
        config.oper_stack.clear()
        config.oper_stack.append("abcd")
        config.oper_stack.append(0)
        config.oper_stack.append("WXYZ")
        ops.putinterval_oper()
        assert config.oper_stack == ["WXYZ"]

    def test_putinterval_out_of_range(self):
        config.oper_stack.clear()
        config.oper_stack.append("abcd")
        config.oper_stack.append(2)
        config.oper_stack.append("WXYZ")
        with pytest.raises(IndexOutOfRangeException):
            ops.putinterval_oper()

    def test_putinterval_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(123)
        config.oper_stack.append(0)
        config.oper_stack.append("XY")
        with pytest.raises(TypeMismatchException):
            ops.putinterval_oper()

    def test_putinterval_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.putinterval_oper()

class TestEqOperator:
    def test_eq_numbers(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(5)
        ops.eq_oper()
        assert config.oper_stack == [True]

    def test_eq_numbers_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(6)
        ops.eq_oper()
        assert config.oper_stack == [False]

    def test_eq_strings(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append("hello")
        ops.eq_oper()
        assert config.oper_stack == [True]

    def test_eq_strings_false(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append("world")
        ops.eq_oper()
        assert config.oper_stack == [False]

    def test_eq_booleans(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(True)
        ops.eq_oper()
        assert config.oper_stack == [True]

    def test_eq_dicts(self):
        config.oper_stack.clear()
        d1 = PSDict()
        d1['a'] = 1
        d2 = PSDict()
        d2['a'] = 1
        config.oper_stack.append(d1.dict)
        config.oper_stack.append(d2.dict)
        ops.eq_oper()
        assert config.oper_stack == [True]

    def test_eq_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.eq_oper()

class TestNeOperator:
    def test_ne_numbers_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(6)
        ops.ne_oper()
        assert config.oper_stack == [True]

    def test_ne_numbers_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(5)
        ops.ne_oper()
        assert config.oper_stack == [False]

    def test_ne_strings_true(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append("world")
        ops.ne_oper()
        assert config.oper_stack == [True]

    def test_ne_strings_false(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append("hello")
        ops.ne_oper()
        assert config.oper_stack == [False]

    def test_ne_booleans_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(False)
        ops.ne_oper()
        assert config.oper_stack == [True]

    def test_ne_dicts(self):
        config.oper_stack.clear()
        d1 = PSDict()
        d1['a'] = 1
        d2 = PSDict()
        d2['a'] = 1
        config.oper_stack.append(d1.dict)
        config.oper_stack.append(d2.dict)
        ops.ne_oper()
        assert config.oper_stack == [False]

    def test_ne_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.ne_oper()

class TestGtOperator:
    def test_ge_true_equal(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(5)
        ops.ge_oper()
        assert config.oper_stack == [True]

    def test_ge_true_greater(self):
        config.oper_stack.clear()
        config.oper_stack.append(10)
        config.oper_stack.append(5)
        ops.ge_oper()
        assert config.oper_stack == [True]

    def test_ge_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(3)
        config.oper_stack.append(5)
        ops.ge_oper()
        assert config.oper_stack == [False]

    def test_ge_float_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(5.5)
        config.oper_stack.append(5)
        ops.ge_oper()
        assert config.oper_stack == [True]

    def test_ge_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(5)
        with pytest.raises(TypeMismatchException):
            ops.ge_oper()

    def test_ge_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.ge_oper()

class TestGtOperator:
    def test_gt_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(10)
        config.oper_stack.append(5)
        ops.gt_oper()
        assert config.oper_stack == [True]

    def test_gt_false_equal(self):
        config.oper_stack.clear()
        config.oper_stack.append(7)
        config.oper_stack.append(7)
        ops.gt_oper()
        assert config.oper_stack == [False]

    def test_gt_false_less(self):
        config.oper_stack.clear()
        config.oper_stack.append(2)
        config.oper_stack.append(5)
        ops.gt_oper()
        assert config.oper_stack == [False]

    def test_gt_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.5)
        config.oper_stack.append(2.1)
        ops.gt_oper()
        assert config.oper_stack == [True]

    def test_gt_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(5)
        with pytest.raises(TypeMismatchException):
            ops.gt_oper()

    def test_gt_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.gt_oper()

class TestLeOperator:
    def test_le_true_equal(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(5)
        ops.le_oper()
        assert config.oper_stack == [True]

    def test_le_true_less(self):
        config.oper_stack.clear()
        config.oper_stack.append(2)
        config.oper_stack.append(5)
        ops.le_oper()
        assert config.oper_stack == [True]

    def test_le_false_greater(self):
        config.oper_stack.clear()
        config.oper_stack.append(10)
        config.oper_stack.append(3)
        ops.le_oper()
        assert config.oper_stack == [False]

    def test_le_float_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(3.5)
        config.oper_stack.append(4)
        ops.le_oper()
        assert config.oper_stack == [True]

    def test_le_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(5)
        with pytest.raises(TypeMismatchException):
            ops.le_oper()

    def test_le_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.le_oper()

class TestLtOperator:
    def test_lt_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(2)
        config.oper_stack.append(5)
        ops.lt_oper()
        assert config.oper_stack == [True]

    def test_lt_false_equal(self):
        config.oper_stack.clear()
        config.oper_stack.append(5)
        config.oper_stack.append(5)
        ops.lt_oper()
        assert config.oper_stack == [False]

    def test_lt_false_greater(self):
        config.oper_stack.clear()
        config.oper_stack.append(8)
        config.oper_stack.append(3)
        ops.lt_oper()
        assert config.oper_stack == [False]

    def test_lt_float(self):
        config.oper_stack.clear()
        config.oper_stack.append(2.5)
        config.oper_stack.append(3.1)
        ops.lt_oper()
        assert config.oper_stack == [True]

    def test_lt_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        config.oper_stack.append(5)
        with pytest.raises(TypeMismatchException):
            ops.lt_oper()

    def test_lt_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.lt_oper()

class TestAndOperator:
    def test_and_bool_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(True)
        ops.and_oper()
        assert config.oper_stack == [True]

    def test_and_bool_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(False)
        ops.and_oper()
        assert config.oper_stack == [False]

    def test_and_bool_false2(self):
        config.oper_stack.clear()
        config.oper_stack.append(False)
        config.oper_stack.append(False)
        ops.and_oper()
        assert config.oper_stack == [False]

    def test_and_int_bitwise(self):
        config.oper_stack.clear()
        config.oper_stack.append(6)  # 110
        config.oper_stack.append(3)  # 011
        ops.and_oper()
        assert config.oper_stack == [2]  # 010

    def test_and_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(3)
        with pytest.raises(TypeMismatchException):
            ops.and_oper()

    def test_and_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.and_oper()

class TestNotOperator:
    def test_not_bool_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        ops.not_oper()
        assert config.oper_stack == [False]

    def test_not_bool_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(False)
        ops.not_oper()
        assert config.oper_stack == [True]

    def test_not_int(self):
        config.oper_stack.clear()
        config.oper_stack.append(6)
        ops.not_oper()
        assert config.oper_stack == [~6]   # -7

    def test_not_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.not_oper()

    def test_not_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append("hello")
        with pytest.raises(TypeMismatchException):
            ops.not_oper()

class TestOrOperator:
    def test_or_bool_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(False)
        ops.or_oper()
        assert config.oper_stack == [True]

    def test_or_bool_false(self):
        config.oper_stack.clear()
        config.oper_stack.append(False)
        config.oper_stack.append(False)
        ops.or_oper()
        assert config.oper_stack == [False]

    def test_or_bool_true_true(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(True)
        ops.or_oper()
        assert config.oper_stack == [True]

    def test_or_int_bitwise(self):
        config.oper_stack.clear()
        config.oper_stack.append(6)   # 110
        config.oper_stack.append(3)   # 011
        ops.or_oper()
        assert config.oper_stack == [7]  # 111

    def test_or_type_error(self):
        config.oper_stack.clear()
        config.oper_stack.append(True)
        config.oper_stack.append(3)
        with pytest.raises(TypeMismatchException):
            ops.or_oper()

    def test_or_underflow(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            ops.or_oper()
