# Run `python main.py` in the terminal

# Note: Python is lazy loaded so the first run will take a moment,
# But after cached, subsequent loads are super fast! ⚡️

from fastapi import FastAPI
from schema import BOOK
from typing import List

BOOKS_DB = {}
app = FastAPI("/api")

#----------------------------------------Routes--------------------#
@app.get('/books') # pagination
def get_books(start: int, count: int) -> List[BOOK]:
    start = max(start, 0) # start index must not be less than 0
    count = max(min(count, 30), 1) # count must be between 1-30
    if len(BOOKS_DB) < (start+count):
        return {'error': 'Invalid page start and count value'}
    return BOOKS_DB.items()[start:count]


@app.get('/books/:id')
def get_book(isbn: int) -> BOOK:
    return BOOKS_DB[isbn]


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