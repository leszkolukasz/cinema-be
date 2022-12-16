from fastapi import Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from src.router import app
from src.database.utility import get_db
import src.dto as dto
import src.models as models
from src.services import *


@app.post("/sign-up")
def sign_up(user: dto.User, db: Session = Depends(get_db)):
    create_user(db, user.login, user.password)

@app.post('/login')
def login(user: dto.User, Authorize: AuthJWT = Depends(), db: Session = Depends(get_db)):
    db_user = find_user_by_login(db, user.login)

    if not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Bad username or password")

    access_token = Authorize.create_access_token(subject=db_user.id)
    return {"token": access_token, "username": db_user.login}