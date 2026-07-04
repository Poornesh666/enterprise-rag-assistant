from pydantic import BaseModel


class LoginResponse(BaseModel):
    access_token: str
    token_type: str
    role: str


class TestResponse(BaseModel):
    message: str
    role: str


class ChatResponse(BaseModel):
    username: str
    role: str
    query: str
    response: str