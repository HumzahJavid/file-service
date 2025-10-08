from __future__ import annotations

import uvicorn
from fastapi import FastAPI

from file_service.file_service import ROUTER

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


app.include_router(ROUTER)

# uv run fastapi run --port 8003
if __name__ == "__main__":
    uvicorn.run("main:app", port=8000, reload=True, access_log=False)
