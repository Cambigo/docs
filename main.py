from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

app = FastAPI()

app.mount("/", StaticFiles(directory="./site", html=True), name="notebook")

# mkdocs build
# pip install "fastapi[standard]"
# fastapi dev main.py