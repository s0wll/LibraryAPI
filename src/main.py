import sys
from pathlib import Path

from fastapi import FastAPI
import uvicorn

sys.path.append(str(Path(__file__).parent.parent))

from src.api.auth import router as router_auth
from src.api.users import router as router_users
from src.api.authors import router as router_authors
from src.api.books import router as router_books
from src.api.borrows import router as router_borrows


app = FastAPI()

app.include_router(router_auth)
app.include_router(router_users)
app.include_router(router_authors)
app.include_router(router_books)
app.include_router(router_borrows)

if __name__ == "__main__":
    uvicorn.run("main:app", host="", reload=True)