import datetime
from pydantic import BaseModel

class Movie(BaseModel):
    id: int
    title: str
    director: str
    length: int
    poster_url: str
    summary: str
    release_date: datetime.date

    class Config:
        orm_mode = True
