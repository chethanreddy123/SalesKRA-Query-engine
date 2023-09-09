from fastapi import FastAPI, HTTPException, Request, Response
import google.generativeai as palm
from fastapi.middleware.cors import CORSMiddleware


palm.configure(api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM')

app = FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


response = palm.chat(messages=["Jon is very good boy and works and microsoft"])

@app.post("/chat/")
async def chat(request: Request):
    data = await request.json()
    message = data.get("message")
    
    if message is None:
        raise HTTPException(status_code=400, detail="Message not provided")

    global response
    if message.upper() == "Q":
        return {"response": "Goodbye!"}

    response = response.reply(message)
    return {"response": response.last}
