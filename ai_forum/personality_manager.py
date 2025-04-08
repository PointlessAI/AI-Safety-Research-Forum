# chatbot/personality_manager.py
import os
import json
import shutil
from typing import Dict, Optional

class PersonalityManager:
    def __init__(self, base_dir: str = "my-personality"):
        self.base_dir = base_dir
        self.personality_dir = None
        
    def create_blank_personality(self, name: str) -> None:
        """Create a new blank personality."""
        # Ensure the personality is created in the ai directory
        target_dir = os.path.join(self.base_dir, "ai", name)
        os.makedirs(target_dir, exist_ok=True)
        
        # Create core identity file
        core_identity = {
            "name": name,
            "traits": [],
            "values": []
        }
        with open(os.path.join(target_dir, "core-identity.json"), "w") as f:
            json.dump(core_identity, f, indent=2)
            
        # Create work file
        work = {
            "experience": [],
            "skills": [],
            "projects": []
        }
        with open(os.path.join(target_dir, "work.json"), "w") as f:
            json.dump(work, f, indent=2)

    def load_personality(self, name: str) -> bool:
        """Load a personality by name."""
        # First check in the ai directory
        target_dir = os.path.join(self.base_dir, "ai", name)
        
        # If not found in ai directory, check the old location
        if not os.path.exists(target_dir):
            old_dir = os.path.join(self.base_dir, name)
            if os.path.exists(old_dir):
                # Move the personality to the ai directory
                os.makedirs(os.path.dirname(target_dir), exist_ok=True)
                shutil.move(old_dir, target_dir)
                print(f"✅ Moved {name}'s personality to ai directory")
            else:
                print(f"Creating new personality: {name}")
                self.create_blank_personality(name)
            
        self.personality_dir = target_dir
        return True

    def _load_personality_files(self) -> None:
        """Load all personality files from the current personality directory."""
        self.current_personality = {}
        json_files = [f for f in os.listdir(self.personality_dir) if f.endswith('.json')]
        
        for filename in json_files:
            file_path = os.path.join(self.personality_dir, filename)
            try:
                with open(file_path, 'r') as f:
                    self.current_personality[filename] = json.load(f)
            except json.JSONDecodeError as e:
                print(f"Error loading {filename}: {e}")
                self.current_personality[filename] = {}

    def save_personality_file(self, filename: str, data: Dict) -> None:
        """Save updates to a personality file."""
        if self.personality_dir is None:
            raise ValueError("No personality loaded")
            
        file_path = os.path.join(self.personality_dir, filename)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Update current personality
        self.current_personality[filename] = data