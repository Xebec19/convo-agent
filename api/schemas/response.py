from pydantic import BaseModel


class APIResponse(BaseModel):
    """
    APIResponse defines schema for
    response
    """

    status: bool
    data: str | int
    message: str
