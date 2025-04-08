# chatbot/group_chat.py
import time
import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from .chatbot import ChatBot
from dotenv import load_dotenv
from openai import OpenAI

class GroupChat:
    def __init__(self, delay: float = 2.0):
        """Initialize the group chat with a delay between messages."""
        self.delay = delay
        self.participants: List[ChatBot] = []
        self.conversation_history: List[Dict] = []
        self.chat_file = None
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables or .env file")
        self.client = OpenAI(api_key=api_key)

    def add_participant(self, bot: ChatBot) -> bool:
        """Add a participant to the group chat."""
        if len(self.participants) >= 5:
            print("❌ Maximum number of participants (5) reached")
            return False
        if bot in self.participants:
            print(f"❌ {bot.name} is already in the chat")
            return False
        self.participants.append(bot)
        print(f"✅ Added {bot.name} to the chat")
        return True

    def remove_participant(self, bot_name: str) -> bool:
        """Remove a participant from the group chat."""
        for i, bot in enumerate(self.participants):
            if bot.name == bot_name:
                self.participants.pop(i)
                print(f"✅ Removed {bot_name} from the chat")
                return True
        print(f"❌ {bot_name} not found in the chat")
        return False

    def _create_context_message(self, speaker: ChatBot) -> str:
        """Create context message for the current speaker."""
        other_names = [bot.name for bot in self.participants if bot != speaker]
        return f"""You are {speaker.name} participating in a group chat with {', '.join(other_names)}.
        Important:
        - Respond naturally to what was just said
        - You can address specific people or the whole group
        - Let your personality shine through
        - React authentically to the content of messages
        - Feel free to change topics if it feels natural
        - Express emotions, thoughts, and opinions freely
        - Keep responses concise and engaging
        - Try to maintain a balanced conversation with all participants
        - Reference previous messages and topics when relevant
        - Build upon the ongoing conversation naturally
        - Pay close attention to recent questions asked by others
        - Do not repeat questions that were just asked by someone else
        - If someone already asked a question, either:
          a) Wait for the answer if it hasn't been given yet
          b) Add to the existing question with additional context
          c) Ask a related but different question
        - Be aware of the conversation flow and avoid redundant interactions"""

    def _get_last_messages(self, count: int = 10) -> str:
        """Get the last few messages for context."""
        if not self.conversation_history:
            return "No previous messages."
        return "\n".join([
            f"{msg['speaker']}: {msg['message']}"
            for msg in self.conversation_history[-count:]
        ])

    def _save_conversation(self) -> None:
        """Save the current conversation to a file."""
        if not self.chat_file:
            # Create a filename based on timestamp only
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            self.chat_file = f"chat_{timestamp}.json"
            
        # Save conversation history with metadata
        data = {
            "participants": [bot.name for bot in self.participants],
            "start_time": self.conversation_history[0]["timestamp"] if self.conversation_history else datetime.now().isoformat(),
            "messages": self.conversation_history
        }
        
        with open(self.chat_file, "w") as f:
            json.dump(data, f, indent=2)

    def _update_relationships(self, message: str, speaker: ChatBot) -> None:
        """Update relationships between the speaker and other participants."""
        for listener in self.participants:
            if listener != speaker:
                # Create conversation segment in the expected format
                conversation_segment = [
                    {
                        "speaker": speaker.name,
                        "listener": listener.name,
                        "message": message
                    }
                ]
                try:
                    speaker.relationship_manager.update_relationship(
                        listener.name,
                        conversation_segment
                    )
                except Exception as e:
                    print(f"Warning: Failed to update relationship between {speaker.name} and {listener.name}: {e}")

    def start(self) -> None:
        """Start the group chat with round-robin turn-taking."""
        if len(self.participants) < 2:
            print("❌ Need at least 2 participants to start the chat")
            return

        print("\n=== Group Chat Started ===")
        print(f"Participants: {', '.join(bot.name for bot in self.participants)}")
        print("Type 'quit' to end the chat\n")

        # Initialize turn counter
        turn_counter = 0
        
        while True:
            try:
                # Get current speaker based on turn counter
                current_speaker = self.participants[turn_counter % len(self.participants)]
                
                # Get context for the current speaker
                context = self._create_context_message(current_speaker)
                recent_messages = self._get_last_messages()
                
                # Create messages for the API
                messages = [
                    {"role": "system", "content": context},
                    {"role": "user", "content": f"""Recent conversation history:
{recent_messages}

Please respond to the ongoing conversation. Consider:
1. The context of previous messages
2. Your relationships with other participants
3. The natural flow of the discussion
4. Any specific topics or points that need addressing

What would you like to say?"""}
                ]
                
                # Get response from the current speaker
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=1000,
                    temperature=0.7
                )
                
                message = response.choices[0].message.content.strip()
                
                # Check if we should quit
                if message.lower() == 'quit':
                    break
                
                # Add message to history with timestamp
                self.conversation_history.append({
                    "speaker": current_speaker.name,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Save conversation after each message
                self._save_conversation()
                
                # Print the message
                print(f"\n{current_speaker.name}: {message}")
                
                # Update relationships
                self._update_relationships(message, current_speaker)
                
                # Increment turn counter for next round
                turn_counter += 1
                
                # Add delay between messages
                time.sleep(self.delay)
                
            except KeyboardInterrupt:
                print("\nChat ended by user")
                break
            except Exception as e:
                print(f"Error: {e}")
                break

        print("\n=== Group Chat Ended ===")
        # Final save of the conversation
        self._save_conversation() 