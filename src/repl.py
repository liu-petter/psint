from src.parsers import input_parser
from src import config
import logging


def repl():
    while True:
        user_input = input("> ")
        tokens = user_input.split()
        for token in tokens:
            if token.lower() == "quit":
                return
            result = input_parser(token)
            if result is not None:
                print(result)
        logging.debug(f"oper_stack: {config.oper_stack}")