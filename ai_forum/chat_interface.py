import os
import json
from typing import List, Optional
from .chatbot import ChatBot
from .group_chat import GroupChat
from .research_chat import ResearchChat
from .personality_manager import PersonalityManager

class ChatInterface:
    def __init__(self):
        """Initialize the chat interface."""
        self.personality_manager = PersonalityManager()
        self.chat_bots: List[ChatBot] = []
        self.current_chat = None

    def main(self):
        """Main entry point for the chat interface."""
        print("\n=== AI Chat Interface ===")
        print("1. Start a group chat")
        print("2. Start a one-on-one chat")
        print("3. Research (Full Team Collaboration)")
        
        while True:
            try:
                choice = input("\nSelect an option (1, 2, or 3): ").strip()
                if choice not in ["1", "2", "3"]:
                    print("Please enter 1, 2, or 3")
                    continue
                break
            except KeyboardInterrupt:
                print("\nExiting...")
                return
        
        # Initialize chat with selected mode
        if choice == "3":
            print("\n=== Research Mode Selected ===")
            print("Initializing research team...")
            try:
                mode = "research"
                chat = ResearchChat(mode=mode)
            except Exception as e:
                print("Error initializing research mode. Please try again.")
                return
            
            # Load available personalities
            ai_dir = "my-personality/ai"
            personalities = [d for d in os.listdir(ai_dir) if os.path.isdir(os.path.join(ai_dir, d))]
            
            # Add all participants for research team
            print("\nAdding all participants to research team...")
            for personality in personalities:
                personality_dir = os.path.join(ai_dir, personality)
                try:
                    bot = load_personality(personality_dir)
                    if chat.add_participant(bot):
                        print(f"Added {bot.name} to the research team")
                    else:
                        print(f"Failed to add {personality}")
                except Exception as e:
                    print(f"Error loading {personality}: {str(e)}")
            
            # Start the research chat
            try:
                chat.start()
            except KeyboardInterrupt:
                print("\nResearch session ended by user")
            except Exception as e:
                print(f"Error: {e}")
        else:
            # Handle group chat or one-on-one chat
            print("\nThis feature is not implemented yet.")
            print("Please select option 3 for Research mode.")

def load_personality(personality_dir: str) -> ChatBot:
    """Load a personality from the specified directory."""
    # Extract the personality name from the directory path
    personality_name = os.path.basename(personality_dir)
    
    # Create the ChatBot instance with just the required parameters
    return ChatBot(personality_name=personality_name, personality_dir=personality_dir)

if __name__ == "__main__":
    chat_interface = ChatInterface()
    chat_interface.main() 