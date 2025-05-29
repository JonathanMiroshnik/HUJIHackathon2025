import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
from pathlib import Path
# Get absolute path to project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from server.controllers.languageHelper import Dialog




app = FastAPI()

# Allow requests from your frontend (adjust the URL as needed)
origins = [
    "http://localhost:5173",  # React dev server
    # Add your deployed frontend URL here when needed
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Can also use ["*"] for all origins (dev only)
    allow_credentials=True,
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],     # Allow all headers (including Authorization)
)



# Define a Pydantic model for expected JSON input
class RequestData(BaseModel):
    input: str  # or any other fields



# Activation importance:
# source ../.venv/bin/activate
# pip install "fastapi[all]"

# main is name of file, this file is server.py, so it is "server":
# uvicorn server:app --reload




# Create dialog instance
dialog = Dialog()




@app.post("/api")
async def read_root(data: RequestData):
    print("Received data:", data.input)
    await asyncio.sleep(1)  # Simulate processing
    return {"message": f"Processed: {data.input}"}

@app.post("/explain-word")
async def read_root(data: RequestData):
    print("Received data:", data.input)
    # TODO: check if it is single word?
    final_description = dialog.explain_word(data.input);
    print(final_description)
    return final_description


class StringRequest(BaseModel):
    input: list[str]  # Must match exactly what you send from frontend

@app.post("/arabic-speech-continue-conversation")
async def read_root(data: StringRequest):
    print("Received data:", data.input)
    # TODO: check if it is single word?
    final_description = dialog.continue_conversation(data.input);
    print(final_description)
    return {"message": final_description}


@app.post("/arabic-speech-explanation")
async def read_root(data: StringRequest):
    print("Received data:", data.input)
    # TODO: check if it is single word?
    final_description = dialog.explain_conversation(data.input);
    print(final_description)
    return {"message": final_description}

# # Use explain_sentence
# hebrew_explanation = dialog.explain_sentence(arabic_sentence, arabic_question)