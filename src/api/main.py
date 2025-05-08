from fastapi import FastAPI

from api.endpoints import v1_router
from common.environment.config import env_config


app = FastAPI(
    title=f"{env_config.project_name} API",
    docs_url="/api/docs",
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": f"Welcome to {env_config.project_name}"}
