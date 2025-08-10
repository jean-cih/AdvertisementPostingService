from fastapi import FastAPI, status, HTTPException
from api.endpoints import auth, adverts, admin
import asyncio
from database import engine
from src.models.models import Base
import uvicorn


app = FastAPI()

app.include_router(auth.router)
app.include_router(adverts.router)
app.include_router(admin.router)


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup():
    await init_db()


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)