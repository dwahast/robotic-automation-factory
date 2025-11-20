import uvicorn
from fastapi import FastAPI

from src.routers.package_controller import router as package_router

app = FastAPI(docs_url="/")
app.include_router(package_router)


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
