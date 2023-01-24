from pydantic import BaseModel, Field

class User(BaseModel):
    email :str = Field(max_length = 15, min_length = 5)
    password :str

    class Config:
        schema_extra = {
            "example": {                
                "email" : "email",
                "password" : "pass"
            }
        }