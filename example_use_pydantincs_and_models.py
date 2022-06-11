from typing import Optional
from uuid import UUID

from fastapi import FastAPI, Form, Header, HTTPException, Request, status
from pydantic import BaseModel, Field
from starlette.responses import JSONResponse

app = FastAPI()

BOOKS = {
    'book_1': {'title': 'Title One', 'author': 'Author One'},
    'book_2': {'title': 'Title Two', 'author': 'Author Two'},
    'book_3': {'title': 'Title Three', 'author': 'Author Three'},
    'book_4': {'title': 'Title Four', 'author': 'Author Four'},
    'book_5': {'title': 'Title Five', 'author': 'Author Five'},
}


class NegativeNumberException(Exception):
    def __int__(self, obj, message):
        self.message = message
        super().__init__(self.message)


class Book(BaseModel):
    id: UUID
    title: str = Field(min_length=1, title='Title of book')
    author: str
    rating: Optional[int] = Field(le=5, ge=1)

    class Config:
        schema_extra = {
            'example':
                {
                    'id': "3fa85f64-5717-4562-b3fc-2c963f66afa6",
                    'title': 'Example title',
                    'author': 'Example author',
                    'rating': 5
                }

        }


@app.exception_handler(NegativeNumberException)
async def negative_number_handler(request: Request, exception: NegativeNumberException):
    return JSONResponse(status_code=418, content={'message': 'FU be glupak!'})


@app.get('/')
async def read_all_books(books_to_return: Optional[int] = None):
    if books_to_return is not None and books_to_return > 0:
        return BOOKS[:books_to_return]
    return BOOKS


@app.post('/', status_code=status.HTTP_201_CREATED)
async def post_example_with_object(book: Book):
    BOOKS.append(book)
    return book


@app.get('/header-example')
async def read_header_example(random_header: Optional[str] = Header(None)):
    return {'Random-Header': random_header}


@app.get('/header-login')
async def check_login_data(username: str | None = Header(None), password: str | None = Header(None)):
    if username == 'test' and password == 'test':
        return BOOKS
    raise HTTPException(detail='Fucking login damn it!', status_code=403, headers={'login-header': 'FU'})


@app.post('/form-example', status_code=status.HTTP_201_CREATED)
async def post_data_example(username: str = Form(...), password: str = Form(...)):
    print(username)
    print(password)
    return {'username': username, 'password': password}


@app.get('/{uuid}')
async def get_example_with_object(uuid: UUID):
    for item in BOOKS:
        if item.id == uuid:
            return item
    return None


@app.put('/book/update/{uuid}')
async def put_example_with_object(uuid: UUID, book: Book):
    for item in BOOKS:
        # update element of book code
        pass
    return BOOKS


@app.delete('/{uuid}')
async def delete_item_example(uuid: UUID):
    for item in BOOKS:
        if item.id == uuid:
            # remove book from list code
            pass
    return BOOKS


@app.delete('/exception/{uuid}')
async def raise_exception_example(uuid: UUID):
    raise HTTPException(detail=f'Nope! I do not want to!! {uuid}', status_code=404, headers={'test-header': 'FU'})


@app.delete('/custom-exception/{uuid}')
async def raise_custom_exception_example(uuid: UUID):
    raise NegativeNumberException(BOOKS, 'test_message')
