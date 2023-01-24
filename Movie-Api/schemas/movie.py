from pydantic import BaseModel, Field
from typing import Optional

class Movie(BaseModel):
    id: Optional[int] = None
    title: str = Field(max_length = 15, min_length = 5)
    overview : str
    year: int = Field(le = 2022, ge = 1900)
    rating: float
    category: str

    class Config:
        schema_extra = {
            "example": {                
                "title" : "Pelicula",
                "overview" : "Descripcion",
                "year" : 2022,
                "rating": 5,
                "category": "Mi categoria" 
            }
        }