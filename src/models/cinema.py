from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, UniqueConstraint
from sqlalchemy.orm import relationship

from .base import Base
from .constraints import positive


class Cinema(Base):
    __tablename__ = "cinemas"
    __table_args__ = (UniqueConstraint("name", "address", name="name_address_unique"),)

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    address = Column(String, nullable=False)
    admin_id = Column(Integer, ForeignKey("users.id"))

    admin = relationship("User", back_populates="managed_cinemas")
    rooms = relationship("Room", back_populates="cinema")


class Room(Base):
    __tablename__ = "rooms"
    __table_args__ = (
        UniqueConstraint("cinema_id", "name", name="cinema_id_name_unique"),
    )

    id = Column(Integer, primary_key=True)
    cinema_id = Column(Integer, ForeignKey("cinemas.id"), nullable=False)
    name = Column(String, nullable=False)
    width = Column(Integer, positive("width"), nullable=False)
    length = Column(Integer, positive("length"), nullable=False)

    cinema = relationship("Cinema", back_populates="rooms")
    screenings = relationship("Screening", back_populates="room")


class Screening(Base):
    __tablename__ = "screenings"

    id = Column(Integer, primary_key=True)
    movie_id = Column(Integer, ForeignKey("movies.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    start_time = Column(
        DateTime, nullable=False
    )

    movie = relationship("Movie", back_populates="screenings")
    room = relationship("Room", back_populates="screenings")
    reservations = relationship("Reservation", back_populates="screening")
