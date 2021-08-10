from typing import Optional
from pydantic import BaseModel


class Song(BaseModel):
    name: str
    author: str
    tags: list[str]
