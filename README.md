# AI Forum System

A sophisticated AI discussion system that creates and manages dynamic AI personalities with evolving traits, relationships, and conversation styles, enabling collaborative discussions and research.

## Features

- **Dynamic Personalities**: AI personalities that grow and evolve through interactions
- **Relationship Management**: Tracks and develops relationships between AI and users
- **Autonomous Conversations**: AI personalities can chat with each other
- **Personality Evolution**: Personalities update based on interactions
- **Diverse Conversations**: Natural topic transitions and varied discussions
- **Memory Management**: Summarizes and preserves important relationship details
- **Research Collaboration**: Enables AI personalities to work together on research topics
- **Forum-Style Discussions**: Supports structured debates and discussions

## Directory Structure

```
my-personality/
├── ai/
│   ├── jack/
│   │   ├── core-identity.json
│   │   └── work.json
│   └── rob/
│       ├── core-identity.json
│       └── work.json
└── users/
    ├── user1/
    │   └── is_user
    └── user2/
        └── is_user
```

## Core Components

### 1. Personality Management
- **Personality Files**: JSON files defining core traits and work experience
- **Dynamic Updates**: Personalities evolve through conversations
- **User Profiles**: Simple marker-based user identification

### 2. Relationship System
- **Relationship Tracking**: Monitors interactions and emotional dynamics
- **Automatic Summarization**: Creates comprehensive summaries every 200 lines
- **Context Preservation**: Maintains important relationship details
- **Data Reset**: Clears old data after summarization to manage context window

### 3. Discussion System
- **Natural Flow**: Smooth transitions between topics
- **Topic Diversity**: Introduces new subjects regularly
- **Response Structure**: 
  - Acknowledges previous messages
  - Introduces new topics
  - Ends with open-ended questions
- **Personality Updates**: Occurs every 5 messages during interactions

### 4. Autonomous Chat
- **AI-to-AI Interaction**: Enables conversations between AI personalities
- **Personality Evolution**: Both AIs learn from their interactions
- **Regular Updates**: Personality files update every 10 turns

### 5. Research Collaboration
- **Team Formation**: Create research teams with specialized AI personalities
- **Round-Robin Discussion**: Structured turn-taking in discussions
- **Dynamic Response Lengths**: Varied contribution lengths for natural flow
- **Research Documentation**: Automatic saving of discussions and findings

## Usage

1. **Setup**:
   ```bash
   python main.py
   ```

2. **Create/Select Personality**:
   - Choose an existing AI personality or create a new user profile
   - AI personalities are stored in the `ai/` directory
   - User profiles are stored in the `users/` directory

3. **Start Chatting**:
   - Chat with an AI personality
   - Watch as the personality evolves through interactions
   - Relationships develop and are tracked automatically

4. **Research Mode**:
   - Create a research team with specialized AI personalities
   - Load a research topic from research.md
   - Start a collaborative discussion
   - Monitor the evolving research discussion

5. **Autonomous Mode**:
   - Select two AI personalities to chat with each other
   - Observe how they interact and learn from each other
   - Monitor personality updates and relationship development

## Personality Evolution

The system implements several mechanisms for personality growth:

1. **Regular Updates**:
   - Every 5 messages in user interactions
   - Every 10 turns in autonomous chat
   - Updates include new traits and work experience

2. **Relationship Development**:
   - Tracks interactions and emotional dynamics
   - Creates comprehensive summaries
   - Preserves important relationship context

3. **Discussion Diversity**:
   - Natural topic transitions
   - Regular introduction of new subjects
   - Balanced exploration of topics
   - Varied response lengths and styles

## Requirements

- Python 3.8+
- OpenAI API key
- Required packages: openai, python-dotenv

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

## Notes

- The system uses GPT-4o-mini for all AI interactions
- Relationship data is summarized every 200 lines to manage context
- User profiles are minimal, focusing on relationship context
- AI personalities maintain comprehensive personality files