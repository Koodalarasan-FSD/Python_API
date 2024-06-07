from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import httpx

app = FastAPI()

# Retrieve API's from other Link(source) and to send as JSON directly to display it in HTML.

# Set up Jinja2 templates
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def read_posts(request: Request):
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        posts = response.json()
    return templates.TemplateResponse("index.html", {"request": request, "posts": posts})

# To Run/Execute the python file - Run these command:  uvicorn displayapifromexternallink:app --reload
