# HUJI Hackathon 2025
An Arabic learning website from Hebrew speakers

# Structure
The project is a full-stack project, with a front-end(writtern in React, in the "client" folder) 
and a back-end(written in Python with FastAPI, in the "server" folder)

To make it run properly, both the server and client should run at the same time:
The Server will run at http://localhost:8000
The Client will run at http://localhost:5173

# Requirements:
To run the project both the client and the server need to be set up properly.
First, clone the repository:
```
git clone https://github.com/JonathanMiroshnik/HUJIHackathon2025.git
```

## Client:
To run the Client, you must install the npm packages within:
```
cd HUJIHackathon2025/client
npm install
npm run dev
```

## Server:
Because this is a Python server, we recommend to create a Python virtual environment and install the packages:
```
pip install -r server/requirements.txt
```

For the LLM secction of the project, we use Google's Gemini, to make it work, please add a file called ".env" in the "server" folder and add the Gemini API key to such a line:
```
GEMINI_API_KEY=API_KEY_HERE
```

To run the server, we use uvicorn:
```
uvicorn server.server:app --reload
```

Further notes on the proper installation and running of the project can be found at the top of server/server.py
