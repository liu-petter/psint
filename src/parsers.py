import logging
from src.exceptions import ParseException

logging.basicConfig(level=logging.DEBUG)

def boolean_parser(input):
    logging.debug(f"boolean_parser: input = \"{input}\"")
    if input == "true":
        return True
    elif input == "false":
        return False
    else:
        raise ParseException("Failed to parse boolean")
    
def number_parser(input):
    logging.debug(f"number_parser: input = \"{input}\"")
    try:
        float_val = float(input)
        if float_val.is_integer():
            return int(float_val)
        else:
            return float_val
    except ValueError:
        raise ParseException("Failed to parse number")    

PARSERS = [
    boolean_parser,
    number_parser
]

def constant_parser(input):
    for parser in PARSERS:
        try:
            return parser(input)
        except ParseException as e:
            logging.debug(e)
            continue
    raise ParseException(f"Could not parse {input} as boolean or number")