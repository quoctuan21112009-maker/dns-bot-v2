from fastapi import WebSocket
from typing import Dict, Set, Callable
import logging
import json

logger = logging.getLogger(__name__)

class WebSocketManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set[WebSocket]] = {}
        self.user_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str, room: str = "default"):
        """Accept and register a WebSocket connection"""
        await websocket.accept()
        
        if room not in self.active_connections:
            self.active_connections[room] = set()
        
        self.active_connections[room].add(websocket)
        self.user_connections[client_id] = websocket
        
        logger.info(f"✅ Client {client_id} connected to room {room}")
    
    async def disconnect(self, client_id: str, room: str = "default"):
        """Remove a WebSocket connection"""
        if room in self.active_connections:
            websocket = self.user_connections.get(client_id)
            if websocket:
                self.active_connections[room].discard(websocket)
        
        self.user_connections.pop(client_id, None)
        logger.info(f"❌ Client {client_id} disconnected")
    
    async def broadcast(self, message: dict, room: str = "default"):
        """Broadcast message to all users in room"""
        if room not in self.active_connections:
            return
        
        disconnected = set()
        for websocket in self.active_connections[room]:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Broadcast error: {e}")
                disconnected.add(websocket)
        
        # Remove disconnected
        self.active_connections[room] -= disconnected
    
    async def send_to_user(self, client_id: str, message: dict):
        """Send message to specific user"""
        websocket = self.user_connections.get(client_id)
        if websocket:
            try:
                await websocket.send_json(message)
            except Exception as e:
                logger.error(f"Send to user error: {e}")

# Global manager
ws_manager = WebSocketManager()