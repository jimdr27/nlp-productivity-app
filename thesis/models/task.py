from dataclasses import dataclass
from typing import Optional

@dataclass
class Task:
    id: int
    title: str
    due_date: Optional[str] = None
    status: str = "pending"
    