class ErrorDSL(Exception):
    """Error base del DSL."""


class ErrorLexico(ErrorDSL):
    pass


class ErrorSintactico(ErrorDSL):
    pass


class ErrorDeTipos(ErrorDSL):
    pass
