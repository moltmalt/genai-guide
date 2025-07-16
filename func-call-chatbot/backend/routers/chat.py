from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from routers.middleware import KnownAppError
from models.chatbot import TShirtChatbot
from schemas.chat import ChatResponse, ChatMessage

router = APIRouter()
chatbot_sessions = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(message: ChatMessage):
    try:
        session_id = message.session_id or "default"

        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = TShirtChatbot()
        
        chatbot = chatbot_sessions[session_id]
        response = chatbot.process_user_input(message.message)

        return ChatResponse(response=response, session_id=session_id)
    except Exception as e:
        raise KnownAppError(str(e), status_code=500)
    
@router.websocket("/ws/chat/{session_id}")
async def websocket_chat(websocket: WebSocket, session_id: str):
    await websocket.accept()
    
    if session_id not in chatbot_sessions:
        chatbot_sessions[session_id] = TShirtChatbot()
    
    chatbot = chatbot_sessions[session_id]
    
    try:
        while True:
            data = await websocket.receive_text()
            response = chatbot.process_user_input(data)
            await websocket.send_text(response)
    except WebSocketDisconnect:
        KnownAppError(f"Client {session_id} disconnected")