from fastapi import FastAPI

app = FastAPI()


@app.get("/api/hello-world")
def hell_world():
    return {"response": "hell_world"}
