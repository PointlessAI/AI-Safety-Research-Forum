# chatbot/prompt_manager.py
import os
import json
from typing import List, Dict

class PromptManager:
    def __init__(self, personality_manager: PersonalityManager):
        self.personality_manager = personality_manager
    
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