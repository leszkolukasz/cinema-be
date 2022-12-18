import random
from essential_generators import DocumentGenerator

from src.database.setup import SessionLocal
from src.database.setup import engine
from src.models.base import Base
import src.models as models
from initializer.getters import get_random_cinema

Base.metadata.create_all(bind=engine)

db = SessionLocal()
gen = DocumentGenerator()

i = 0
while i < 10:
    try:
        room = models.Room(
            name=f"room-{random.randint(1, 1000000)}",
            width=random.randint(1, 10),
            length=random.randint(1, 10),
            cinema_id=get_random_cinema(db).id,
        )
        db.add(room)
        db.commit()
        i += 1
    except Exception as e:
        db.rollback()
