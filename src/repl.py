from src.parsers import input_parser, tokenize_input
from src import config
import logging

logging.basicConfig(level=logging.INFO)

def repl():
    while True:
        user_input = input("> ")
        tokens = tokenize_input(user_input)
        for token in tokens:
            if token.lower() == "quit":
                return
            result = input_parser(token, config.dict_stack[-1])
            if result is not None:
                print(result)
        logging.debug(f"oper_stack: {config.oper_stack}")