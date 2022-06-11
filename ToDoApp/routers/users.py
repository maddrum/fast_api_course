from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import models
from data_validators import PasswordUpdate
from routers.auth import get_current_user, get_password_auth
from routers.todos import check_user

router = APIRouter(prefix='/users', tags=['users'], responses={404: {'description': 'Not found'}})


@router.get('/')
async def get_users(db: Session = Depends(models.get_db)):
    return db.query(models.Users).all()


@router.get('/{id}')
async def get_users(id: int, db: Session = Depends(models.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.get('/get_user/')
async def get_users_query(id: int, db: Session = Depends(models.get_db)):
    user = db.query(models.Users).filter(models.Users.id == id).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user


@router.post('/update-password')
async def get_users_query(password_data: PasswordUpdate, db: Session = Depends(models.get_db),
                          user: dict = Depends(get_current_user)):
    check_user(user)
    user_obj = db.query(models.Users).filter(models.Users.id == user['user_id']).first()
    user_obj.hashed_password = get_password_auth(password_data.password)
    db.add(user_obj)
    db.commit()
    user_obj = db.query(models.Users).filter(models.Users.id == user['user_id']).first()
    return user_obj
