from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

app = FastAPI()

# Program to create api's from csv file

# Define the data model
class Person(BaseModel):
    id: int
    name: str
    email: str
    age: int

# Function to load data from CSV
def load_data():
    df = pd.read_csv('data.csv')
    return df.to_dict(orient='records')

# Load data from CSV into memory
data = load_data()

@app.get("/persons/", response_model=List[Person])
def get_persons():
    return data

@app.get("/persons/{person_id}", response_model=Person)
def get_person(person_id: int):
    person = next((item for item in data if item["id"] == person_id), None)
    if person is None:
        raise HTTPException(status_code=404, detail="Person not found")
    return person

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To Run/Execute the python file - Run these command:  uvicorn createapifromcsv:app --reload
