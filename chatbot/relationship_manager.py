import os
import json
import time
from typing import Dict, List, Optional
from openai import OpenAI
from dotenv import load_dotenv

class RelationshipManager:
    def __init__(self, personality_dir: str):
        # personality_dir should be the full path to the AI personality's directory
        self.personality_dir = personality_dir
        self.relationships_dir = os.path.join(self.personality_dir, "relationships")
        os.makedirs(self.relationships_dir, exist_ok=True)
        self.current_relationships = {}
        
        # Get the AI's name from the directory name
        self.name = os.path.basename(self.personality_dir)
        
        # Initialize OpenAI client
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables or .env file")
        self.client = OpenAI(api_key=api_key)

    def get_relationship_file(self, other_name: str) -> str:
        """Get the path to a relationship file for a specific person."""
        return os.path.join(self.relationships_dir, f"{other_name}.json")

    def load_relationship(self, other_name: str) -> Dict:
        """Load relationship data for a specific person."""
        file_path = self.get_relationship_file(other_name)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                return json.load(f)
        return self._create_blank_relationship(other_name)

    def _create_blank_relationship(self, other_name: str) -> Dict:
        """Create a blank relationship template."""
        return {
            "interactions": [],
            "observed_traits": [],
            "shared_experiences": [],
            "emotional_dynamics": {
                "positive_moments": [],
                "challenges": [],
                "trust_level": "neutral"
            },
            "communication_patterns": {
                "topics": [],
                "style": [],
                "frequency": "occasional"
            },
            "relationship_development": {
                "milestones": [],
                "current_status": "acquaintance",
                "growth_areas": []
            },
            "social_preferences": {
                "preferred_topics": [],
                "interaction_style": [],
                "boundaries": []
            },
            "interaction_history": {
                "recent_interactions": [],
                "key_moments": [],
                "conflicts": [],
                "resolutions": []
            }
        }

    def save_relationship(self, other_name: str, data: Dict) -> None:
        """Save relationship data for a specific person."""
        file_path = self.get_relationship_file(other_name)
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)

    def _summarize_relationship(self, data: Dict) -> str:
        """Create a comprehensive summary of the relationship."""
        system_prompt = f"""You are a relationship summarizer. Create a detailed summary of the relationship between {self.name} and the user.

The summary should include:
1. Key shared experiences and memories
2. Important conversations and topics discussed
3. Emotional dynamics and trust level
4. Communication patterns and preferences
5. Relationship milestones and current status
6. Notable interactions and their impact
7. Any significant challenges or positive moments

Format the summary as a natural narrative that captures the essence of the relationship. Include specific details and examples from the interaction history.

Make the summary detailed enough to preserve important memories and context, but concise enough to be useful for future interactions."""
        
        # Format the data for summarization
        summary_data = {
            "interactions": data.get("interactions", []),
            "shared_experiences": data.get("shared_experiences", []),
            "emotional_dynamics": data.get("emotional_dynamics", {}),
            "communication_patterns": data.get("communication_patterns", {}),
            "relationship_development": data.get("relationship_development", {}),
            "interaction_history": data.get("interaction_history", {})
        }
        
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Summarize this relationship data:\n\n{json.dumps(summary_data, indent=2)}"}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            max_tokens=500,  # Increased token limit for more detailed summaries
            temperature=0.7
        )
        
        return response.choices[0].message.content.strip()

    def update_relationship(self, other_name: str, conversation_segment: List[Dict]) -> None:
        """Update relationship with another AI based on conversation."""
        relationship_file = os.path.join(self.relationships_dir, f"{other_name}.json")
        
        # Load existing relationship or create new one
        if os.path.exists(relationship_file):
            with open(relationship_file, "r") as f:
                relationship = json.load(f)
        else:
            relationship = self._create_blank_relationship(other_name)
            
        # Add new interaction with timestamp
        for interaction in conversation_segment:
            new_interaction = {
                "speaker": interaction["speaker"],
                "listener": interaction["listener"],
                "message": interaction["message"],
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
            
            # Ensure interactions list exists
            if "interactions" not in relationship:
                relationship["interactions"] = []
            relationship["interactions"].append(new_interaction)
            
            # Ensure interaction_history exists
            if "interaction_history" not in relationship:
                relationship["interaction_history"] = {
                    "recent_interactions": [],
                    "key_moments": [],
                    "conflicts": [],
                    "resolutions": []
                }
            
            # Update interaction history
            relationship["interaction_history"]["recent_interactions"].append(
                f"{interaction['speaker']} said: {interaction['message']}"
            )
            
            # Keep only the last 10 recent interactions
            if len(relationship["interaction_history"]["recent_interactions"]) > 10:
                relationship["interaction_history"]["recent_interactions"] = relationship["interaction_history"]["recent_interactions"][-10:]
        
        # Save updated relationship
        with open(relationship_file, "w") as f:
            json.dump(relationship, f, indent=2)
            
    def get_relationship_summary(self, other_name: str) -> Dict:
        """Get summary of relationship with another AI."""
        relationship_file = os.path.join(self.relationships_dir, f"{other_name}.json")
        
        if not os.path.exists(relationship_file):
            return {
                "interaction_count": 0,
                "topics_discussed": [],
                "emotional_dynamics": []
            }
            
        with open(relationship_file, "r") as f:
            relationship = json.load(f)
            
        return {
            "interaction_count": len(relationship["interactions"]),
            "topics_discussed": relationship["topics_discussed"],
            "emotional_dynamics": relationship["emotional_dynamics"]
        }

    def _merge_relationship_data(self, current_data: Dict, new_data: Dict) -> Dict:
        """Merge new relationship data with current data."""
        for key, value in new_data.items():
            if isinstance(value, dict):
                if key not in current_data:
                    current_data[key] = {}
                current_data[key] = self._merge_relationship_data(current_data[key], value)
            elif isinstance(value, list):
                if key not in current_data:
                    current_data[key] = []
                current_data[key].extend(item for item in value if item not in current_data[key])
            else:
                current_data[key] = value
        return current_data 