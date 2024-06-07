from fastapi import FastAPI
import httpx

app = FastAPI()

# Retrieve & Display API's from External(other) Link(source)
@app.get("/posts/")
async def get_posts():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://jsonplaceholder.typicode.com/posts")
        return response.json()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)

# To Run/Execute the python file - Run these command:  uvicorn apifromexternallink:app --reload
