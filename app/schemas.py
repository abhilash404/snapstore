from pydantic import BaseModel, ConfigDict
from typing import Optional

class CreateUserRequest(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_toekn: str
    token_type: str

class us(BaseModel):
    email: str
    password: str