from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import init_db
from app.api import auth, vault, emotional, beneficiaries, trigger


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield


app = FastAPI(title=settings.APP_NAME, version="2.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(vault.router)
app.include_router(emotional.router)
app.include_router(beneficiaries.router)
app.include_router(trigger.router)


@app.get("/")
async def root():
    return {"message": "DigitalLegacy API v2 - 数字遗产管家", "version": "2.0.0"}


@app.get("/health")
async def health():
    return {"status": "ok"}
