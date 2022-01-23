from typing import Optional, List
from pydantic import BaseModel


class Song(BaseModel):
    name: str
    composer: Optional[str]
    author_text: Optional[str]
    links: List[str]
    seasons: List[str]
    choirs: List[str]
 # "name": "Памятник солдату",
 #    "composer": "В. Голиков",
 #    "author_text": null,
 #    "genry": "Русская современная",
 #    "links": [
 #      "D:\\Библиотека1\\Кандидатский\\Русская современная\\В. Голиков;Памятник солдату\\В. Голиков Памятник солдату 2 клавир.pdf",
 #      "D:\\Библиотека1\\Кандидатский\\Русская современная\\В. Голиков;Памятник солдату\\В. Голиков Памятник солдату клавир.pdf",
 #      "D:\\Библиотека1\\Кандидатский\\Русская современная\\В. Голиков;Памятник солдату\\В.Голиков Памятник солдату.pdf"
 #    ],
 #    "seasons": [
 #      "2020-2021"
 #    ],
 #    "choirs": [
 #      "Кандидатский"
 #    ]