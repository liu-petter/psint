import logging
from src import config
from src.exceptions import ParseException, UnmatchedBracketException

logging.basicConfig(level=logging.INFO)

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

# handles user defined variables
def name_constant_parser(input):
    logging.debug(f"name_constant_parser: input = \"{input}\"")
    if input.startswith("/"):
        return input
    else:
        raise ParseException("Can't parse input into a name constant")

# handles code blocks   
def code_block_parser(input):
    logging.debug(f"code_block_parser: input = \"{input}\"")
    if len(input) >= 2 and input.startswith("{") and input.endswith("}"):
        # needs a minimum of open bracket and close bracket
        return input[1:-1].strip().split()      # removes first and last bracket and wrapping whitespace
    else:
        raise ParseException("Could not parse input into a code block")

# list of parsers
PARSERS = [
    boolean_parser,
    number_parser,
    name_constant_parser,
    code_block_parser
]

# parses a constant by finding a parser that matches
def constant_parser(input):
    for parser in PARSERS:
        try:
            return parser(input)
        except ParseException as e:
            logging.debug(e)
            continue
    raise ParseException(f"Could not parse {input} as boolean or number")

# parses a single user inputed token
def input_parser(input):
    try: 
        result = constant_parser(input)
        config.oper_stack.append(result)
    except ParseException as p:
        logging.debug(p)
        lookup_dict(input)

# looks up in the dictionary stack for named constants
def lookup_dict(input):
    for current_dict in reversed(config.dict_stack):
        if input in current_dict:
            value = current_dict[input]
            if callable(value):
                # check if value is a function
                try:
                    value()
                except Exception as e:
                    logging.debug(e)
            elif isinstance(value, list):
                # parses through code blocks
                for item in value:
                    input_parser(item)
            else:
                config.oper_stack.append(value)
            return
    raise ParseException(f"Could not find {input} in dictionary")

# tokenizes the input with spaces and handles code blocks
def tokenize_input(input):
    tokens = []             # final list of tokens
    current = []            # list of chars for current token we are looking at
    i = 0
    length = len(input)

    while i < length:
        char = input[i]

        # skip whitespace
        if char.isspace():
            if current:
                # reached end of token, join to form single string and reset current
                tokens.append("".join(current))
                current = []
            i += 1
            continue

        # start of a code block
        if char == '{':
            i += 1
            block = ['{']

            # append until }
            while i < length and input[i] != '}':
                block.append(input[i])
                i += 1

            if i >= length:
                raise UnmatchedBracketException("Unmatched '{' in input")

            # append closing }
            block.append('}')
            i += 1

            tokens.append("".join(block))
            continue

        # normal token
        current.append(char)
        i += 1

    # final token
    if current:
        tokens.append("".join(current))

    return tokens
