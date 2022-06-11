from enum import Enum

from fastapi import FastAPI

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}


class Directions(str, Enum):
    up = 'up'
    down = 'down'


@app.get('/')
async def get_example():
    return BOOKS


@app.get('/specified-path-parameter/{book_id}')
async def unspecified_path_parameter(book_id):
    return BOOKS.get(book_id)


@app.get('/unspecified-path-parameter/{book_id}')
async def specified_path_parameter(book_id: int):
    return BOOKS.get(f'book_{book_id}')


@app.get('/enumerated-path-parameter/{dir_name}')
async def enumeration_path_parameters(dir_name: Directions):
    if dir_name == Directions.up:
        return {'dir': 'up'}
    return {'dir': 'down'}


@app.get('/query_parameter')
async def query_parameter(book_name: str):
    if book_name is not None:
        books = BOOKS.copy()
        del books[book_name]
        return books
    return BOOKS


@app.post('/post-example')
async def post_example(title, author):
    current_id = max([int(item.split('_')[-1]) for item in BOOKS.keys()])
    new_id = current_id + 1
    BOOKS[f'book_{new_id}'] = {'title': title, 'author': author}
    return BOOKS


@app.put('/put-example/{book_id}')
async def put_example(book_id: str, title: str):
    current = BOOKS.get(book_id)
    if current is None:
        return {'No book id found'}
    current['title'] = title
    BOOKS[book_id] = current
    return current


@app.delete('/put-example/{book_id}')
async def delete_example(book_id: str):
    current = BOOKS.get(book_id)
    if current is None:
        return {'No book id found'}
    del BOOKS[book_id]
    return {'status': 'Deleted'}
