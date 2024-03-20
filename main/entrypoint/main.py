import sys, os
sys.path.insert(0, os.path.abspath("."))
from fastapi import FastAPI
from main.library.utils.core.settings_helper import load_environment, get
import uvicorn
from main.library.di_container import Container
from main.entrypoint.controllers.main_controller import router as main_controller_router

load_environment(get("environment"))
container = Container()
app = FastAPI()
app.container = container
app.include_router(main_controller_router)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
