from dataclasses import dataclass
from typing import List
from src.query import Query

@dataclass
class Level:
    """Represents a game level with law implementation challenge"""
    id: str
    title: str
    description: str
    background_story: str
    given_facts: str
    law_description: str
    queries: List[Query]
    hints: List[str] = None
    difficulty: int = 1
    solution: List[str] = None
    completed: bool = False