from fastapi import FastAPI

from api.ask import router as ask_router
from api.contradict import router as contradict_router


app = FastAPI(
    title="RAG System API"
)


app.include_router(
    ask_router
)

app.include_router(
    contradict_router
)