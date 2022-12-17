from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT

from src.router import app
from src.database.utility import get_db
import src.dto as dto
from src.services import *


@app.get("/movies/{id}", response_model=dto.Movie)
def get_movies(id: int, db: Session = Depends(get_db)):
    try:
        movie = get_movies_by_id(db, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Movie not found")
    return movie


@app.get("/movies/{id}/score", response_model=float)
def get_movie_score(id: int, db: Session = Depends(get_db)):
    return get_movie_score_by_id(db, id)


@app.get("/movies", response_model=list[dto.Movie])
def get_movies(like: str = "", limit: int = 10, db: Session = Depends(get_db)):
    return get_movies_like(db, like, limit)


@app.post("/reviews")
def add_review(
    review: dto.Review,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    add_review_by_movie_id(db, Authorize.get_jwt_subject(), review.movie_id, review.score, review.text)

@app.get("/reviews/{movieId}", response_model=list[dto.Review])
def get_reviews(
    movieId: int,
    db: Session = Depends(get_db),
):
    return get_reviews_by_movie_id(db, movieId)

@app.get("/screenings/{movieId}/days", response_model=list[str])
def get_screening_days(
    movieId: int,
    db: Session = Depends(get_db),
):
    dates = get_screening_days_by_movie_id(db, movieId)
    return [date[0] for date in dates]

@app.get("/screenings/{movieId}/days/{day}/cinemas", response_model=list[dto.Cinema])
def get_screening_cinemas(
    movieId: int,
    day: str,
    db: Session = Depends(get_db),
):
    cinemas = get_screening_cinemas_by_movie_id_and_day(db, movieId, day)
    return cinemas

@app.get("/screenings/{movieId}/days/{day}/cinemas/{cinema_id}", response_model=list[dto.Screening])
def get_screenings_for_day_and_cinema_and_movie(
    movieId: int,
    day: str,
    cinema_id: int,
    db: Session = Depends(get_db),
):
    screenings = get_screening_by_cinema_id_and_movie_id_and_day(db, movieId, day, cinema_id)
    return [dto.Screening.from_orm(screening) for screening in screenings]


@app.get("/screenings/{screeningId}/free-seats", response_model=list[int])
def get_free_seats_for_screaning(
    screeningId: int,
    db: Session = Depends(get_db),
):
    seats = get_free_seats_for_screening_by_screening_id(db, screeningId)
    return seats