import src.models as models


def get_movies_by_id(db, id):
    return db.query(models.Movie).filter(models.Movie.id == id).one()


def get_movies_like(db, like, limit):
    return (
        db.query(models.Movie)
        .filter(models.Movie.title.ilike(f"%{like}%"))
        .limit(limit)
        .all()
    )
