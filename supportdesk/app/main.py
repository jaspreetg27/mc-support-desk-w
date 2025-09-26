from fastapi import FastAPI
from .routers.health import router as health_router

app = FastAPI(title="SupportDesk API")

@app.get("/")
def root():
    return {"ok": True}

app.include_router(health_router)
