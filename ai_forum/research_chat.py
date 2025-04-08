import time
import json
import os
import shutil
import random
from typing import List, Dict, Optional
from datetime import datetime
from .chatbot import ChatBot
from dotenv import load_dotenv
from openai import OpenAI

class ResearchChat:
    def __init__(self, mode: str = "general", delay: float = 2.0):
        """Initialize the chat with a specified mode and delay between messages.
        
        Args:
            mode (str): Either "general" for regular chat or "research" for research collaboration
            delay (float): Delay between messages in seconds
        """
        if mode not in ["general", "research"]:
            raise ValueError("Mode must be either 'general' or 'research'")
            
        self.mode = mode
        self.delay = delay
        self.participants: List[ChatBot] = []
        self.conversation_history: List[Dict] = []
        self.chat_file = None
        self.research_file = "research.json" if mode == "research" else None
        
        # Initialize OpenAI client
        load_dotenv()
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            raise ValueError("OpenAI API key not found in environment variables or .env file")
        self.client = OpenAI(
            api_key=api_key,
            base_url="https://api.openai.com/v1"  # Add the correct base URL
        )
        
        # Initialize or load research project if in research mode
        if self.mode == "research":
            self._load_research_project()

    def _load_research_project(self) -> None:
        """Load existing research project or create new one."""
        if os.path.exists(self.research_file):
            with open(self.research_file, "r") as f:
                self.research_project = json.load(f)
        else:
            self.research_project = {
                "title": "Research Project",
                "description": "",
                "objectives": [],
                "findings": [],
                "conclusions": [],
                "next_steps": [],
                "last_updated": datetime.now().isoformat()
            }
            self._save_research_project()

    def _save_research_project(self) -> None:
        """Save the current state of the research project."""
        if self.mode == "research":
            self.research_project["last_updated"] = datetime.now().isoformat()
            with open(self.research_file, "w") as f:
                json.dump(self.research_project, f, indent=2)

    def add_participant(self, bot: ChatBot) -> bool:
        """Add a participant to the chat."""
        if len(self.participants) >= 5:
            print("❌ Maximum number of participants (5) reached")
            return False
        if bot in self.participants:
            print(f"❌ {bot.name} is already in the chat")
            return False
            
        # Ensure the bot's personality directory is in the ai folder
        ai_dir = os.path.join(bot.personality_manager.base_dir, "ai")
        bot_dir = os.path.join(ai_dir, bot.name)
        
        # Create the ai directory if it doesn't exist
        os.makedirs(ai_dir, exist_ok=True)
        
        # If the bot's directory exists outside ai, move it
        old_dir = os.path.join(bot.personality_manager.base_dir, bot.name)
        if os.path.exists(old_dir) and not os.path.exists(bot_dir):
            shutil.move(old_dir, bot_dir)
            print(f"✅ Moved {bot.name}'s personality to ai directory")
            
        self.participants.append(bot)
        print(f"✅ Added {bot.name} to the {'research team' if self.mode == 'research' else 'chat'}")
        return True

    def remove_participant(self, bot_name: str) -> bool:
        """Remove a participant from the chat."""
        for i, bot in enumerate(self.participants):
            if bot.name == bot_name:
                self.participants.pop(i)
                print(f"✅ Removed {bot_name} from the {'research team' if self.mode == 'research' else 'chat'}")
                return True
        print(f"❌ {bot_name} not found in the {'research team' if self.mode == 'research' else 'chat'}")
        return False

    def _create_context_message(self, speaker: ChatBot) -> str:
        """Create context message for the current speaker."""
        other_names = [bot.name for bot in self.participants if bot != speaker]
        
        if self.mode == "research":
            return f"""You are {speaker.name} participating in a research collaboration with {', '.join(other_names)}.
            Important:
            - Focus on contributing to the research project
            - Build upon previous findings and insights
            - Provide evidence-based contributions
            - Ask clarifying questions when needed
            - Suggest next steps for the research
            - Reference existing research findings
            - Maintain a professional and academic tone
            - Keep responses focused and relevant to the research
            - Avoid personal interactions or relationship building
            - Contribute to the collective research goals"""
        else:
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
            - Build upon the ongoing conversation naturally"""

    def _get_last_messages(self, count: int = 5) -> str:
        """Get the last few messages for context."""
        if not self.conversation_history:
            return "No previous messages."
        
        # Get the last 'count' messages
        recent_messages = self.conversation_history[-count:]
        
        # Format messages with timestamps and speaker names
        formatted_messages = []
        for msg in recent_messages:
            timestamp = datetime.fromisoformat(msg['timestamp']).strftime('%H:%M:%S')
            formatted_messages.append(f"[{timestamp}] {msg['speaker']}: {msg['message']}")
        
        return "\n".join(formatted_messages)

    def _save_conversation(self) -> None:
        """Save the current conversation to a file."""
        if not self.chat_file:
            # Create a filename based on timestamp and mode
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            prefix = "research_chat" if self.mode == "research" else "chat"
            self.chat_file = f"{prefix}_{timestamp}.json"
            
        # Save conversation history with metadata
        data = {
            "mode": self.mode,
            "participants": [bot.name for bot in self.participants],
            "start_time": self.conversation_history[0]["timestamp"] if self.conversation_history else datetime.now().isoformat(),
            "messages": self.conversation_history
        }
        
        if self.mode == "research":
            data["research_project"] = self.research_project["title"]
        
        with open(self.chat_file, "w") as f:
            json.dump(data, f, indent=2)

    def _get_random_lengths(self) -> tuple[int, int]:
        """Get random token and word lengths for the response."""
        token_length = random.randint(50, 500)
        word_length = random.randint(10, 100)
        return token_length, word_length

    def start(self):
        """Start the research chat session."""
        print("\n=== Research Discussion Forum ===")
        print("Loading team members...")
        
        # Load all team members
        team_members = []
        for bot in self.participants:
            try:
                # Load personality from ai directory
                personality_dir = os.path.join("my-personality", "ai", bot.name)
                if not os.path.exists(personality_dir):
                    print(f"❌ Error: Personality directory not found for {bot.name}")
                    continue
                
                # Load core identity and work files
                core_identity_path = os.path.join(personality_dir, "core-identity.json")
                work_path = os.path.join(personality_dir, "work.json")
                
                if not os.path.exists(core_identity_path) or not os.path.exists(work_path):
                    print(f"❌ Error: Required files not found for {bot.name}")
                    continue
                
                with open(core_identity_path, 'r') as f:
                    core_identity = json.load(f)
                
                with open(work_path, 'r') as f:
                    work = json.load(f)
                
                team_members.append({
                    "name": bot.name,
                    "core_identity": core_identity,
                    "work": work
                })
                print(f"✅ Loaded {bot.name}")
                
            except Exception as e:
                print(f"❌ Error loading {bot.name}: {e}")
        
        if not team_members:
            print("❌ No team members could be loaded")
            return

        # Load research.md content
        try:
            with open("research.md", "r") as f:
                research_content = f.read()
        except Exception as e:
            print(f"Error loading research.md: {e}")
            return

        # Create initial report
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_file = f"discussion_forum_{timestamp}.md"
        
        with open(report_file, "w") as f:
            f.write(f"# Discussion Forum - {timestamp}\n\n")
            f.write("## Topic\n\n")
            f.write(f"{research_content}\n\n")
            f.write("## Discussion Thread\n\n")
        
        print("\nStarting forum discussion...")
        print("Press Ctrl+C to stop the discussion")
        
        turn_counter = 0
        while True:
            try:
                # Get current speaker
                current_speaker = self.participants[turn_counter % len(self.participants)]
                
                # Get random lengths for this response
                token_length, word_length = self._get_random_lengths()
                
                # Get context for the current speaker
                context = self._create_context_message(current_speaker)
                recent_messages = self._get_last_messages()
                
                # Create messages for the API
                messages = [
                    {"role": "system", "content": context},
                    {"role": "user", "content": f"""Discussion Topic:
{research_content}

Recent Posts:
{recent_messages}

As {current_speaker.name}, make a focused contribution that:
- Builds upon previous points
- Makes clear assertions
- Challenges or supports previous statements
- Adds new evidence or perspective
- Advances the discussion

Important:
- Start your contribution with a variety of words (avoid starting with the same word as previous statements)
- Use different sentence structures
- Keep it detailed but concise
- Each sentence should directly address the recent discussion
- Ensure your sentences flow naturally together
- Aim for approximately {word_length} words per sentence"""}
                ]
                
                # Get response from the current speaker
                response = self.client.chat.completions.create(
                    model="gpt-4o-mini",
                    messages=messages,
                    max_tokens=token_length,
                    temperature=1.0
                )
                
                message = response.choices[0].message.content
                # Split into sentences and clean them
                sentences = [s.strip() for s in message.split('.') if s.strip()]
                
                # Process each sentence to match the target word length
                processed_sentences = []
                for sentence in sentences:
                    words = sentence.split()
                    if len(words) > word_length:
                        # If sentence is too long, trim it
                        processed_sentences.append(' '.join(words[:word_length]) + '...')
                    else:
                        processed_sentences.append(sentence)
                
                # Join the sentences back together
                message = '. '.join(processed_sentences) + '.'
                
                # Add message to conversation history
                self.conversation_history.append({
                    "speaker": current_speaker.name,
                    "message": message,
                    "timestamp": datetime.now().isoformat()
                })
                
                # Print the message
                print(f"\n{current_speaker.name}: {message}")
                
                # Append to report
                with open(report_file, "a") as f:
                    f.write(f"#### {current_speaker.name} - {datetime.now().strftime('%H:%M:%S')}\n\n")
                    f.write(f"{message}\n\n")
                
                # Increment turn counter
                turn_counter += 1
                
                # Add delay between messages
                time.sleep(self.delay)
                
            except KeyboardInterrupt:
                print("\nDiscussion ended by user")
                break
            except Exception as e:
                print(f"Error in discussion: {e}")
                break
        
        print(f"\nDiscussion saved to {report_file}")

    def _create_prompt(self, recent_messages: str) -> str:
        """Create the appropriate prompt based on the chat mode."""
        if self.mode == "research":
            return f"""Current Research Project:
Title: {self.research_project['title']}
Description: {self.research_project['description']}
Objectives: {', '.join(self.research_project['objectives'])}
Findings: {', '.join(self.research_project['findings'])}
Next Steps: {', '.join(self.research_project['next_steps'])}

Recent discussion:
{recent_messages}

Please contribute to the research project. Consider:
1. Building upon previous findings
2. Suggesting new research directions
3. Analyzing existing data
4. Proposing next steps
5. Asking relevant research questions

What would you like to contribute?"""
        else:
            return f"""Recent conversation:
{recent_messages}

Please respond to the ongoing conversation. Consider:
1. The context of previous messages
2. The natural flow of the discussion
3. Any specific topics or points that need addressing

What would you like to say?""" 