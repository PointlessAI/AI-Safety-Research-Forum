# chatbot/chat_utils.py
from typing import Dict

class ChatUtils:
    @staticmethod
    def create_welcome_message(name: str, user_profile: Dict, core_identity: Dict, emotional: Dict) -> str:
        """Create a personalized welcome message."""
        relationship = user_profile.get('relationship', {})
        trust_level = relationship.get('trust_level', 0.0)
        emotional_bond = relationship.get('emotional_bond', 0.0)
        
        if not name or name == 'the user':
            name = "sir"
            
        # Create welcome message based on relationship status
        if trust_level > 0.8 and emotional_bond > 0.8:
            return f"Hello {name}! It's wonderful to see you again. I've been looking forward to our conversation."
        elif trust_level > 0.5 and emotional_bond > 0.5:
            return f"Hi {name}! It's nice to chat with you again. How have you been?"
        else:
            return f"Hello {name}. I'm here to help. What would you like to discuss?"
            
    @staticmethod
    def format_message(message: str, speaker: str) -> str:
        """Format a message with speaker information."""
        return f"{speaker}: {message}"
        
    @staticmethod
    def get_timestamp() -> str:
        """Get current timestamp in ISO format."""
        from datetime import datetime
        return datetime.now().isoformat()
        
    @staticmethod
    def truncate_message(message: str, max_length: int = 100) -> str:
        """Truncate a message to a maximum length."""
        if len(message) > max_length:
            return message[:max_length] + "..."
        return message