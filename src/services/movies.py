import datetime
from sqlalchemy.sql import func
from sqlalchemy import and_, cast, Date

import src.models as models


def get_movies_by_id(db, id):
    return db.query(models.Movie).filter(models.Movie.id == id).one()


def get_movie_score_by_id(db, movie_id):
    return round(
        db.query(func.avg(models.Review.score), models.Movie.id)
        .filter(models.Movie.id == movie_id)
        .join(models.Review)
        .group_by(models.Movie.id)
        .scalar(),
        2,
    )


def get_movies_like(db, like, limit):
    return (
        db.query(models.Movie)
        .filter(models.Movie.title.ilike(f"%{like}%"))
        .limit(limit)
        .all()
    )


def add_review_by_movie_id(db, user_id, movie_id, score, text):
    review = models.Review(movie_id=movie_id, user_id=user_id, score=score, text=text)
    db.add(review)
    db.commit()


def get_reviews_by_movie_id(db, movie_id):
    return (
        db.query(models.Review)
        .filter(models.Review.movie_id == movie_id)
        .order_by(models.Review.reviewed_on.desc())
        .all()
    )


def get_available_movies(db):
    now = datetime.datetime.utcnow()
    return (
        db.query(models.Movie)
        .distinct(models.Movie.id)
        .join(models.Screening)
        .filter(models.Screening.start_time >= now)
        .all()
    )


def get_screening_days_by_movie_id(db, movie_id):
    now = datetime.datetime.utcnow()
    return (
        db.query(func.DATE(models.Screening.start_time))
        .distinct()
        .filter(
            and_(
                models.Screening.movie_id == movie_id,
                models.Screening.start_time >= now,
            )
        )
        .order_by(models.Screening.start_time)
        .all()
    )


def get_screening_cinemas_by_movie_id_and_day(db, movie_id, day):
    date = max(datetime.datetime.utcnow(), datetime.datetime.strptime(day, "%Y-%m-%d"))

    return (
        db.query(models.Cinema)
        .distinct()
        .join(models.Room)
        .join(models.Screening)
        .filter(
            and_(
                models.Screening.movie_id == movie_id,
                func.DATE(models.Screening.start_time) == func.DATE(date),
            )
        )
        .all()
    )


def get_screening_by_cinema_id_and_movie_id_and_day(db, movie_id, day, cinema_id):
    date = max(datetime.datetime.utcnow(), datetime.datetime.strptime(day, "%Y-%m-%d"))
    return (
        db.query(models.Screening)
        .distinct()
        .filter(
            and_(
                models.Screening.movie_id == movie_id,
                func.DATE(models.Screening.start_time) == func.DATE(date),
            )
        )
        .join(models.Room)
        .filter(models.Room.cinema_id == cinema_id)
        .all()
    )


def get_screening_by_id(db, id):
    return db.query(models.Screening).filter(models.Screening.id == id).one()


def get_free_seats_for_screening_by_screening_id(db, screening_id):
    screening = get_screening_by_id(db, screening_id)
    taken_seats, free_seats = [], []

    for reservation in screening.reservations:
        taken_seats.append(reservation.seat)

    for i in range(screening.room.length * screening.room.width - 1):
        if i not in taken_seats:
            free_seats.append(i)

    return free_seats
