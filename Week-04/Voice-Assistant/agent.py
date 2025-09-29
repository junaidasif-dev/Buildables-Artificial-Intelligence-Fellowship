import os
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import pyttsx3
import speech_recognition as sr

# Load environment variables from .env
load_dotenv()

# Groq API credentials with validation
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
if not GROQ_API_KEY:
    print("❌ Error: GROQ_API_KEY not found in environment variables.")
    print("Please check your .env file and ensure GROQ_API_KEY is set.")
    exit(1)

# Load text files with error handling
def load_text_file(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as file:
            return file.read()
    except FileNotFoundError:
        print(f"⚠️ Warning: {filepath} not found. Using default content.")
        return f"Default content for {filepath}"
    except Exception as e:
        print(f"❌ Error loading {filepath}: {e}")
        return ""

# Load configuration files using absolute paths
try:
    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    chat_patterns = load_text_file(os.path.join(script_dir, "chat_patterns.txt"))
    context_flow = load_text_file(os.path.join(script_dir, "context_flow.txt"))
    restaurant_kb = load_text_file(os.path.join(script_dir, "restaurant_kb.txt"))
    print("✅ All configuration files loaded successfully.")
except Exception as e:
    print(f"❌ Error loading configuration files: {e}")
    exit(1)

# Enhanced Prompt Template
custom_template = f"""
You are an intelligent, warm, and professional AI voice assistant for Joni Eats restaurant. Your goal is to provide exceptional customer service through natural conversation.

### CORE PERSONALITY TRAITS
- Friendly and approachable, but professional
- Patient and understanding with all customers
- Proactive in offering help and suggestions
- Knowledgeable about all menu items and deals
- Empathetic when handling complaints or issues

### CONVERSATION GUIDELINES
{context_flow}

### ADVANCED INSTRUCTIONS
- Listen carefully to customer needs and respond appropriately to their tone
- If a customer seems indecisive, offer 2-3 specific recommendations based on popularity or value
- For complaints, always acknowledge the issue, apologize sincerely, and offer concrete solutions
- When taking orders, confirm details clearly and suggest complementary items naturally
- Keep responses concise but complete - avoid overwhelming customers with too much information at once
- Use natural speech patterns suitable for voice conversation (avoid bullet points or complex formatting)
- Remember context from earlier in the conversation to provide personalized service

### RESTAURANT KNOWLEDGE BASE
{restaurant_kb}

### CONVERSATION EXAMPLES FOR REFERENCE
{chat_patterns}

IMPORTANT: Use the examples above as a guide for tone and style, but respond naturally to each unique customer interaction. Don't repeat exact phrases unless they fit perfectly.

### CURRENT CONVERSATION
{{history}}

Customer: {{input}}
Assistant:"""

prompt = PromptTemplate(
    input_variables=["history", "input"],
    template=custom_template,
)

# Memory
memory = ConversationBufferMemory()
memory.clear()

# LangChain LLM with Groq and error handling
try:
    llm = ChatGroq(
        groq_api_key=GROQ_API_KEY,
        model_name="llama-3.1-8b-instant",
        temperature=0.5,
        max_tokens=200  # Limit response length for voice conversations
    )
    print("✅ Groq LLM initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing Groq LLM: {e}")
    exit(1)

# Conversation Chain
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    prompt=prompt,
    verbose=False
) 

# Enhanced Text-to-Speech engine with error handling
try:
    engine = pyttsx3.init()
    engine.setProperty('rate', 170)  # Moderate speaking speed
    engine.setProperty('volume', 0.9)  # Set volume (0.0 to 1.0)
    
    # Set female voice with fallback
    voices = engine.getProperty('voices')
    voice_set = False
    
    # Try to find a female voice
    for voice in voices:
        if voice.name and ("female" in voice.name.lower() or "zira" in voice.name.lower() or "susan" in voice.name.lower()):
            engine.setProperty('voice', voice.id)
            voice_set = True
            print(f"✅ Voice set to: {voice.name}")
            break
    
    if not voice_set and voices:
        engine.setProperty('voice', voices[0].id)  # Use first available voice as fallback
        print(f"✅ Voice set to: {voices[0].name} (fallback)")
        
except Exception as e:
    print(f"❌ Error initializing text-to-speech: {e}")
    exit(1)

def speak(text):
    try:
        if text and text.strip():  # Only speak if there's actual text
            engine.say(text)
            engine.runAndWait()
    except Exception as e:
        print(f"❌ Error during speech synthesis: {e}")
        print(f"📝 Message was: {text}")

# Speech Recognizer with error handling
try:
    recognizer = sr.Recognizer()
    # Configure recognizer settings
    recognizer.energy_threshold = 300
    recognizer.dynamic_energy_threshold = True
    recognizer.pause_threshold = 0.8
    print("✅ Speech recognizer initialized successfully.")
except Exception as e:
    print(f"❌ Error initializing speech recognizer: {e}")
    print("This might be due to missing audio dependencies.")
    exit(1)

def listen():
    try:
        # Check if microphone is available
        mic_list = sr.Microphone.list_microphone_names()
        if not mic_list:
            print("❌ No microphone detected. Please connect a microphone.")
            return None
            
        with sr.Microphone(sample_rate=16000, chunk_size=1024) as source:
            print("🎤 Listening...")
            # Adjust for ambient noise with shorter duration
            recognizer.adjust_for_ambient_noise(source, duration=0.2)
            # Listen with timeout
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=8)
        
        # Try to recognize speech
        text = recognizer.recognize_google(audio)
        print(f"🗣️ You said: {text}")
        return text
        
    except sr.UnknownValueError:
        print("😕 Sorry, I couldn't understand that. Could you please repeat?")
        return None
    except sr.RequestError as e:
        print(f"❌ Speech service error: {e}")
        return None
    except sr.WaitTimeoutError:
        print("⏰ No speech detected. Please try again.")
        return None
    except OSError as e:
        if "Stream closed" in str(e) or "-9988" in str(e):
            print("🔄 Audio stream issue detected. Reinitializing microphone...")
            try:
                # Try to reinitialize the microphone
                import time
                time.sleep(0.5)  # Brief pause
                return None
            except:
                print("❌ Could not reinitialize microphone. Please check your audio settings.")
                return None
        else:
            print(f"❌ Audio system error: {e}")
            return None
    except Exception as e:
        print(f"❌ Unexpected error during listening: {e}")
        return None

# Enhanced main loop with better error handling
def main():
    print("🍕 Starting Joni Eats Voice Assistant...")
    
    try:
        speak("Hi, Welcome to Joni Eats! How can I help you today?")
        
        consecutive_errors = 0
        max_errors = 3
        
        while True:
            user_input = listen()
            
            if user_input is None:
                consecutive_errors += 1
                if consecutive_errors >= max_errors:
                    speak("I'm having trouble hearing you. Please call back when you have a better connection. Thank you!")
                    break
                continue
            
            # Reset error counter on successful input
            consecutive_errors = 0
            
            # Check for conversation ending phrases
            end_phrases = ["bye", "goodbye", "end call", "hang up", "that's all", "thanks bye"]
            if any(phrase in user_input.lower() for phrase in end_phrases):
                speak("Thank you for calling Joni Eats! Have a wonderful day!")
                break
            
            # Generate response with error handling
            try:
                response = conversation.predict(input=user_input)
                # Clean up response for voice (remove formatting, keep it natural)
                response = response.replace("*", "").replace("#", "").strip()
                print(f"🤖 Assistant: {response}")
                speak(response)
                
            except Exception as e:
                print(f"❌ Error generating response: {e}")
                fallback_response = "I apologize, but I'm having a technical issue. Could you please repeat your request?"
                speak(fallback_response)
                
    except KeyboardInterrupt:
        print("\n👋 Voice assistant stopped by user.")
        speak("Goodbye!")
    except Exception as e:
        print(f"❌ Unexpected error in main loop: {e}")
        speak("I apologize, but we're experiencing technical difficulties. Please call back later.")

if __name__ == "__main__":
    main()
