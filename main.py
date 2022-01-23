# main.py
from typing import List

import uvicorn
from fastapi import FastAPI
# import couchbase.subdocument as SD


from Types import Song
from db import remove, upsert, get, create_params, query
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:80",
    "http://localhost:8080",
    "http://localhost:8081",
    "http://localhost:8082",

]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/helloWorld")
async def hello_world():
    return "HelloWorld"


@app.get("/hello/{name}")
async def hello(name):
    return f'Hello, {name}'


@app.put("/song/{id}")
async def put_song(id: str, song: Song):
    upsert('song', id, song.dict())


@app.delete("/song/{id}")
async def delete_song(id: str):
    return remove('song', id)


@app.get("/song/list")
async def list_songs() -> List[Song]:
    return query('SELECT j.* FROM joy j WHERE j.type == "song"').rows()


@app.get("/song/filter")
async def list_songs_filter(author: str = "") -> List[Song]:
    p = create_params()
    return query(f'SELECT * FROM joy WHERE type == "song" AND `doc`.`author` LIKE {p(f"%{author}%")}', p).rows()


# если поставить эту функцию выше, то она будет иметь приоитет над song/list или song/filter
@app.get("/song/{id}")
async def get_song(id: str):
    return get('song', id)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
