from dataclasses import dataclass
from typing import List

@dataclass
class Query:
    """Represents a Prolog query with expected results"""
    query: str
    expected: List[str]
    description: str = ""