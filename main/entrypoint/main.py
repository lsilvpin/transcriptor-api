import sys, os

sys.path.insert(0, os.path.abspath("."))
from fastapi import FastAPI
from main.library.utils.core.settings_helper import load_environment, get
import uvicorn
from main.library.di_container import Container
from main.entrypoint.controllers.main_controller import router as main_controller_router
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi

load_environment(get("environment"))
app = FastAPI(
    title="transcriptor-api",
    version="1.0.0",
    description="API for transcribing audio files",
)
container = Container()
app.container = container
app.include_router(main_controller_router)


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=app.title,
        version=app.version,
        description=app.description,
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
