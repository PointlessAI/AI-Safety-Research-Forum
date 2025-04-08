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
        
        # Add interests and values
        self._add_interests_values(prompt_parts)
        
        # Add emotional framework
        self._add_emotional_framework(prompt_parts)
        
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
            
    def _add_interests_values(self, prompt_parts: List[str]) -> None:
        """Add interests and values to prompt parts."""
        interests_values_path = os.path.join(self.personality_manager.personality_dir, "interests-values.json")
        try:
            with open(interests_values_path, 'r') as f:
                interests_values = json.load(f)
                prompt_parts.extend([
                    "\n=== INTERESTS AND VALUES ===",
                    "These are your interests, values, and preferences.",
                    json.dumps(interests_values, indent=2)
                ])
        except Exception as e:
            print(f"Error reading interests and values: {e}")
            
    def _add_emotional_framework(self, prompt_parts: List[str]) -> None:
        """Add emotional framework to prompt parts."""
        emotional_framework_path = os.path.join(self.personality_manager.personality_dir, "emotional-framework.json")
        try:
            with open(emotional_framework_path, 'r') as f:
                emotional_framework = json.load(f)
                prompt_parts.extend([
                    "\n=== EMOTIONAL FRAMEWORK ===",
                    "This is your emotional framework and response patterns.",
                    json.dumps(emotional_framework, indent=2)
                ])
        except Exception as e:
            print(f"Error reading emotional framework: {e}")