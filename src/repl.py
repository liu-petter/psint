from src.parsers import input_parser
from src import config
import logging

logging.basicConfig(level=logging.DEBUG)

def repl():
    while True:
        user_input = input("> ")
        tokens = user_input.split()
        for token in tokens:
            if token.lower() == "quit":
                return
            print(input_parser(token))
        logging.debug(f"oper_stack: {config.oper_stack}")