# main.py
import os
from shutil import rmtree
from typing import List

import uvicorn
from fastapi import FastAPI, UploadFile, File
# import couchbase.subdocument as SD
from fastapi.encoders import jsonable_encoder

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
    remove('song', id)
    rmtree((os.getcwd()+f"/files/{id}/"))


@app.get("/song/list")
async def list_songs() -> List[Song]:
    return query('SELECT j.* FROM joy j WHERE j.type == "song"').rows()


@app.get("/song/search")
async def song_search(search: str = "") -> List[Song]:
    p = create_params()
    return query(f"""
            SELECT (
                SELECT *
                FROM joy
                WHERE ANY c IN doc.choirs SATISFIES LOWER(c) LIKE LOWER({p(f"%{search}%")}) END ) AS choirs,
            (
                SELECT *
                FROM joy
                WHERE LOWER(doc.author_text) LIKE LOWER({p(f"%{search}%")} )) AS author_text,
            (
                SELECT *
                FROM joy
                WHERE LOWER(doc.omposer) LIKE LOWER({p(f"%{search}%")} )) AS composer,
            (
                SELECT *
                FROM joy
                WHERE LOWER(doc.genry) LIKE LOWER({p(f"%{search}%")} )) AS genry,
            (
                SELECT *
                FROM joy
                WHERE LOWER(doc.name) LIKE LOWER({p(f"%{search}%")} )) AS name,
            (
                SELECT *
                FROM joy
                WHERE ANY c IN doc.seasons SATISFIES LOWER(c) LIKE LOWER({p(f"%{search}%")}) END ) AS seasons
        """, p).rows()


# если поставить эту функцию выше, то она будет иметь приоитет над song/list или song/filter
@app.get("/song/{id}")
async def get_song(id: str):
    return get('song', id)

@app.post("/file/{song_id}")
async def add_file(song_id: str, files: UploadFile = File(...)):
    get('song', song_id)
    print(files.file)
    # print('../'+os.path.isdir(os.getcwd()+"images"),"*************")
    try:
        os.mkdir("files")
        print(os.getcwd())
    except Exception as e:
        print(e)
    try:
        os.mkdir(f"files/{song_id}")
    except Exception as h:
        print(h)
    filename = files.filename.replace(" ", "-")
    file_name = os.getcwd()+f"/files/{song_id}/" + filename
    with open(file_name,'wb+') as f:
        f.write(files.file.read())
        f.close()
    p = create_params()
    q = f"""
        UPDATE `joy`
        SET doc.links = ARRAY_APPEND(doc.links, {p(filename)})
        WHERE type = "song" and
        id = {p(song_id)} 
    """
    print(q)
    print(p.dic)
    # return!!!!!!!!!!!
    return query(q, p)


@app.delete("/file/{song_id}/{file_id}")
async def delete_file(file_id: str, song_id: str):
    p = create_params()
    q = f"""
            UPDATE `joy`
            SET doc.links = ARRAY_REMOVE(doc.links, {p(file_id)})
            WHERE type = "song" and
            id = {p(song_id)} 
        """
    print(q)
    print(p.dic)
    # return!!!!!!!!!!!
    query(q, p).rows()
    os.remove(os.getcwd()+f"/files/{song_id}/{file_id}")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=80)
