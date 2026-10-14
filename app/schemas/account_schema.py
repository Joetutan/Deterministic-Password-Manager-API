from pydantic import BaseModel


class AccountCreate(BaseModel):
    username:str
    system_name:str

class AccountResponse(BaseModel):
    system_name:str

