from pydantic import BaseModel

class TShirtRequest(BaseModel):
    name: str
    size: str
    color: str

