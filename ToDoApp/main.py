from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from auth import get_current_user
from data_validators import TodoItem
from database import engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def check_user(user):
    if user is None:
        raise HTTPException(detail='No user found', status_code=400)


@app.get('/')
async def read_all(db: Session = Depends(models.get_db)):
    return db.query(models.Todos).all()


@app.get('/todo/user')
async def read_all_by_user(user: dict = Depends(get_current_user), db: Session = Depends(models.get_db)):
    check_user(user)
    return db.query(models.Todos).filter(models.Todos.owner_id == user['user_id']).all()


@app.post('/todo/add')
async def add_data(todo_item: TodoItem, db: Session = Depends(models.get_db), user: dict = Depends(get_current_user)):
    check_user(user)
    todo_model = models.Todos()
    todo_model.title = todo_item.title
    todo_model.description = todo_item.description
    todo_model.priority = todo_item.priority
    todo_model.complete = todo_item.complete
    todo_model.owner_id = user['user_id']
    db.add(todo_model)
    db.commit()

    return {
        'status_code': 201,
        'transaction': 'success',
        'object': db.query(models.Todos).filter(models.Todos.id == todo_model.id).first(),
    }


@app.put('/todo/{id}/change')
async def update_data(
        id,
        todo_item: TodoItem,
        db: Session = Depends(models.get_db),
        user: dict = Depends(get_current_user)):
    check_user(user)
    todo_model = db.query(models.Todos).filter(models.Todos.id == id, models.Todos.owner_id == user['user_id']).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Tupak! Nqma takowa tuka!')
    todo_model.title = todo_item.title
    todo_model.description = todo_item.description
    todo_model.priority = todo_item.priority
    todo_model.complete = todo_item.complete
    db.add(todo_model)
    db.commit()

    return {
        'status_code': 200,
        'transaction': 'success',
        'object': db.query(models.Todos).filter(models.Todos.id == todo_model.id).first(),
    }


@app.delete('/todo/{id}/delete')
async def delete_data(id: int, db: Session = Depends(models.get_db), user: dict = Depends(get_current_user)):
    check_user(user)
    todo_model = db.query(models.Todos).filter(models.Todos.id == id, models.Todos.owner_id == user['user_id']).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Tupak! Nqma takowa tuka!')
    db.delete(todo_model)
    db.commit()

    return {
        'status_code': 204,
        'transaction': 'deleted',
    }


@app.get('/todo/{todo_id}')
async def read_all(todo_id: int, db: Session = Depends(models.get_db), user: dict = Depends(get_current_user)):
    check_user(user)
    result = db.query(models.Todos).filter(models.Todos.id == todo_id, models.Todos.owner_id == user['user_id']).first()
    return result if result is not None else HTTPException(status_code=404, detail='Typak, nqma takowa!')
