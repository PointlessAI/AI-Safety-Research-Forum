# chatbot/prompt_manager.py
import os
import json
from typing import List, Dict, Optional
from datetime import datetime
from .personality_manager import PersonalityManager

class PromptManager:
    def __init__(self, personality_manager: PersonalityManager):
        """Initialize the prompt manager with a personality manager."""
        self.personality_manager = personality_manager
        self.prompt_dir = "prompts"
        self._ensure_prompt_dir()
    
    def _ensure_prompt_dir(self) -> None:
        """Ensure the prompt directory exists."""
        if not os.path.exists(self.prompt_dir):
            os.makedirs(self.prompt_dir)
    
    def create_prompt(self, prompt_name: str, content: str) -> None:
        """Create a new prompt file."""
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_name}.txt")
        with open(prompt_path, "w") as f:
            f.write(content)
    
    def get_prompt(self, prompt_name: str) -> Optional[str]:
        """Get the content of a prompt file."""
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_name}.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "r") as f:
                return f.read()
        return None
    
    def update_prompt(self, prompt_name: str, content: str) -> None:
        """Update an existing prompt file."""
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_name}.txt")
        if os.path.exists(prompt_path):
            with open(prompt_path, "w") as f:
                f.write(content)
    
    def delete_prompt(self, prompt_name: str) -> None:
        """Delete a prompt file."""
        prompt_path = os.path.join(self.prompt_dir, f"{prompt_name}.txt")
        if os.path.exists(prompt_path):
            os.remove(prompt_path)
    
    def list_prompts(self) -> List[str]:
        """List all available prompts."""
        if os.path.exists(self.prompt_dir):
            return [f[:-4] for f in os.listdir(self.prompt_dir) if f.endswith(".txt")]
        return []

    def get_prompt(self) -> str:
        """Get the complete prompt for the AI."""
        prompt_parts = []
        
        # Add core identity
        self._add_core_identity(prompt_parts)
        
        return "\n".join(prompt_parts)
    
    def _add_core_identity(self, prompt_parts: List[str]) -> None:
        """Add core identity to prompt parts."""
        core_identity_path = os.path.join(self.personality_manager.personality_dir, "core-identity.json")
        try:
            with open(core_identity_path, 'r') as f:
                core_identity = json.load(f)
                prompt_parts.extend([
                    "\n=== CORE IDENTITY ===",
                    "This is your core identity and personality traits.",
                    json.dumps(core_identity, indent=2)
                ])
        except Exception as e:
            print(f"Error reading core identity: {e}")