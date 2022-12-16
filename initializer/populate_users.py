from essential_generators import DocumentGenerator

from src.database.setup import SessionLocal
from src.database.setup import engine
import src.models as models
from src.models.base import Base
from src.services import *

Base.metadata.create_all(bind=engine)

db = SessionLocal()
gen = DocumentGenerator()

i = 0
while i < 10:
    try:
        create_user(db, f"{gen.name()}", f"password{i}")
        i += 1
    except Exception as e:
        db.rollback()