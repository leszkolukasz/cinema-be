from sqlalchemy import Column, ForeignKey, Integer, String, Date, PrimaryKeyConstraint, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from .base import Base
from .constraints import between, positive


class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    length = Column(Integer, positive("length"), nullable=False)
    poster_url = Column(String)
    summary = Column(String)
    release_date = Column(Date, nullable=False)

    reviews = relationship("Review", back_populates="movie")
    screenings = relationship("Screening", back_populates="movie")

    def get_summary(self):
        return self.summary if self.summary.is_not(None) else ""


class Review(Base):
    __tablename__ = "reviews"
    __table_args__ = (PrimaryKeyConstraint("movie_id", "user_id", name="review_pk"),)

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    text = Column(String)
    score = Column(Integer, between("score", 0, 10), nullable=False)
    reviewed_on = Column(DateTime, nullable=False, server_default=func.now())

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")

    def get_text(self):
        return self.text if self.text.is_not(None) else ""
