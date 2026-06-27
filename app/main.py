from fastapi import FastAPI
from pathlib import Path
from fastapi.staticfiles import StaticFiles
from .routers import galleries,auth,comments


app = FastAPI()

app.include_router(galleries.router)
app.include_router(auth.router)
app.include_router(comments.router)

BASE_DIR = Path(__file__).resolve().parent


app.mount(
    "/static",
    StaticFiles(directory=BASE_DIR /"static"),
    name="static"
)

@app.get("/")
def root():
    return {"status": "ok"}