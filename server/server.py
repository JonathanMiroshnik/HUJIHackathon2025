# For the virtual environment:
# source ../.venv/bin/activate

# For the FastAPI library:
# pip install "fastapi[all]"
# Also make sure to install the requirements: pip install -r requirements.txt

# For starting the backend server:
# uvicorn server.server:app --reload

import sys
from pathlib import Path
from io import BytesIO
from typing import Any, Optional
from fastapi import HTTPException, FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from gtts import gTTS

from services.TTS.text_to_speak import TextToSpeechConverter
from Yoel.parser import extract_tagged_text
from services.TTS.audio import conversation_with_user

# Get absolute path to project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from Yoel.model import BilingualContentGenerator
from controllers.languageHelper import Dialog

# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent))
# from server.services.LLM.gemini import *

# FastAPI start-up
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

# Pydantic model for expected JSON input
class RequestData(BaseModel):
    input: str

class StringRequest(BaseModel):
    input: list[str]

class ErrorResponse(BaseModel):
    error: str
    details: str | None = None

class WordExplanation(BaseModel):
    word: str
    explanation: str
    language: str = "en"

class ResponseWrapper(BaseModel):
    success: bool
    data: Optional[Any] = None
    error: Optional[ErrorResponse] = None

# # Use explain_sentence
# hebrew_explanation = dialog.explain_sentence(arabic_sentence, arabic_question)

ttsConv = TextToSpeechConverter()

# Create dialog instance
dialog = Dialog()
teacher = BilingualContentGenerator()
teacher.initialize()


@app.post("/api", response_model=ResponseWrapper)
async def api(data: RequestData):
    print("Received data:", data.input)
    
    connected_history: str = '\n'.join(teacher.history)
    output = teacher.generate_bilingual_content(connected_history + "\n\n Current input:\n" + data.input)

    return {
        "success":"true",
        "data":extract_tagged_text(output)
    }


@app.post("/explain-word", response_model=ResponseWrapper)
async def explain_word_route(data: RequestData):
    print("Received data:", data.input)

    if len(data.input.split()) != 1:
        return {
            "success": False,
            "error": {
                "message": "Invalid input",
                "details": "Please provide exactly one word"
            }
        }
    
    explanation = dialog.explain_word(data.input)
    return {
        "success": True,
        "data": {
            "word": data.input,
            "parts": explanation
        }
    }


@app.post("/arabic-speech-continue-conversation", response_model=ResponseWrapper)
async def arabic_speech_continue_conversation(data: StringRequest):
    print("Received data:", data.input)

    final_description = dialog.continue_conversation(data.input);

    return {
        "success": True,
        "data": final_description
    }


@app.post("/arabic-speech-explanation", response_model=ResponseWrapper)
async def arabic_speech_explanation(data: StringRequest):
    print("Received data:", data.input)
    
    final_description = dialog.explain_conversation(data.input);

    return {
        "success": True,
        "data": final_description
    }

@app.post("/translate", response_model=ResponseWrapper)
async def translate_from_arabic(data: StringRequest):
    print("Received data:", data.input)
    
    final_description = dialog.translate_conversation(data.input);

    return {
        "success": True,
        "data": final_description
    }


@app.post("/tts", response_model=ResponseWrapper)
async def tts(text: str = Form(...)):
    ttsConv.exelarate(text)

    # audio_bytes = BytesIO()
    # ttsConv.write_to_fp(audio_bytes)
    # audio_bytes.seek(0)
    # return StreamingResponse(audio_bytes, media_type="audio/mpeg")


@app.post("/stt", response_model=ResponseWrapper)
async def stt(text: str = Form(...)):
    return {"message": conversation_with_user(text)}


# @app.post("/student", response_model=ResponseWrapper)
# async def studentUpdate(input: str):
#     final_input = "The following input represents the state of the student: \n\n" + \
#                     input + "\n\n Return a json object that contains the same state parameters "+\
#                         "that are changed in accordance with the conversation reply: " +\
#                         "\n\n the JSON needs to include the following fields: name, age, gender, background_info, arabic_proficiency_level"
#     gemini = init_model(model_name='gemini-2.0-flash')
#     response = gemini.json_chat.send_message(final_input)

#     print(response)
#     return {"message": response.result.candidates.content.parts[0]}