import uvicorn
from fastapi import FastAPI

from contextlib import asynccontextmanager
from src.routers.package_controller import router as package_router
from src.database import create_db_and_tables

@asynccontextmanager
async def lifespan(_app: FastAPI):
    # Startup
    _app.include_router(package_router)
    create_db_and_tables()
    print("Database created.")
    yield
    # Clean up

app = FastAPI(lifespan=lifespan, docs_url="/")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
