import uuid

from pydantic import BaseModel


class MessageRequest(BaseModel):
    conversation_id: uuid.UUID
    content: str
