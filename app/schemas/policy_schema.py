from pydantic import BaseModel, ConfigDict


class AccountPolicy(BaseModel):
    
    length: int = 20
    lower: bool=True
    upper: bool=True
    digits: bool=True
    symbols: bool=False

    model_config = ConfigDict(from_attributes=True)