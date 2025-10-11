from enum import Enum

class GameResult(Enum):
    SUCCESS = "success"
    SYNTAX_ERROR = "syntax_error"
    WRONG_RESULTS = "wrong_results"
    PROLOG_ERROR = "prolog_error"
