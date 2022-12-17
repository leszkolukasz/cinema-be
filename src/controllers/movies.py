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
    try:
        score = get_movie_score_by_id(db, id)
    except Exception as e:
        raise HTTPException(status_code=404, detail="Movie not found")
    return score


@app.get("/movies", response_model=list[dto.Movie])
def get_movies(like: str = "", limit: int = 10, db: Session = Depends(get_db)):
    try:
        movies = get_movies_like(db, like, limit)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Database error")
    return movies


@app.post("/reviews")
def add_review(
    review: dto.Review,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        add_review_by_movie_id(
            db, Authorize.get_jwt_subject(), review.movie_id, review.score, review.text
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")


@app.get("/reviews/{movie_id}", response_model=list[dto.Review])
def get_reviews(
    movie_id: int,
    db: Session = Depends(get_db),
):
    try:
        reviews = get_reviews_by_movie_id(db, movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
    return reviews

@app.get("/screenings/movies", response_model=list[dto.Movie])
def get_screening_movies(
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        movies = get_available_movies(db)
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Server error")
    return movies

@app.get("/screenings/movies/{movie_id}/days", response_model=list[str])
def get_screening_days(
    movie_id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        dates = get_screening_days_by_movie_id(db, movie_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
    return [date[0] for date in dates]


@app.get("/screenings/movies/{movie_id}/days/{day}/cinemas", response_model=list[dto.Cinema])
def get_screening_cinemas(
    movie_id: int,
    day: str,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        cinemas = get_screening_cinemas_by_movie_id_and_day(db, movie_id, day)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
    return cinemas


@app.get(
    "/screenings/movies/{movie_id}/days/{day}/cinemas/{cinema_id}",
    response_model=list[dto.Screening],
)
def get_screenings_for_day_and_cinema_and_movie(
    movie_id: int,
    day: str,
    cinema_id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        screenings = get_screening_by_cinema_id_and_movie_id_and_day(
            db, movie_id, day, cinema_id
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
    return [dto.Screening.from_orm(screening) for screening in screenings]


@app.get("/screenings/{screening_id}/free-seats", response_model=list[int])
def get_free_seats_for_screening(
    screening_id: int,
    Authorize: AuthJWT = Depends(),
    db: Session = Depends(get_db),
):
    Authorize.jwt_required()
    try:
        seats = get_free_seats_for_screening_by_screening_id(db, screening_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Server error")
    return seats
