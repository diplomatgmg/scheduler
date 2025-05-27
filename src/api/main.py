from fastapi import FastAPI
import uvicorn

from api.core.config import api_config
from api.endpoints import v1_router
from api.endpoints.schemas.root import RootResponse
from common.environment.config import env_config
from common.logging.config import log_config
from common.logging.setup import setup_module_logging
from common.sentry.setup import setup_sentry


app = FastAPI(
    title=f"{env_config.project_name} API",
    docs_url="/api/docs",
)

app.include_router(v1_router, prefix="/api/v1")


@app.get("/", summary="Корневой endpoint")
async def root() -> RootResponse:
    return RootResponse(docs=app.docs_url)


def main() -> None:
    setup_module_logging("api")
    setup_sentry()

    uvicorn.run(
        "api.main:app",
        host=str(api_config.host),
        port=api_config.port,
        log_config=None,
        log_level=log_config.level.lower(),
        reload=env_config.debug,
    )


if __name__ == "__main__":
    main()
