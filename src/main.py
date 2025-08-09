from fastapi import FastAPI, status, HTTPException
from pydantic import BaseModel
import uvicorn


app = FastAPI()


class User(BaseModel):
    username: str
    role: str


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)