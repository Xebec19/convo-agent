from fastapi.middleware.cors import CORSMiddleware
from routes import assets, auth, users
from server import app
from middlewares.authentication import get_current_user

origins = ["http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
)

app.include_router(auth.router)

app.add_middleware(get_current_user)
app.include_router(users.router)
app.include_router(assets.router)
