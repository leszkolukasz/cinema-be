from sqlalchemy import Column, ForeignKey, Integer, String, Date
from sqlalchemy.orm import relationship

from .base import Base
from .constraints import between, positive

class Movie(Base):
    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False)
    director = Column(String, nullable=False)
    length = Column(Integer, positive("length"), nullable=False)
    summary = Column(String)
    release_date = Column(Date, nullable=False)

    reviews = relationship("Review", back_populates="movie")
    screenings = relationship("Screening", back_populates="movie")

    def get_summary(self):
        return self.summary if self.summary.is_not(None) else ""

class Review(Base):
    __tablename__ = "reviews"

    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    text = Column(String)
    score = Column(Integer, between("score", 0, 10), nullable=False)

    user = relationship("User", back_populates="reviews")
    movie = relationship("Movie", back_populates="reviews")
    
    def get_text(self):
        return self.text if self.text.is_not(None) else ""