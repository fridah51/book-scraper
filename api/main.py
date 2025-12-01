from fastapi import FastAPI
from api.books import router as books_router
from api.changes import router as changes_router
from slowapi import Limiter
from slowapi.util import get_remote_address
from slowapi.middleware import SlowAPIMiddleware
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from scheduler.jobs import init_scheduler

load_dotenv()


# ---------- Initialize Scheduler on startup----------
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_scheduler()
    yield


app = FastAPI(title="Books Scraping API", lifespan=lifespan)

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_middleware(SlowAPIMiddleware)


app.include_router(books_router)
app.include_router(changes_router)


