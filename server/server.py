import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Allow requests from your frontend (adjust the URL as needed)
origins = [
    "http://localhost:5173",  # React dev server
    # Add your deployed frontend URL here when needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Can also use ["*"] for all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers (including Authorization)
)

# Activation importance:
# source ../.venv/bin/activate
# pip install "fastapi[all]"

# main is name of file, this file is server.py, so it is "server":
# uvicorn main:app --reload
@app.get("/api")
async def read_root():
    print("hello")
    await asyncio.sleep(5)
    return {"message": "Hello from FastAPI!"}
