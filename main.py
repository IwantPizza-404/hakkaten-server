from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from app.api.v1 import users, posts, auth
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router, prefix="/api/v1")
app.include_router(posts.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1/auth")
app.mount("/static", StaticFiles(directory="uploads"), name="static")
