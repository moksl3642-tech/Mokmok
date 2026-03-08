from fastapi import FastAPI

from app.api.v1.routers.game import router as game_router

app = FastAPI(title="Mokmok Backend")
app.include_router(game_router, prefix="/api/v1")
