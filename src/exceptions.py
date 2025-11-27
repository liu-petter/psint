class ParseException(Exception):
    """An exception to record an error in the parsing"""
    def __init__(self, message):
        super().__init__(message)

class TypeMismatchException(Exception):
    """An exception to record a type mismatch in an operation"""
    def __init__(self, message):
        super().__init__(message)