from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str
