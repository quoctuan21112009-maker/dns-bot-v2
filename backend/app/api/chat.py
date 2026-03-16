from fastapi import APIRouter, Depends, WebSocket, Query, UploadFile, File, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from app.database import get_db_session
from app.models.user import User
from app.models.message import Message
from app.websocket import ws_manager
from app.services.ai_service import AIService
import logging
import os

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/chat", tags=["chat"])

class ChatRequest(BaseModel):
    message: str
    session_id: str

class ChatResponse(BaseModel):
    reply: str
    tokens_used: int
    model_used: str

@router.post("/send", response_model=ChatResponse)
async def send_message(
    request: ChatRequest,
    db: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(lambda: None),  # Get from JWT
):
    """Send message and get AI response"""
    
    # Save user message
    user_msg = Message(
        user_id=current_user.id,
        session_id=request.session_id,
        role="user",
        content=request.message,
        model_used=current_user.ai_model
    )
    db.add(user_msg)
    
    # Get AI response
    ai_service = AIService(
        provider=current_user.ai_provider,
        api_key=current_user.ai_api_key
    )
    
    try:
        response_text, tokens = await ai_service.chat(request.message)
        
        # Save AI response
        ai_msg = Message(
            user_id=current_user.id,
            session_id=request.session_id,
            role="assistant",
            content=response_text,
            tokens_used=tokens,
            model_used=current_user.ai_model
        )
        db.add(ai_msg)
        await db.commit()
        
        # Broadcast to WebSocket
        await ws_manager.broadcast({
            "type": "message:new",
            "message": {
                "id": ai_msg.id,
                "role": "assistant",
                "content": response_text,
                "created_at": ai_msg.created_at.isoformat()
            }
        }, room=request.session_id)
        
        return ChatResponse(
            reply=response_text,
            tokens_used=tokens,
            model_used=current_user.ai_model
        )
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.websocket("/ws/{session_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    session_id: str,
    user_id: int = Query(...)
):
    """WebSocket endpoint for real-time chat"""
    await ws_manager.connect(websocket, f"user_{user_id}", room=session_id)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "message:send":
                # Broadcast user is typing
                await ws_manager.broadcast({
                    "type": "user:typing",
                    "user_id": user_id
                }, room=session_id)
                
                # Process message
                logger.info(f"Message from user {user_id}: {data.get('content')[:50]}")
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        await ws_manager.disconnect(f"user_{user_id}", room=session_id)