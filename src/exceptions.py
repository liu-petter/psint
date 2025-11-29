class ParseException(Exception):
    """An exception to record an error in the parsing"""
    def __init__(self, message):
        super().__init__(message)

class TypeMismatchException(Exception):
    """An exception to record a type mismatch in an operation"""
    def __init__(self, message):
        super().__init__(message)

class UnmatchedBracketException(Exception):
    """An exception to record an unmatched bracket in a code block"""
    def __init__(self, message):
        super().__init__(message)

class ZeroDivisionException(Exception):
    """An exception to catch division by zero error"""
    def __init__(self, message):
        super().__init__(message)

class IndexOutOfRangeException(Exception):
    """An exception that occurs when indexing out of range"""
    def __init__(self, message):
        super().__init__(message)