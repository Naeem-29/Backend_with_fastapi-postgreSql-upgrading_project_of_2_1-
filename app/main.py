from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from .routers import galleries

app = FastAPI()

app.include_router(galleries.router)

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)