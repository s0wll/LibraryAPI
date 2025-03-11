import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.users import router as router_users
from src.api.authors import router as router_authors


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_authors)

if __name__ == "__main__":
    uvicorn.run("main:app", host="", reload=True)