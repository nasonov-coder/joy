# main.py

import uvicorn
from fastapi import FastAPI
import jsonpickle
# import couchbase.subdocument as SD


from Types import Song, doc
from db import cluster, collection

app = FastAPI()


@app.get("/helloWorld")
async def read_root():
    return "HelloWorld"


@app.get("/hello/{name}")
async def read_root(name):
    return f'Hello, {name}'


@app.get("/song/list")
async def list_songs() -> list[Song]:
    return cluster.query('SELECT * FROM joy where type == "song"').rows()


@app.put("/song/{id}")
async def put_song(id: str, song: Song):
    collection.upsert(f'song@{id}', {'id': id, 'type': "song", 'doc': song.dict()})


@app.delete("/song/{id}")
async def put_song(id: str):
    return collection.remove(f'song@{id}')


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
