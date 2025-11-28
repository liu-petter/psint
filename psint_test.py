import pytest
from src.exceptions import ParseException, TypeMismatchException, UnmatchedBracketException
from src.parsers import boolean_parser, number_parser, code_block_parser, tokenize_input
from src.operations import add_oper, sub_oper, mul_oper, pop_oper, def_oper
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

class TestPopOperator:
    """Tests the pop and = operators"""
    def test_pop_single_element(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        pop_oper()
        assert len(config.oper_stack) == 0
    
    def test_pop_two_elements(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        pop_oper()
        assert len(config.oper_stack) == 1

    def test_pop_on_empty(self):
        config.oper_stack.clear()
        config.oper_stack.extend([])
        with pytest.raises(TypeMismatchException):
            pop_oper()

class TestDefOperator:
    """Tests the def operator"""
    def test_def_on_empty(self):
        config.oper_stack.clear()
        config.oper_stack.extend([])
        with pytest.raises(TypeMismatchException):
            def_oper()
        
    def test_def_on_single(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1])
        with pytest.raises(TypeMismatchException):
            def_oper()
    
    def test_def_on_non_named_constant_as_key(self):
        config.oper_stack.clear()
        config.oper_stack.extend([1,2])
        with pytest.raises(TypeMismatchException):
            def_oper()

    def test_def_on_named_constant_as_key(self):
        init_config()
        config.oper_stack.clear()
        config.oper_stack.extend(['/x', 2])
        def_oper()
        assert config.dict_stack[-1]['x'] == 2
    
    def test_def_on_constant_as_key(self):
        config.oper_stack.clear()
        config.oper_stack.extend([2, "/x"])
        with pytest.raises(TypeMismatchException):
            def_oper()