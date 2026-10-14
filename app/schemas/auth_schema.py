from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id:int
    username:str
    email: EmailStr
    model_config = {"from_attributes": True}

class ResponseToken(BaseModel):
    access_token: str
    token_type: str