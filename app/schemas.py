from pydantic import BaseModel, ConfigDict
from typing import Optional

class Blog(BaseModel):
    title: str
    body: str

class ShowBlog(BaseModel):
    body: str     
    class config(BaseModel):
        model_config = ConfigDict(from_attributes=True)