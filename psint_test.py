import pytest
from src.exceptions import ParseException, TypeMismatchException
from src.parsers import boolean_parser, number_parser
from src.operations import add_oper, sub_oper, mul_oper, pop_oper
from src import config

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

class TestAddOperator:
    """Tests for sub operator"""
    def test_add_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        add_oper()
        assert config.oper_stack == [3]
    
    def test_add_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            add_oper()
    
    def test_add_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            add_oper()
    
    def test_add_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        add_oper()
        assert config.oper_stack == [1,5]
    
    def test_add_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        add_oper()
        assert config.oper_stack == [2]
    
    def test_add_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            add_oper()

class TestSubOperator:
    """Tests for sub operator"""
    def test_sub_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([2,1])
        sub_oper()
        assert config.oper_stack == [1]
    
    def test_sub_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            sub_oper()
    
    def test_sub_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            sub_oper()
    
    def test_sub_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        sub_oper()
        assert config.oper_stack == [1,-1]
    
    def test_sub_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        sub_oper()
        assert config.oper_stack == [-4]
    
    def test_sub_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            sub_oper()

class TestMulOperator:
    """Tests for mul operator"""
    def test_mul_two_nums(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        mul_oper()
        assert config.oper_stack == [2]
    
    def test_mul_one_num(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            mul_oper()
    
    def test_mul_empty_stack(self):
        config.oper_stack.clear()
        with pytest.raises(TypeMismatchException):
            mul_oper()
    
    def test_mul_two_nums_non_empty_stack(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2,3])
        mul_oper()
        assert config.oper_stack == [1,6]
    
    def test_mul_pos_and_neg(self):
        config.oper_stack.clear()
        config.oper_stack.extend([-1,3])
        mul_oper()
        assert config.oper_stack == [-3]
    
    def test_mul_int_and_bool(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1, True])
        with pytest.raises(TypeMismatchException):
            mul_oper()