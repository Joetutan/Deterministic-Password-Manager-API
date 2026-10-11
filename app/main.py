from fastapi import FastAPI

from app.api.auth_routes import router as auth_router
from app.api.vault_routes import router as vault_router

app = FastAPI(title="Deterministic Password Manager", version="0.1.0")

app.include_router(auth_router)
app.include_router(vault_router)