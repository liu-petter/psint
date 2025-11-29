import pytest
from src.exceptions import ParseException, TypeMismatchException, UnmatchedBracketException, ZeroDivisionException
from src.parsers import boolean_parser, number_parser, code_block_parser, tokenize_input
import src.operations as ops
from src import config
from src.config import init_config

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