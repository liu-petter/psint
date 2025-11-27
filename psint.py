from src.parsers import constant_parser

def repl():
    while True:
        user_input = input("> ")
        tokens = user_input.split()
        for token in tokens:
            if token == ":q":
                return
            print(constant_parser(token))


if __name__ == "__main__":
    repl()