from pydantic import BaseModel

class ChatRequest(BaseModel):
    message: str


class ChatResponse(BaseModel):
    username: str
    role: str
    query: str
    response: str