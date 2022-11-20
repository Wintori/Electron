import uvicorn as uvicorn
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette import status

from back.app.endpoints.import_fiels import router as imp_router
from back.app.endpoints.data_sources_crud import router as ds_router
from back.app.endpoints.api_keys import router as api_keys_router
from back.app.endpoints.group import router as group_router
from back.app.endpoints.users import router as user_router
from back.app.models.db import database_accessor, Base
from config.settings import Settings


def bind_exceptions(app: FastAPI) -> None:
    @app.exception_handler(Exception)
    async def unhandled_error(_: Request, exc: Exception) -> JSONResponse:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={"message": str(exc)},
        )


def bind_events(app: FastAPI, db_settings: dict) -> None:
    @app.on_event("startup")
    async def set_engine():
        db = database_accessor
        await db.run()
        await db.init_db(Base)
        app.state.db = db
        app.tree = dict()

    @app.on_event("shutdown")
    async def close_engine():
        await app.state.db.stop()


def get_app() -> FastAPI:
    settings = Settings()
    app = FastAPI(
        title="FastReport API",
        description="Хранилище данных",
        docs_url="/swagger",
    )
    bind_events(app, settings.db_settings)
    bind_exceptions(app)
    app.include_router(imp_router, prefix="")
    app.include_router(ds_router, prefix="")
    app.include_router(api_keys_router, prefix="")
    app.include_router(group_router, prefix="")
    app.include_router(user_router, prefix="")

    # add_pagination(app)
    return app


app = get_app()
if __name__ == '__main__':
    uvicorn.run(
        app,
        host="127.0.0.1",
        port=8083,
    )
