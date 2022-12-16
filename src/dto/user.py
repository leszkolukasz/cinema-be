import datetime
from pydantic import BaseModel


class User(BaseModel):
    login: str
    password: str


class Reservation(BaseModel):
    id: int
    movie_id: int
    movie_title: str
    movie_poster_url: str
    room_name: str
    start_time: datetime.datetime
    seat: int

    def from_orm(other):
        return Reservation(
            id=other.id,
            movie_id=other.screening.movie_id,
            movie_title=other.screening.movie.title,
            movie_poster_url=other.screening.movie.poster_url,
            room_name=other.screening.room.name,
            start_time=other.screening.start_time,
            seat=other.seat,
        )
