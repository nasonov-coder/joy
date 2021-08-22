from typing import Optional, List
from pydantic import BaseModel


class Song(BaseModel):
    name: str
    author: str
    tags: List[str]
