from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request
from routers.middleware import KnownAppError
from models.chatbot import TShirtChatbot
from schemas.chat import ChatResponse, ChatMessage
from supabase_client import get_access_token

router = APIRouter()
chatbot_sessions = {}

@router.post("/chat", response_model=ChatResponse)
async def chat_with_bot(message: ChatMessage, request: Request):
    try:
        session_id = message.session_id or "default"
        access_token = None
        
        try:
            access_token = get_access_token(request)
        except:
            pass

        if session_id not in chatbot_sessions:
            chatbot_sessions[session_id] = TShirtChatbot()
        
        chatbot = chatbot_sessions[session_id]
        
        # Store access token in chatbot session for function calls
        if access_token:
            chatbot.access_token = access_token
        
        result = chatbot.process_user_input(message.message)
        
        # Handle the new response format
        if isinstance(result, dict):
            response = result.get("response", "Sorry, I didn't get that.")
            action_buttons = result.get("action_buttons")
        else:
            # Backward compatibility for old format
            response = result
            action_buttons = None

        return ChatResponse(
            response=response, 
            session_id=session_id,
            action_buttons=action_buttons
        )
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
            result = chatbot.process_user_input(data)
            
            # Handle the new response format
            if isinstance(result, dict):
                response = result.get("response", "Sorry, I didn't get that.")
            else:
                response = result
            
            await websocket.send_text(response)
    except WebSocketDisconnect:
        KnownAppError(f"Client {session_id} disconnected")