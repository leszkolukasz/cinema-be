from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    # reviews = relationship("Review", back_populates="user")
    # reservations = relationship("Reservation", back_populates="user")
    # managed_cinemas = relationship("Cinema", back_populates="administrator")