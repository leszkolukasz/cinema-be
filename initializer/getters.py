from sqlalchemy.sql.expression import func

import src.models as models


def get_random_user(db):
    user = db.query(models.User).order_by(func.random()).first()
    return user


def get_random_cinema(db):
    cinema = db.query(models.Cinema).order_by(func.random()).first()
    return cinema


def get_random_movie(db):
    movie = db.query(models.Movie).order_by(func.random()).first()
    return movie


def get_random_room(db):
    room = db.query(models.Room).order_by(func.random()).first()
    return room


def get_random_screening(db):
    screening = db.query(models.Screening).order_by(func.random()).first()
    return screening

