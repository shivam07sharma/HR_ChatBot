from fastapi import FastAPI
from bot import run_bot, getUserMemory
from pydantic import BaseModel
app = FastAPI()

class UserInput(BaseModel):
    user_id: str
    message: str

@app.post("/chat")
def homeChat(request:UserInput):
    user_input = request.message
    session = request.user_id.lower()
    response = run_bot(user_input,session)
    return {"response": response}

@app.get("/history")
def get_history(user_id: str):
    session = user_id.lower()
    memory = getUserMemory(session)
    raw_history = memory.load_memory_variables({})["chat_history"]
    
    formatted = []
    for msg in raw_history:
        role = "user" if msg.type == "human" else "assistant"
        formatted.append({"role": role, "content": msg.content})
        
    return {"messages": formatted}
# ... your existing FastAPI code ...

# if __name__ == "__main__":
#     uvicorn.run("server:app", host="127.0.0.1", port=8000, reload=True)