from fastapi import FastAPI
from apps.api.app.api.v1.auth import router as auth_router
from apps.api.app.core.exceptions import setup_exception_handlers

app = FastAPI(
    title="EKCP API",
    description="Enterprise Knowledge & Continuity Platform API Service",
    version="0.1.0",
)

setup_exception_handlers(app)

# Register API v1 Auth Router under /api/v1
app.include_router(auth_router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {"status": "ok", "service": "ekcp-api"}
