from pathlib import Path
from fastapi import FastAPI
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

try:
    from utils.decorators import utils
    from settings.config import config
    from database.database import db
    from app.lifespan import Lifespan
    from app.rate_limit import rate_limit
    from app.static import static_files
    from app.router_registry import ROUTERS
except ImportError as ie:
    exit(f'{ie} :: {Path(__file__).resolve()}')


@utils.exception
def init_app() -> FastAPI:
    lifespan: Lifespan = Lifespan(lifespans=[rate_limit, db.init])
    app: FastAPI = FastAPI(lifespan=lifespan)

    app.add_middleware(middleware_class=GZipMiddleware, minimum_size=1000)
    app.add_middleware(middleware_class=SessionMiddleware, secret_key=config.SESSION_KEY)
    app.add_middleware(middleware_class=CORSMiddleware, **config.CORS)
    app.mount(**static_files)

    for router in ROUTERS:
        app.include_router(router)

    return app
