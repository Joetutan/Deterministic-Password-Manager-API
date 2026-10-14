from pydantic import BaseModel

class PassCreate(BaseModel):
    ...

class PassResponse(BaseModel):
    password: str