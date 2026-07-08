from typing import BaseModel

class BOOK(BaseModel):
    isbn: int # will act as primary key
    title: str
    author: str

class UpdateBook(BaseModel):
    title: str
    author: str