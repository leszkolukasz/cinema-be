import random

from src.database.setup import SessionLocal
from src.database.setup import engine
from src.models.base import Base
import src.models as models
from initializer.getters import get_random_user, get_random_screening

Base.metadata.create_all(bind=engine)

db = SessionLocal()

i = 0
while i < 10:
    try:
        user = get_random_user(db)
        screening = get_random_screening(db)

        reservation = models.Reservation(
            user_id = user.id,
            screening_id = screening.id,
            seat=random.randint(0, screening.room.width*screening.room.length-1)
        )
        db.add(reservation)
        db.commit()
        i += 1
    except Exception as e:
        db.rollback()
