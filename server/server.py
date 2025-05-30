import asyncio
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

import sys
from pathlib import Path

from server.Yoel.parser import extract_tagged_text
from server.services.TTS.audio import conversation_with_user
# Get absolute path to project root
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from server.Yoel.model import BilingualContentGenerator
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
# uvicorn server.server:app --reload


# Create dialog instance
dialog = Dialog()
teacher = BilingualContentGenerator()
teacher.initialize()

@app.post("/api")
async def read_root(data: RequestData):
    print("Received data:", data.input)
    
    connected_history: str = '\n'.join(teacher.history)
    output = teacher.generate_bilingual_content(connected_history + "\n\n Current input:\n" + data.input)
    return {"message": extract_tagged_text(output)}

@app.post("/explain-word")
async def read_root(data: RequestData):
    print("Received data:", data.input)
    # TODO: check if it is single word?
    final_description = dialog.explain_word(data.input);
    print("final",final_description)
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

from fastapi import Form
from fastapi.responses import StreamingResponse
from gtts import gTTS
from io import BytesIO
from server.services.TTS.text_to_speak import TextToSpeechConverter

ttsConv = TextToSpeechConverter()

# pip install playsound

#pip install gTTS
@app.post("/tts")
async def tts(text: str = Form(...)):
    ttsConv.exelarate(text)

    # audio_bytes = BytesIO()
    # ttsConv.write_to_fp(audio_bytes)
    # audio_bytes.seek(0)
    # return StreamingResponse(audio_bytes, media_type="audio/mpeg")



@app.post("/stt")
async def stt(text: str = Form(...)):
    return {"message": conversation_with_user(text)}



# import sys
# from pathlib import Path
# sys.path.append(str(Path(__file__).parent))
# from server.services.LLM.gemini import *

# @app.post("/student")
# async def studentUpdate(input: str):
#     final_input = "The following input represents the state of the student: \n\n" + \
#                     input + "\n\n Return a json object that contains the same state parameters "+\
#                         "that are changed in accordance with the conversation reply: " +\
#                         "\n\n the JSON needs to include the following fields: name, age, gender, background_info, arabic_proficiency_level"
#     gemini = init_model(model_name='gemini-2.0-flash')
#     response = gemini.json_chat.send_message(final_input)

#     print(response)
#     return {"message": response.result.candidates.content.parts[0]}