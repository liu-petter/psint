import pytest
from exceptions import ParseException
from parsers import boolean_parser, number_parser

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

class TestNumberParseing:
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