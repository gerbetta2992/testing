from fastapi import FastAPI
from routers import layer_router

app = FastAPI()

app.include_router(layer_router.router, prefix="/layers", tags=["layers"])
