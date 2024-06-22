from pydantic import BaseModel

class TokenResponse(BaseModel):
    access_token:str
    token_type: str= "Bearer"
    refresh_token:str
    expires_in:int

    