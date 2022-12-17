import random
from faker import Faker

from src.database.setup import SessionLocal
from src.database.setup import engine
from src.models.base import Base
import src.models as models
from initializer.getters import get_random_cinema, get_random_movie, get_random_room

Base.metadata.create_all(bind=engine)

db = SessionLocal()
fake = Faker()

i = 0
while i < 100:
    try:
        cinema = get_random_cinema(db)
        if len(cinema.rooms) == 0:
            continue

        room = random.choice(cinema.rooms)
        screening = models.Screening(
            movie_id=get_random_movie(db).id,
            room_id=room.id,
            start_time=fake.future_datetime()
        )
        db.add(screening)
        db.commit()
        i += 1
    except Exception as e:
        db.rollback()
