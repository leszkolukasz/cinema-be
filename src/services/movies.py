from sqlalchemy.sql import func

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
