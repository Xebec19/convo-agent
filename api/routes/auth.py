from fastapi import APIRouter, Depends, status, Response, HTTPException
from sqlalchemy import select, func
from sqlalchemy.orm import Session

from api.database import get_db
from api.models.user_model import User
from api.schemas.auth import SignInRequest, SignUpRequest

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup")
async def signup(request: SignUpRequest, db: Session = Depends(get_db), status_code=201, response: Response):
    # get name, email, phone num and password
    # lowercase email and check if it dont have a duplicate in db
    # validate name and phonenum as well
    # encrypt password and store it in db

    query = select(func.count()).select_from(User).where( func.lower(User.name) ==  request.email.lower())

    count = db.scalar(query)

    if count > 0:
        raise HTTPException(
            status_code=401,
            detail="User is already present"
        )

    

    


@router.get("/signin")
async def signin(request: SignInRequest):
    pass
