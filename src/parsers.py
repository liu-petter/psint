import logging
from src import config
from src.exceptions import ParseException, UnmatchedBracketException

logging.basicConfig(level=logging.ERROR)

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

def string_parser(input):
    logging.debug(f"ps_string_parser: input = \"{input}\"")
    
    if len(input) >= 2 and input.startswith("(") and input.endswith(")"):
        # removes ()
        return input[1:-1]
    else:
        raise ParseException("Could not parse input into a string")

# list of parsers
PARSERS = [
    boolean_parser,
    number_parser,
    name_constant_parser,
    code_block_parser,
    string_parser
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
# current_dict is the first dictionary that is looked into (used for lexical scoping)
def input_parser(input, current_dict):
    try: 
        result = constant_parser(input)
        config.oper_stack.append(result)
    except ParseException as p:
        logging.debug(p)
        try: 
            if config.STATIC_SCOPING:
                lookup_dict_static(input, current_dict)
            else:
                lookup_dict(input)
        except ParseException as e:
            # could not find constant in dictionaries
            logging.error(e)

# looks up in the dictionary stack for named constants
def lookup_dict(input):
    for current_dict in reversed(config.dict_stack):
        if input in current_dict:
            value = current_dict[input]
            if callable(value):                  
                # check if value is a function
                try:
                    if input in ["if", "ifelse", "for", "repeat"]:
                        # required to check if the function requires executing code blocks
                        value(input_parser)
                    else:
                        value()
                except Exception as e:
                    logging.error(e)
            elif isinstance(value, list):
                # parses through code blocks
                for item in value:
                    input_parser(item, current_dict)
            else:
                config.oper_stack.append(value)
            return
    raise ParseException(f"Could not find {input} in dictionary")

def lookup_dict_static(input, current_dict):
    while current_dict is not None:
        if input in current_dict:
            value = current_dict[input]
            if callable(value):
                try:
                    if input in config.exec_funcs:
                        # required to check if the function requires executing code blocks
                        value(input_parser)
                    else:
                        value()
                except Exception as e:
                    logging.error(e)
            elif isinstance(value, list):
                for item in value:
                    input_parser(item, current_dict)
            else:
                config.oper_stack.append(value)
            return
        # search in parent dict
        current_dict = current_dict.get_parent()
    raise ParseException(f"Could not find {input} in dictionaries (lexical)")

# tokenizes the input with spaces and handles code blocks
def tokenize_input(input):
    tokens = []        # final list of tokens
    current = []       # list of chars for current token
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

            while i < length:
                if input[i] == '}':
                    block.append('}')
                    i += 1
                    break
                else:
                    block.append(input[i])
                    i += 1
            else:
                raise UnmatchedBracketException("Unmatched '{' in input")
            
            tokens.append("".join(block))
            continue

        # start of string
        if char == '(':
            i += 1
            string_token = ['(']
            paren_count = 1  # for nested parentheses

            while i < length and paren_count > 0:
                c = input[i]
                string_token.append(c)
                if c == '(':
                    paren_count += 1
                elif c == ')':
                    paren_count -= 1
                i += 1

            if paren_count != 0:
                raise ParseException("Unmatched '(' in input")

            tokens.append("".join(string_token))
            continue

        # normal token
        current.append(char)
        i += 1

    if current:
        tokens.append("".join(current))

    return tokens
