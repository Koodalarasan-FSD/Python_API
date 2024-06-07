from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from typing import List, Optional
import uuid
import json

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Define the data model
class FormData(BaseModel):
    id: str
    name: str
    email: str
    message: Optional[str] = None

# In-memory storage for form data
form_data_store = {}

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("form.html", {"request": request})

@app.post("/submit", response_class=RedirectResponse)
async def submit_form(name: str = Form(...), email: str = Form(...), message: Optional[str] = Form(None)):
    form_id = str(uuid.uuid4())
    form_data_store[form_id] = FormData(id=form_id, name=name, email=email, message=message)
    return RedirectResponse(url=f"/data/{form_id}", status_code=303)

@app.get("/data/{form_id}", response_class=HTMLResponse)
def read_data(request: Request, form_id: str):
    if form_id not in form_data_store:
        raise HTTPException(status_code=404, detail="Form data not found")
    form_data = form_data_store[form_id]
    form_data_json = json.dumps(form_data.dict(), indent=4)
    return templates.TemplateResponse("data.html", {"request": request, "form_data_json": form_data_json})

@app.get("/data", response_model=List[FormData])
def list_data():
    return list(form_data_store.values())

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To Run/Execute the python file - Run these command:  uvicorn createapifromform:app --reload
