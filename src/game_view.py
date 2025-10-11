from enum import Enum

class GameView(Enum):
    """Different game views/screens"""
    INTRODUCTION = "introduction"
    TASK_OVERVIEW = "task_overview"
    TASK_WORKSPACE = "task_workspace"
    FAILURE = "failure"
    SUCCESS = "success"
