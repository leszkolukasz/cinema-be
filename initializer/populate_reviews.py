import random
from essential_generators import DocumentGenerator

from src.database.setup import SessionLocal
from src.database.setup import engine
from src.models.base import Base
import src.models as models
from initializer.getters import get_random_movie, get_random_user

Base.metadata.create_all(bind=engine)

db = SessionLocal()
gen = DocumentGenerator()

i = 0
while i < 10000:
    try:
        review = models.Review(
            movie_id=get_random_movie(db).id,
            user_id=get_random_user(db).id,
            text=gen.paragraph(),
            score=random.randint(1, 10)
        )
        db.add(review)
        db.commit()
        i += 1
    except Exception as e:
        db.rollback()
