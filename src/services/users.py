import src.models as models
from src.services import *

def create_user(db, login, password):
    hashed_password = get_password_hash(password)
    db_user = models.User(login=login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_user_by_login(db, login):
    return db.query(models.User).filter(models.User.login == login).one()
