import random
from faker import Faker

from src.database.setup import SessionLocal
from src.database.setup import engine
from src.models.base import Base
import src.models as models
from initializer.getters import get_random_user

Base.metadata.create_all(bind=engine)

db = SessionLocal()
fake = Faker()

i = 0
while i < 10:
    try:
        cinema = models.Cinema(
            name=f"cinema-{random.randint(1, 1000000)}",
            address=fake.address(),
            admin_id=get_random_user(db).id,
        )
        db.add(cinema)
        db.commit()
        i += 1
    except Exception as e:
        db.rollback()