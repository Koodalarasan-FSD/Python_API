import json
from typing import List, Optional
from fastapi import FastAPI, HTTPException, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Load books(api's) from the JSON file and to display in web page.

# Define the data model
class Book(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: int

# Load books(api's) from the JSON file
def load_books():
    with open("books.json", "r") as file:
        return {book["id"]: Book(**book) for book in json.load(file)}

books = load_books()

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("Book.html", {"request": request, "books": list(books.values())})

@app.post("/books/", response_model=Book)
def create_book(book: Book):
    if book.id in books:
        raise HTTPException(status_code=400, detail="Book ID already exists")
    books[book.id] = book
    return book

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int):
    if book_id not in books:
        raise HTTPException(status_code=404, detail="Book not found")
    return books[book_id]

@app.get("/books/", response_model=List[Book])
def list_books():
    return list(books.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To Run/Execute the python file - Run these command:  uvicorn apifromjsonfile:app --reload
