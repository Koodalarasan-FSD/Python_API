from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Define the data model
class Book(BaseModel):
    title: str
    author: str
    description: Optional[str] = None
    year: int

# Define a response model including the id field
class BookResponse(BaseModel):
    id: int
    title: str
    author: str
    description: Optional[str] = None
    year: int

# In-memory storage for books
books = [
    {
        "id": 1,
        "title": "1984",
        "author": "George Orwell",
        "description": "Dystopian novel",
        "year": 1949
    },
    {
        "id": 2,
        "title": "To Kill a Mockingbird",
        "author": "Harper Lee",
        "description": "Novel about racism and justice",
        "year": 1960
    }
]

@app.get("/books/", response_model=List[BookResponse])
def list_books():
    return books

@app.get("/books/{book_id}", response_model=BookResponse)
def read_book(book_id: int):
    for book in books:
        if book["id"] == book_id:
            return book
    raise HTTPException(status_code=404, detail="Book not found")

@app.post("/books/", response_model=BookResponse)
def create_book(book: Book):
    # Generate a new book_id
    new_book_id = max(book['id'] for book in books) + 1 if books else 1
    
    # Update the book dictionary with the new book
    book_data = book.dict()
    book_data["id"] = new_book_id
    books.append(book_data)
    
    # Return the response including the id
    return book_data

@app.put("/books/{book_id}", response_model=BookResponse)
def update_book(book_id: int, book: Book):
    for item in books:
        if item["id"] == book_id:
            item.update(book.dict())
            item["id"] = book_id
            # Create a BookResponse object with the updated book data
            return BookResponse(**item)
    raise HTTPException(status_code=404, detail="Book not found")

@app.delete("/books/{book_id}", response_model=BookResponse)
def delete_book(book_id: int):
    for index, item in enumerate(books):
        if item["id"] == book_id:
            return books.pop(index)
    raise HTTPException(status_code=404, detail="Book not found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To Run/Execute the python file - Run these command:  uvicorn api:app --reload

"""
Accessing API Endpoints in the Browser
1) Get all data:
    - Open your browser and go to: http://127.0.0.1:8000/books/
2) Get a single data by ID:
    - Open your browser and go to: http://127.0.0.1:8000/books/1

Using Postman to Test(Accessing) API Endpoints
Postman is a popular tool for testing APIs. Here's how to use it:
1) Get all data:
    - Method: GET
    - URL: http://127.0.0.1:8000/books/
    - Click Send.
2) Get a single data by ID:
    - Method: GET
    - URL: http://127.0.0.1:8000/books/1
    - Click Send.
3) Create a new data:
    - Method: POST
    - URL: http://127.0.0.1:8000/books/
    - Go to the Body tab.
    - Select raw and JSON as the data format.
    - Enter the following JSON:
        {
            "title": "Nelson's Life of Medicine",
            "author": "Nelson tex",
            "description": "Novel about Medicine travel of Dr.Nelson",
            "year": 1969
        }
    - Click Send.
4) Update a data:
    - Method: PUT
    - URL: http://127.0.0.1:8000/books/1
    - Go to the Body tab.
    - Select raw and JSON as the data format.
    - Enter the following JSON:
        {
            "id": 2,
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "description": "Novel about racism and justice",
            "year": 1961
        }
    - Click Send.
5) Delete a data:
    - Method: DELETE
    - URL: http://127.0.0.1:8000/books/1
    - Click Send.
"""