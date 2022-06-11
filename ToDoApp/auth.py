from typing import Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from jose import jwt

import models
from data_validators import CreateUser, LoginUser

app = FastAPI()

SECRET_KEY = '123456'
ALGORITHM = 'HS256'

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')
oauth2_bearer = OAuth2PasswordBearer(tokenUrl='token')


def get_password_auth(password):
    return bcrypt_context.hash(password)


def password_check(user_obj, password):
    return bcrypt_context.verify(password, user_obj.hashed_password)


def authenticate_user(login_data, db):
    user = db.query(models.Users).filter(models.Users.username == login_data.username).first()
    if user is None:
        return None

    if not password_check(password=login_data.password, user_obj=user):
        return None
    return user


def create_access_token(username: str, user_id: int, expires_delta: Optional[timedelta] = None):
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    encode = {'sub': username, 'id': user_id, 'exp': expire}
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@app.post('/create/user')
async def create_new_user(create_user: CreateUser, db: Session = Depends(models.get_db)):
    username_count = db.query(models.Users).filter(models.Users.username == create_user.username).count()
    if username_count != 0:
        raise HTTPException(status_code=400, detail='User with that username already exists!')
    create_user_model = models.Users()
    create_user_model.email = create_user.email
    create_user_model.username = create_user.username
    create_user_model.first_name = create_user.first_name
    create_user_model.last_name = create_user.last_name
    create_user_model.hashed_password = get_password_auth(create_user.password)
    create_user_model.is_active = True

    db.add(create_user_model)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'success',
        'object': db.query(models.Users).filter(models.Users.id == create_user_model.id).first(),
    }


@app.post('/login')
async def login_user(login_data: LoginUser, db: Session = Depends(models.get_db)):
    user = authenticate_user(login_data=login_data, db=db)
    if user is None:
        raise HTTPException(status_code=400, detail='Wrong username or password')
    return {
        'status_code': 200,
        'transaction': 'success',
        'user': user
    }


@app.post('/token')
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(models.get_db)):
    user = authenticate_user(form_data, db)
    if user is None:
        raise HTTPException(detail='User not found', status_code=400)

    token_expires = timedelta(minutes=20)
    token = create_access_token(username=user.username, user_id=user.id, expires_delta=token_expires)

    return {
        'status_code': 200,
        'transaction': 'success',
        'token': token,
    }
