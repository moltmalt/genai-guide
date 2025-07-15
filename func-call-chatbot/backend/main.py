from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, List
from func_call_oop import TShirtDatabase, TShirtChatbot
from decimal import Decimal
from fastapi import WebSocket, WebSocketDisconnect

import uvicorn
import os, json

app = FastAPI(
    title = "T-Shirt Store API",
    description="API for t-shirt ordering system",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

BASE_DIR = "../mock-db"

class TShirtRequest(BaseModel):
    name: str
    size: str
    color: str

class CartItem(BaseModel):
    name: str
    quantity: int
    size: str
    color: str
    price: Decimal

class OrderRequest(BaseModel):
    name: str
    quantity: int
    size: str
    color: str
    price: Decimal

class ChatMessage(BaseModel):
    message: str
    session_id: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    session_id: str

database = TShirtDatabase()
chatbot_sessions = {}

@app.get("/")
async def root():
    return{
        "message": "T-Shirt API is running"
    }

@app.get("/api/products")
def get_products():
    file_path = os.path.join(BASE_DIR, "shirt.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@app.get("/api/cart")
def get_cart():
    file_path = os.path.join(BASE_DIR, "cart.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@app.get("/api/order")
def get_order():
    file_path = os.path.join(BASE_DIR, "order.json")
    with open(file_path, "r") as f:
        data = json.load(f)
    return JSONResponse(data)

@app.post("/api/tshirts/search")
async def get_t_shirts(request: TShirtRequest):
    try:
        result = database.get_t_shirts(
            name = request.name,
            size = request.size,
            color =  request.color
        )
        return {"success": True, "data": result}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@app.post("/api/cart/add")
async def add_to_cart(item: CartItem):
    try:
        result = database.get_t_shirts(
            name = item.name,
            quantity = item.quantity,
            size = item.size,
            color = item.color,
            price = item.price
        )
        return {"success": True, "message": "Item added to cart" ,"data": result}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

@app.post("/api/order/place")
async def place_order(item: CartItem):
    try:
        result = database.place_order(
            name = item.name,
            quantity = item.quantity,
            size = item.size,
            color = item.color,
            price = item.price
        )
        return {"success": True, "message": "Order placed succesfully" ,"data": result}
    except Exception as e:
        raise HTTPException(status_code = 500, detail=str(e))

# chatbot endpoint

@app.post("/api/chat", response_model=ChatResponse)
async def chat_with_bot(message: ChatMessage):
    try:
        session_id = message.session_id or "default"

        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = TShirtChatbot()
        
        chatbot = chatbot_sessions[session_id]
        response = chatbot.process_user_input(message.message)

        return ChatResponse(response=response, session_id=session_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# for error handling

@app.exception_handler(404)
async def not_found_handler(request, exc):
    return JSONResponse(
        status_code=404,
        content={"message": "Endpoint not found"}
    )

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error"}
    )

# WebSocket support for real-time chat (optional)

@app.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = TShirtChatbot()
    
    chatbot = chatbot_sessions[session_id]
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            # Process with chatbot
            response = chatbot.process_user_input(data)
            
            # Send response back
            await websocket.send_text(response)
    except WebSocketDisconnect:
        print(f"Client {session_id} disconnected")

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  
        log_level="info"
    )
