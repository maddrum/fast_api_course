from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session

import models
from database import engine, SessionLocal
from data_validators import TodoItem

app = FastAPI()
models.Base.metadata.create_all(bind=engine)





@app.get('/')
async def read_all(db: Session = Depends(get_db)):
    return db.query(models.Todos).all()


@app.post('/todo/add')
async def add_data(todo_item: TodoItem, db: Session = Depends(get_db)):
    todo_model = models.Todos()
    todo_model.title = todo_item.title
    todo_model.description = todo_item.description
    todo_model.priority = todo_item.priority
    todo_model.complete = todo_item.complete
    db.add(todo_model)
    db.commit()

    return {
        'status_code': 201,
        'transaction': 'success',
        'object': db.query(models.Todos).filter(models.Todos.id == todo_model.id).first(),
    }


@app.put('/todo/{id}/change')
async def update_data(id, todo_item: TodoItem, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == id).first()
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
async def delete_data(id: int, db: Session = Depends(get_db)):
    todo_model = db.query(models.Todos).filter(models.Todos.id == id).first()
    if todo_model is None:
        raise HTTPException(status_code=404, detail='Tupak! Nqma takowa tuka!')
    db.delete(todo_model)
    db.commit()

    return {
        'status_code': 204,
        'transaction': 'deleted',
    }


@app.get('/todo/{todo_id}')
async def read_all(todo_id: int, db: Session = Depends(get_db)):
    result = db.query(models.Todos).filter(models.Todos.id == todo_id).first()
    return result if result is not None else HTTPException(status_code=404, detail='Typak, nqma takowa!')
