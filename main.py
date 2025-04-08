# main.py
from dotenv import load_dotenv
import os
from ai_forum.chatbot import ChatBot
from ai_forum.personality_manager import PersonalityManager
from ai_forum.relationship_manager import RelationshipManager
import json
import shutil
from ai_forum.autonomous_chat import AutonomousChat
from openai import OpenAI
from ai_forum.group_chat import GroupChat
from ai_forum import ResearchChat
from ai_forum.chat_interface import ChatInterface
from ai_forum.prompt_manager import PromptManager
from ai_forum.personality_updater import PersonalityUpdater
from ai_forum.chat_utils import ChatUtils

def remove_user_relationship_dynamics():
    """Remove relationship dynamics and core identity from all user personalities."""
    personality_manager = PersonalityManager()
    users_dir = os.path.join(personality_manager.base_dir, "users")
    
    if not os.path.exists(users_dir):
        return
        
    for user_name in os.listdir(users_dir):
        user_dir = os.path.join(users_dir, user_name)
        if os.path.isdir(user_dir):
            # Remove social-dynamics.json if it exists
            social_dynamics_file = os.path.join(user_dir, "social-dynamics.json")
            if os.path.exists(social_dynamics_file):
                os.remove(social_dynamics_file)
                print(f"Removed social-dynamics.json from {user_name}")
            
            # Remove core-identity.json if it exists
            core_identity_file = os.path.join(user_dir, "core-identity.json")
            if os.path.exists(core_identity_file):
                os.remove(core_identity_file)
                print(f"Removed core-identity.json from {user_name}")
            
            # Remove relationships directory if it exists
            relationships_dir = os.path.join(user_dir, "relationships")
            if os.path.exists(relationships_dir):
                shutil.rmtree(relationships_dir)
                print(f"Removed relationships directory from {user_name}")

def cleanup_workspace():
    """Clean up workspace by moving legacy directories and ensuring proper structure."""
    personality_manager = PersonalityManager()
    base_dir = personality_manager.base_dir
    
    # Ensure proper directory structure exists
    os.makedirs(os.path.join(base_dir, "ai"), exist_ok=True)
    os.makedirs(os.path.join(base_dir, "users"), exist_ok=True)
    
    # Remove relationship dynamics from users
    remove_user_relationship_dynamics()
    
    # Remove relationships directory from ai directory if it exists
    ai_relationships_dir = os.path.join(base_dir, "ai", "relationships")
    if os.path.exists(ai_relationships_dir):
        shutil.rmtree(ai_relationships_dir)
        print("Removed relationships directory from ai directory")
    
    # Move legacy AI personalities to ai directory
    for item in os.listdir(base_dir):
        if item not in ["ai", "users"]:  # Skip the new directories
            item_path = os.path.join(base_dir, item)
            if os.path.isdir(item_path):
                # Check if it's a user or AI personality
                if os.path.exists(os.path.join(item_path, "is_user")):
                    # Move to users directory
                    target_path = os.path.join(base_dir, "users", item)
                    if not os.path.exists(target_path):
                        shutil.move(item_path, target_path)
                        print(f"Moved user personality {item} to users directory")
                else:
                    # Move to ai directory
                    target_path = os.path.join(base_dir, "ai", item)
                    if not os.path.exists(target_path):
                        shutil.move(item_path, target_path)
                        print(f"Moved AI personality {item} to ai directory")
    
    # Ensure relationships directory exists for all AI personalities
    ai_dir = os.path.join(base_dir, "ai")
    for ai_name in os.listdir(ai_dir):
        ai_path = os.path.join(ai_dir, ai_name)
        if os.path.isdir(ai_path):
            relationships_dir = os.path.join(ai_path, "relationships")
            if not os.path.exists(relationships_dir):
                os.makedirs(relationships_dir)
                print(f"Created relationships directory for {ai_name}")
            
            # Initialize relationship with all other AIs and users
            relationship_manager = RelationshipManager(ai_path)
            
            # Create relationships with other AIs
            for other_ai in os.listdir(ai_dir):
                if other_ai != ai_name:
                    relationship_file = relationship_manager.get_relationship_file(other_ai)
                    if not os.path.exists(relationship_file):
                        relationship_manager.save_relationship(other_ai, relationship_manager._create_blank_relationship(other_ai))
            
            # Create relationships with all users
            users_dir = os.path.join(base_dir, "users")
            for user_name in os.listdir(users_dir):
                relationship_file = relationship_manager.get_relationship_file(user_name)
                if not os.path.exists(relationship_file):
                    relationship_manager.save_relationship(user_name, relationship_manager._create_blank_relationship(user_name))

def setup_api_key():
    """Ensure OpenAI API key is set up."""
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("\nOpenAI API key not found in environment variables.")
        print("You can get your API key from: https://platform.openai.com/api-keys")
        print("Please enter your OpenAI API key:")
        api_key = input("> ").strip()
        os.environ['OPENAI_API_KEY'] = api_key
        
        # Optionally save to .env file
        save = input("\nWould you like to save this API key to .env file? (y/n): ").lower()
        if save == 'y':
            with open(".env", "a") as f:
                f.write(f"\nOPENAI_API_KEY={api_key}\n")
            print("API key saved to .env file!")

def migrate_existing_personalities():
    """Migrate existing personalities to the new directory structure."""
    personality_manager = PersonalityManager()
    old_dir = personality_manager.base_dir
    ai_dir = os.path.join(old_dir, "ai")
    users_dir = os.path.join(old_dir, "users")
    
    # Create new directories if they don't exist
    os.makedirs(ai_dir, exist_ok=True)
    os.makedirs(users_dir, exist_ok=True)
    
    # Move existing personalities
    if os.path.exists(old_dir):
        for item in os.listdir(old_dir):
            if item not in ["ai", "users"]:  # Skip the new directories
                item_path = os.path.join(old_dir, item)
                if os.path.isdir(item_path):
                    # Check if it's a user or AI personality
                    if os.path.exists(os.path.join(item_path, "is_user")):
                        shutil.move(item_path, os.path.join(users_dir, item))
                    else:
                        shutil.move(item_path, os.path.join(ai_dir, item))

def check_existing_user(name):
    """Check if user exists in users directory."""
    personality_manager = PersonalityManager()
    users_dir = os.path.join(personality_manager.base_dir, "users", name)
    
    if os.path.exists(users_dir):
        return True
    return False

def get_available_personalities():
    """Get list of available AI personalities from my-personality/ai directory."""
    personality_manager = PersonalityManager()
    ai_dir = os.path.join(personality_manager.base_dir, "ai")
    personalities = []
    
    if os.path.exists(ai_dir):
        personalities = [d for d in os.listdir(ai_dir) 
                        if os.path.isdir(os.path.join(ai_dir, d))]
    
    return personalities

def setup_relationships(personalities):
    """Create relationship directories and initial relationship data for all personality pairs."""
    personality_manager = PersonalityManager()
    relationship_manager = RelationshipManager(personality_manager.base_dir)
    
    # Create relationship data template
    relationship_data = {
        "previous_interactions": [],
        "observed_traits": [],
        "trust_level": 0.5,
        "relationship_status": "acquaintance"
    }
    
    # Create relationships between all personality pairs
    for person1 in personalities:
        for person2 in personalities:
            if person1 != person2:
                # Use the personality directory as base for relationships
                rel_dir = os.path.join(personality_manager.base_dir, "ai", person1, "relationships", person2)
                if not os.path.exists(rel_dir):
                    os.makedirs(rel_dir)
                    # Save relationship data for both directions
                    relationship_manager.save_relationship(person1, relationship_data)
                    relationship_manager.save_relationship(person2, relationship_data)
                    print(f"Created {person1}-{person2} relationship")

def create_user_personality(name):
    """Create a new user personality with default structure or load existing one."""
    personality_manager = PersonalityManager()
    user_dir = os.path.join(personality_manager.base_dir, "users", name)
    
    if os.path.exists(user_dir):
        print(f"\nLoading existing personality for {name}")
        return True
    
    # Create new personality if it doesn't exist
    os.makedirs(user_dir)
    
    # Create is_user marker file
    with open(os.path.join(user_dir, "is_user"), "w") as f:
        f.write("")
        
    print(f"\nCreated new personality for {name}")
    return True

def select_personality(personalities, prompt):
    """Let user select a personality from the available list."""
    while True:
        print(f"\n{prompt}")
        for i, name in enumerate(personalities, 1):
            print(f"{i}. {name}")
        
        try:
            choice = int(input("\nEnter your choice (number): "))
            if 1 <= choice <= len(personalities):
                return personalities[choice - 1]
            print("Invalid choice. Please try again.")
        except ValueError:
            print("Please enter a valid number.")

def load_personality(personality_dir: str) -> ChatBot:
    """Load a personality from a directory."""
    personality_name = os.path.basename(personality_dir)
    # Create the ChatBot instance with just the required parameters
    bot = ChatBot(personality_name=personality_name, personality_dir=personality_dir)
    return bot

def main():
    """Main entry point for the application."""
    interface = ChatInterface()
    interface.main()

if __name__ == "__main__":
    main()