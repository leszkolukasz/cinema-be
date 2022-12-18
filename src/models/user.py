from sqlalchemy import Column, ForeignKey, Integer, String, UniqueConstraint, event
from sqlalchemy.orm import relationship

from .base import Base
from .constraints import nonnegative
from .triggers import (
    validate_seat_func,
    validate_seat_trigger,
    validate_reservation_time_func,
    validate_reservation_time_trigger,
)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    login = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

    reviews = relationship("Review", back_populates="user")
    reservations = relationship("Reservation", back_populates="user")
    managed_cinemas = relationship("Cinema", back_populates="admin")


class Reservation(Base):
    __tablename__ = "reservations"
    __table_args__ = (
        UniqueConstraint("screening_id", "user_id", name="screen_id_user_id_unique"),
        UniqueConstraint("screening_id", "seat", name="screen_id_seat_unique"),
    )

    id = Column(Integer, primary_key=True)
    screening_id = Column(Integer, ForeignKey("screenings.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    seat = Column(
        Integer, nonnegative("seat"), nullable=False
    )  # needs trigger to check if is correct

    screening = relationship("Screening", back_populates="reservations")
    user = relationship("User", back_populates="reservations")


event.listen(
    Reservation.__table__,
    "after_create",
    validate_seat_func.execute_if(dialect="postgresql"),
)
event.listen(
    Reservation.__table__,
    "after_create",
    validate_seat_trigger.execute_if(dialect="postgresql"),
)

event.listen(
    Reservation.__table__,
    "after_create",
    validate_reservation_time_func.execute_if(dialect="postgresql"),
)
event.listen(
    Reservation.__table__,
    "after_create",
    validate_reservation_time_trigger.execute_if(dialect="postgresql"),
)