from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import auth, users

app = FastAPI()

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(auth.router)
app.include_router(users.router)
