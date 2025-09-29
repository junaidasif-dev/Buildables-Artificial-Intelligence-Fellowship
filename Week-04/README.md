# Joni Eats Voice Assistant - Enhanced Version

## Overview
An intelligent voice assistant for Joni Eats restaurant powered by Groq AI, featuring natural conversation, comprehensive error handling, and professional customer service capabilities.

## Key Features

### 🎯 Enhanced Conversational AI
- **Advanced Prompt Engineering**: Multi-layered prompt with personality traits, conversation guidelines, and contextual awareness
- **Natural Response Generation**: Responses optimized for voice conversations with appropriate length and tone
- **Context Awareness**: Maintains conversation history for personalized interactions

### 🗣️ Improved Voice Capabilities
- **Robust Speech Recognition**: Google Speech Recognition with ambient noise adjustment and timeout handling
- **Professional Text-to-Speech**: Optimized voice settings with female voice preference and error recovery
- **Smart Audio Processing**: Handles audio issues gracefully with user-friendly error messages

### 🛡️ Comprehensive Error Handling
- **API Validation**: Checks for required environment variables on startup
- **File Loading**: Graceful handling of missing configuration files
- **Connection Resilience**: Manages speech recognition failures and network issues
- **Fallback Responses**: Provides helpful messages when technical issues occur

### 📚 Rich Conversation Patterns
Over 25 conversation examples covering:
- **Greetings & Welcome**: Natural conversation starters
- **Menu Inquiries**: Detailed product information and recommendations
- **Order Processing**: Step-by-step order taking with confirmations
- **Delivery & Payment**: Address collection and payment method handling
- **Complaints & Issues**: Professional problem resolution
- **Special Requests**: Customization and special accommodation handling

## Configuration Files

### `chat_patterns.txt`
Contains comprehensive conversation examples organized by scenario:
- Greeting & Welcome scenarios
- Menu inquiries and recommendations
- Order processing workflows
- Delivery and location handling
- Payment method discussions
- Deals and promotions
- Complaint resolution
- Special requests and customizations
- Natural conversation endings

### `context_flow.txt`
Defines conversation flow rules and guidelines

### `restaurant_kb.txt`
Complete restaurant knowledge base including menu, pricing, deals, and policies

## Technical Improvements

### Enhanced Error Handling
- API key validation on startup
- Configuration file loading with fallbacks
- Speech recognition timeout management
- Network connectivity error handling
- Graceful degradation for technical issues

### Optimized Performance
- Response length limits for voice conversations
- Ambient noise adjustment for better recognition
- Memory management with conversation buffers
- Efficient file loading and caching

### User Experience Enhancements
- Clear status messages and feedback
- Progressive error recovery (3 consecutive errors before timeout)
- Natural conversation ending detection
- Professional voice synthesis with fallback options

## Usage

### Prerequisites
- Python 3.12+ with virtual environment
- All dependencies installed via `requirements.txt`
- Groq API key configured in `.env` file
- Microphone and speakers/headphones

### Running the Assistant
```bash
# Activate virtual environment
.\.venv\Scripts\Activate.ps1

# Navigate to Voice-Assistant directory
cd Week-04\Voice-Assistant

# Run the assistant
python agent.py
```

### Voice Commands
The assistant recognizes natural speech and responds to:
- Menu inquiries ("What do you recommend?")
- Order placement ("I want to place an order")
- Delivery questions ("Do you deliver to my area?")
- Payment inquiries ("Can I pay with card?")
- Complaints ("My order was wrong")
- Conversation ending ("Thanks, bye!")

## Error Recovery
- **Speech Recognition Issues**: Assistant will ask you to repeat up to 3 times
- **Network Problems**: Provides fallback responses and suggests calling back
- **API Errors**: Graceful error messages with technical details in console
- **Audio Issues**: Clear instructions for troubleshooting

## Customization Options
- Modify `chat_patterns.txt` to add new conversation scenarios
- Adjust voice speed/volume in agent.py TTS settings
- Update restaurant information in `restaurant_kb.txt`
- Customize personality traits in the prompt template

## Troubleshooting
1. **No audio input**: Check microphone permissions and connectivity
2. **API errors**: Verify GROQ_API_KEY in .env file
3. **Import errors**: Ensure all dependencies are installed in virtual environment
4. **Voice issues**: Check speaker/headphone connectivity
