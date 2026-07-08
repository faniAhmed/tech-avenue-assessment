# Run `python main.py` in the terminal

# Note: Python is lazy loaded so the first run will take a moment,
# But after cached, subsequent loads are super fast! ⚡️

from fastapi import FastAPI
from schema import BOOK
from typing import List

BOOKS_DB = {}
app = FastAPI("/api")

#----------------------------------------Routes--------------------#
"""
Forgot the import and return method for exact status codes, 
added comments instead. 
Validation errors are handled by the Schema and fastapi.
Respective error code is also returned on Validation errors
"""

@app.get('/books') # pagination
def get_books(start: int, count: int) -> List[BOOK]:
    start = max(start, 0) # start index must not be less than 0
    count = max(min(count, 30), 1) # count must be between 1-30
    if len(BOOKS_DB) < (start+count):
        return {'error': 'Invalid page start and count value'}
    return BOOKS_DB.values()[start:count]


@app.get('/books/:id')
def get_book_bt_isbn(isbn: int) -> BOOK:
    return BOOKS_DB[isbn]


@app.get('/books/:title')
def get_book_by_title(search_title: str) -> BOOK
    for book in BOOKS_DB.values():
        title = book.get('title')
        if search_title in title:
            return book
    return {'error': "Book doesn't exist in the db"} # 404 error code


@app.post('/books')
def add_book(new_book: BOOK) -> BOOK | dict:
    new_book_isbn = new_book['isbn']
    if new_book_isbn in BOOKS_DB:
        return {'error': 'Duplicate entry, book already exists'} # Code for duplicate data entry
    BOOKS_DB[new_book_isbn] = new_book
    return BOOKS_DB[new_book_isbn]


@app.put('/books/:id')
def update_book(isbn: int, data: UpdateBook) -> BOOK | dict:
    if isbn not in BOOKS_DB:
        return {'error': "Book doesn't exist in the database"} # 404 book not found
    book = BOOKS_DB[isbn]
    book |= data
    BOOKS_DB[isbn] = book
    return BOOKS_DB[isbn]


@app.delete('/books/:id')
def delete_book(isbn: int) -> BOOK | dict:
    if isbn not in BOOKS_DB:
        return {'error': "Book doesn't exist in the database"} # 404 book not found
    return BOOKS_DB.pop(isbn)