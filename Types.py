from typing import Optional
from pydantic import BaseModel

def doc(type: str, id: str, doc: object):
    return {id: id, type: type, doc: doc}
# class Doc:
#     def __init__(self, id, type, doc) -> None:
#         self.id = id
#         self.type = type
#         self.doc = doc
#
#     id: str
#     type: str
#     doc: object


class Song(BaseModel):
    name: str
    author: str
    tags: list[str]
