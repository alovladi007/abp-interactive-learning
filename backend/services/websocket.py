"""
WebSocket Service for Real-time Features
Handles notifications, chat, and live updates
"""

from fastapi import WebSocket, WebSocketDisconnect, Depends, HTTPException, status
from typing import Dict, List, Set, Optional, Any
import json
import asyncio
from datetime import datetime
import redis.asyncio as redis
from sqlalchemy.orm import Session
from sqlalchemy import and_, or_

from ..database import get_db
from ..models.user import User
from ..models.payment import Notification
from ..auth import get_current_user_ws


class ConnectionManager:
    """
    Manages WebSocket connections for real-time features
    """
    
    def __init__(self):
        # Active connections: {user_id: [websocket_connections]}
        self.active_connections: Dict[int, List[WebSocket]] = {}
        
        # Room subscriptions: {room_id: Set[user_id]}
        self.rooms: Dict[str, Set[int]] = {}
        
        # User presence tracking
        self.user_presence: Dict[int, Dict[str, Any]] = {}
        
        # Redis for pub/sub across multiple servers
        self.redis_client = None
        self.pubsub = None
        
    async def initialize_redis(self):
        """Initialize Redis connection for pub/sub"""
        self.redis_client = await redis.from_url(
            "redis://localhost:6379",
            encoding="utf-8",
            decode_responses=True
        )
        self.pubsub = self.redis_client.pubsub()
        
    async def connect(self, websocket: WebSocket, user_id: int):
        """
        Accept WebSocket connection and add to active connections
        """
        await websocket.accept()
        
        if user_id not in self.active_connections:
            self.active_connections[user_id] = []
        
        self.active_connections[user_id].append(websocket)
        
        # Update user presence
        self.user_presence[user_id] = {
            "status": "online",
            "last_seen": datetime.utcnow().isoformat(),
            "connection_count": len(self.active_connections[user_id])
        }
        
        # Notify user's contacts about online status
        await self.broadcast_presence_update(user_id, "online")
        
        # Send pending notifications
        await self.send_pending_notifications(websocket, user_id)
        
        print(f"User {user_id} connected. Total connections: {len(self.active_connections[user_id])}")
        
    async def disconnect(self, websocket: WebSocket, user_id: int):
        """
        Remove WebSocket connection and update presence
        """
        if user_id in self.active_connections:
            if websocket in self.active_connections[user_id]:
                self.active_connections[user_id].remove(websocket)
            
            if not self.active_connections[user_id]:
                del self.active_connections[user_id]
                
                # Update user presence
                self.user_presence[user_id] = {
                    "status": "offline",
                    "last_seen": datetime.utcnow().isoformat(),
                    "connection_count": 0
                }
                
                # Notify user's contacts about offline status
                await self.broadcast_presence_update(user_id, "offline")
                
                # Leave all rooms
                for room_id in list(self.rooms.keys()):
                    if user_id in self.rooms[room_id]:
                        self.rooms[room_id].remove(user_id)
                        if not self.rooms[room_id]:
                            del self.rooms[room_id]
        
        print(f"User {user_id} disconnected")
        
    async def send_personal_message(self, message: str, user_id: int):
        """
        Send message to specific user
        """
        if user_id in self.active_connections:
            for connection in self.active_connections[user_id]:
                try:
                    await connection.send_text(message)
                except:
                    # Connection might be closed
                    pass
                    
    async def send_json_to_user(self, data: Dict[str, Any], user_id: int):
        """
        Send JSON data to specific user
        """
        message = json.dumps(data)
        await self.send_personal_message(message, user_id)
        
    async def broadcast(self, message: str, exclude_user: Optional[int] = None):
        """
        Broadcast message to all connected users
        """
        for user_id, connections in self.active_connections.items():
            if user_id != exclude_user:
                for connection in connections:
                    try:
                        await connection.send_text(message)
                    except:
                        pass
                        
    async def broadcast_to_room(self, room_id: str, message: str, exclude_user: Optional[int] = None):
        """
        Broadcast message to all users in a specific room
        """
        if room_id in self.rooms:
            for user_id in self.rooms[room_id]:
                if user_id != exclude_user and user_id in self.active_connections:
                    for connection in self.active_connections[user_id]:
                        try:
                            await connection.send_text(message)
                        except:
                            pass
                            
    async def join_room(self, room_id: str, user_id: int):
        """
        Add user to a room
        """
        if room_id not in self.rooms:
            self.rooms[room_id] = set()
        
        self.rooms[room_id].add(user_id)
        
        # Notify room members
        await self.broadcast_to_room(
            room_id,
            json.dumps({
                "type": "user_joined",
                "room_id": room_id,
                "user_id": user_id,
                "timestamp": datetime.utcnow().isoformat()
            }),
            exclude_user=user_id
        )
        
    async def leave_room(self, room_id: str, user_id: int):
        """
        Remove user from a room
        """
        if room_id in self.rooms and user_id in self.rooms[room_id]:
            self.rooms[room_id].remove(user_id)
            
            if not self.rooms[room_id]:
                del self.rooms[room_id]
            else:
                # Notify remaining room members
                await self.broadcast_to_room(
                    room_id,
                    json.dumps({
                        "type": "user_left",
                        "room_id": room_id,
                        "user_id": user_id,
                        "timestamp": datetime.utcnow().isoformat()
                    })
                )
                
    async def send_notification(
        self,
        user_id: int,
        notification_type: str,
        title: str,
        message: str,
        data: Optional[Dict[str, Any]] = None,
        db: Optional[Session] = None
    ):
        """
        Send real-time notification to user
        """
        notification_data = {
            "type": "notification",
            "notification_type": notification_type,
            "title": title,
            "message": message,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send via WebSocket if user is online
        if user_id in self.active_connections:
            await self.send_json_to_user(notification_data, user_id)
        
        # Store in database for offline delivery
        if db:
            notification = Notification(
                user_id=user_id,
                type=notification_type,
                title=title,
                message=message,
                metadata=data
            )
            db.add(notification)
            db.commit()
            
    async def send_pending_notifications(self, websocket: WebSocket, user_id: int):
        """
        Send all unread notifications when user connects
        """
        # This would fetch from database
        # For now, sending a welcome notification
        welcome_data = {
            "type": "notification",
            "notification_type": "system",
            "title": "Welcome Back!",
            "message": "You have successfully connected to EUREKA",
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await websocket.send_text(json.dumps(welcome_data))
        
    async def broadcast_presence_update(self, user_id: int, status: str):
        """
        Broadcast user presence update to relevant users
        """
        presence_data = {
            "type": "presence_update",
            "user_id": user_id,
            "status": status,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to all users (in production, send only to friends/contacts)
        await self.broadcast(json.dumps(presence_data), exclude_user=user_id)
        
    async def handle_chat_message(
        self,
        sender_id: int,
        recipient_id: int,
        message: str,
        db: Session
    ):
        """
        Handle direct chat message between users
        """
        chat_data = {
            "type": "chat_message",
            "sender_id": sender_id,
            "recipient_id": recipient_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Send to recipient if online
        await self.send_json_to_user(chat_data, recipient_id)
        
        # Store in database
        # This would save to a chat_messages table
        
        # Send delivery confirmation to sender
        confirmation = {
            "type": "message_delivered",
            "message_id": "generated_id",
            "timestamp": datetime.utcnow().isoformat()
        }
        await self.send_json_to_user(confirmation, sender_id)
        
    async def handle_course_chat(
        self,
        course_id: int,
        user_id: int,
        message: str,
        db: Session
    ):
        """
        Handle course discussion/chat
        """
        room_id = f"course_{course_id}"
        
        chat_data = {
            "type": "course_chat",
            "course_id": course_id,
            "user_id": user_id,
            "message": message,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        # Broadcast to all users in the course room
        await self.broadcast_to_room(room_id, json.dumps(chat_data), exclude_user=user_id)
        
    async def send_learning_update(
        self,
        user_id: int,
        course_id: int,
        progress: float,
        lesson_completed: Optional[str] = None
    ):
        """
        Send learning progress update
        """
        update_data = {
            "type": "learning_update",
            "course_id": course_id,
            "progress": progress,
            "lesson_completed": lesson_completed,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.send_json_to_user(update_data, user_id)
        
    async def broadcast_instructor_announcement(
        self,
        course_id: int,
        instructor_id: int,
        announcement: str
    ):
        """
        Broadcast announcement from instructor to all enrolled students
        """
        room_id = f"course_{course_id}"
        
        announcement_data = {
            "type": "instructor_announcement",
            "course_id": course_id,
            "instructor_id": instructor_id,
            "announcement": announcement,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        await self.broadcast_to_room(room_id, json.dumps(announcement_data))
        
    async def handle_live_session(
        self,
        session_id: str,
        action: str,
        user_id: int,
        data: Optional[Dict[str, Any]] = None
    ):
        """
        Handle live session events (for live classes)
        """
        session_data = {
            "type": "live_session",
            "session_id": session_id,
            "action": action,  # join, leave, raise_hand, chat, etc.
            "user_id": user_id,
            "data": data or {},
            "timestamp": datetime.utcnow().isoformat()
        }
        
        room_id = f"session_{session_id}"
        await self.broadcast_to_room(room_id, json.dumps(session_data))


# Global connection manager instance
manager = ConnectionManager()


# WebSocket endpoint
async def websocket_endpoint(
    websocket: WebSocket,
    user: User = Depends(get_current_user_ws),
    db: Session = Depends(get_db)
):
    """
    Main WebSocket endpoint for real-time features
    """
    if not user:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return
        
    await manager.connect(websocket, user.id)
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            
            try:
                message = json.loads(data)
                message_type = message.get("type")
                
                # Handle different message types
                if message_type == "ping":
                    # Heartbeat
                    await websocket.send_text(json.dumps({"type": "pong"}))
                    
                elif message_type == "chat":
                    # Direct chat message
                    await manager.handle_chat_message(
                        sender_id=user.id,
                        recipient_id=message.get("recipient_id"),
                        message=message.get("message"),
                        db=db
                    )
                    
                elif message_type == "course_chat":
                    # Course discussion
                    await manager.handle_course_chat(
                        course_id=message.get("course_id"),
                        user_id=user.id,
                        message=message.get("message"),
                        db=db
                    )
                    
                elif message_type == "join_room":
                    # Join a room (course, session, etc.)
                    room_id = message.get("room_id")
                    await manager.join_room(room_id, user.id)
                    
                elif message_type == "leave_room":
                    # Leave a room
                    room_id = message.get("room_id")
                    await manager.leave_room(room_id, user.id)
                    
                elif message_type == "typing":
                    # Typing indicator
                    recipient_id = message.get("recipient_id")
                    typing_data = {
                        "type": "typing_indicator",
                        "user_id": user.id,
                        "is_typing": message.get("is_typing", True)
                    }
                    await manager.send_json_to_user(typing_data, recipient_id)
                    
                elif message_type == "live_session":
                    # Live session interaction
                    await manager.handle_live_session(
                        session_id=message.get("session_id"),
                        action=message.get("action"),
                        user_id=user.id,
                        data=message.get("data")
                    )
                    
                else:
                    # Unknown message type
                    error_response = {
                        "type": "error",
                        "message": f"Unknown message type: {message_type}"
                    }
                    await websocket.send_text(json.dumps(error_response))
                    
            except json.JSONDecodeError:
                error_response = {
                    "type": "error",
                    "message": "Invalid JSON format"
                }
                await websocket.send_text(json.dumps(error_response))
                
    except WebSocketDisconnect:
        await manager.disconnect(websocket, user.id)
    except Exception as e:
        print(f"WebSocket error for user {user.id}: {str(e)}")
        await manager.disconnect(websocket, user.id)