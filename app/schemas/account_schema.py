from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AccountCreate(BaseModel):
    username:str
    system_name:str

class AccountResponse(BaseModel):
    account_alias: str
    system_name: str
    #last_rotated: datetime
    #version: int = 1
    model_config = ConfigDict(from_attributes=True)

