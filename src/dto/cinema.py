import datetime
from pydantic import BaseModel

class Cinema(BaseModel):
    id: int
    name: str
    address: str
    admin_id: int

    class Config:
        orm_mode = True

class Screening(BaseModel):
    id: int
    room_name: str
    start_time: datetime.datetime

    def from_orm(other):
        return Screening(id=other.id, room_name=other.room.name, start_time=other.start_time)