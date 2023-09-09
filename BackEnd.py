from fastapi import FastAPI, HTTPException, Request, Response
import google.generativeai as palm

palm.configure(api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM')

app = FastAPI()

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