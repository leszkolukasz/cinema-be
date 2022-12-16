from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

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


@app.get("/movies", response_model=list[dto.Movie])
def get_movies(like: str = "", limit: int = 10, db: Session = Depends(get_db)):
    return get_movies_like(db, like, limit)
