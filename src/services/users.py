import src.models as models
from src.services import *

def create_user(db, login, password):
    hashed_password = get_password_hash(password)
    db_user = models.User(login=login, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def find_user_by_login(db, login):
    return db.query(models.User).filter(models.User.login == login).one()

def get_reservations_by_user_id(db, user_id):
    user = db.query(models.User).filter(models.User.id == user_id).one()
    return user.reservations

def delete_reservation_by_id(db, user_id, reservation_id):
    reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).one()
    print(reservation, user_id)
    if reservation.user.id != user_id:
        return False
    db.delete(reservation)
    db.commit()
    return True

def reserve_seat_for_user(db, screening_id, user_id, seat):
    reservation = models.Reservation(screening_id=screening_id, user_id=user_id, seat=seat)
    db.add(reservation)
    db.commit()