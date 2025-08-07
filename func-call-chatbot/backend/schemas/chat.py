"""
Chat-related Pydantic models for request/response validation.

This module defines the data models used for chat functionality, including
message structures, action buttons, and response formats.
"""

from pydantic import BaseModel
from typing import Optional, List


class ActionButton(BaseModel):
    """
    Model representing an action button in chat responses.
    
    Action buttons provide interactive options for users to select from,
    allowing for guided conversations and quick actions.
    """
    label: str
    """The display text for the action button"""
    value: str
    """The value that will be sent when the button is clicked"""


class ChatMessage(BaseModel):
    """
    Model for incoming chat messages from users.
    
    Represents the structure of messages sent by users to the chatbot,
    including optional session management.
    """
    message: str
    """The text message content from the user"""
    session_id: Optional[str] = None
    """Optional session identifier for maintaining conversation context"""


class ChatResponse(BaseModel):
    """
    Model for chatbot responses to users.
    
    Represents the structure of responses sent by the chatbot to users,
    including the response text, session management, and optional action buttons.
    """
    response: str
    """The text response content from the chatbot"""
    session_id: Optional[str] = None
    """Optional session identifier for maintaining conversation context"""
    action_buttons: Optional[List[ActionButton]] = None
    """Optional list of action buttons for user interaction"""