import sys
from pathlib import Path

import uvicorn
from fastapi import FastAPI

sys.path.append(str(Path(__file__).parent.parent))

from src.routers.clients import router as clients_router
from src.routers.subscriptions import router as subscriptions_router

app = FastAPI()

app.include_router(clients_router)
app.include_router(subscriptions_router)


if __name__=="__main__":
    uvicorn.run("main:app", reload=True)