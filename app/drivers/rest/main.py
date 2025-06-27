from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def read_root() -> dict:
    return {"message": "Hello, FastAPI with Poetry"}


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}
