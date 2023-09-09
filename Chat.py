from langchain.chains import ConversationChain
from langchain.chains.conversation.memory import (ConversationBufferMemory, 
                                                  ConversationSummaryMemory, 
                                                  ConversationBufferWindowMemory,
                                                  ConversationKGMemory)
from langchain.callbacks import get_openai_callback
from langchain.llms import GooglePalm
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel


llm = GooglePalm(
    model='models/text-bison-001',
    temperature=0,
    # The maximum length of the response
    max_output_tokens=80000,
    google_api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM'
)


def count_tokens(chain, query):
    with get_openai_callback() as cb:
        result = chain.run(query)
        print(f'Spent a total of {cb.total_tokens} tokens')

    return result


# Initialize your LLM chain and conversation chain
llm = GooglePalm(
    model='models/text-bison-001',
    temperature=0,
    max_output_tokens=80000,
    google_api_key='AIzaSyA1fu-ob27CzsJozdr6pHd96t5ziaD87wM'
)

conversation_buf = ConversationChain(
    llm=llm,
    memory=ConversationBufferMemory()
)


# Initialize conversation_buf with the initial message
initial_message = "Good morning AI!, You are an Expert in Sales Key Result Areas (KRA) Setting and Performance Management. You are here to help me with my queries regarding Sales Key Result Areas (KRA) Setting and Performance Management."
conversation_buf(initial_message)


# Initialize FastAPI app
app = FastAPI()

# Define request and response models (if needed)
class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    response: str

# Define API endpoint for chat
@app.post("/chat/")
async def chat(request: Request):
    json_data = await request.json()
    query = json_data.get("query")

    try:
        response = count_tokens(conversation_buf, query)
        return {"response": response}
    except Exception as e:
        return HTTPException(status_code=500, detail=str(e))

# Define a route for initial setup (if needed)
@app.get("/")
def initial_setup():
    return {"message": "Server is up and running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
