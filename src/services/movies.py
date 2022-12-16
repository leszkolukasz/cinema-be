import src.models as models


def get_movies_by_id(db, id):
    return db.query(models.Movie).filter(models.Movie.id == id).one()

def get_movie_score_by_id(db, id):
    movie = get_movies_by_id(db, id)
    score = 0
    for review in movie.reviews:
        score += review.score
    if len(movie.reviews):
        return round(score / len(movie.reviews), 2)


def get_movies_like(db, like, limit):
    return (
        db.query(models.Movie)
        .filter(models.Movie.title.ilike(f"%{like}%"))
        .limit(limit)
        .all()
    )
