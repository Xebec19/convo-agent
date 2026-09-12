from pydantic import BaseModel, EmailStr, Field


class SignInRequest(BaseModel):
    email: EmailStr
    password: str


class SignUpRequest(BaseModel):
    name: str
    phoneNum: str = Field(min_length=10, max_length=15, pattern=r"^\+?[1-9]\d{9,14}$")
    email: EmailStr
    password: str


class SigninResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    image: str | None = None
