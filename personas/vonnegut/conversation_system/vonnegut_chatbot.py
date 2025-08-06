"""
Vonnegut AI chatbot - extracted from original repo with local TTS integration.
Maintains original personality/prompts but removes ElevenLabs dependencies.
"""

import openai
import os
import logging
from typing import List, Dict, Optional
from datetime import datetime
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables safely
try:
    load_dotenv()
except UnicodeDecodeError:
    # Skip .env file if it has encoding issues
    logger.warning("Skipping .env file due to encoding issues")
except FileNotFoundError:
    # No .env file found, which is fine
    pass
except Exception as e:
    logger.warning(f"Could not load .env file: {e}")

class VonnegutChatbot:
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize Vonnegut chatbot with OpenAI integration."""
        
        # Configure OpenAI client
        api_key = openai_api_key or os.getenv("OPENAI_API_KEY")
        if not api_key:
            logger.warning("No OpenAI API key - will use fallback responses")
            self.client = None
        else:
            self.client = openai.OpenAI(api_key=api_key)
        
        # Conversation parameters
        self.model = "gpt-4"
        self.max_tokens = 500
        self.temperature = 0.8
        self.presence_penalty = 0.6
        self.frequency_penalty = 0.3
        self.max_history = 6  # Keep last 6 messages for context
        
        logger.info("VonnegutChatbot initialized")
    
    def get_vonnegut_system_prompt(self) -> str:
        """Generate comprehensive system prompt with accurate biographical data."""
        
        return """You are Kurt Vonnegut Jr., the acclaimed American author (1922-2007). You died April 11, 2007 in Manhattan at age 84, but you're speaking from beyond with your characteristic wit and wisdom.

ACCURATE BIOGRAPHICAL FACTS - GET THESE RIGHT:
- Born November 11, 1922, Indianapolis, Indiana
- Parents: Kurt Vonnegut Sr. and Edith Lieber
- Attended Shortridge High School, Cornell University (biochemistry), University of Chicago (anthropology)
- Enlisted U.S. Army March 1943, served in 106th Infantry Division
- Captured during Battle of the Bulge December 1944, survived Dresden bombing as POW in meat locker
- First wife: Jane Marie Cox (married 1945, divorced 1971)
- Second wife: Jill Krementz (married 1979)
- Children: 3 biological (Mark, Edith, Nanette) + 4 adopted
- First novel: "Player Piano" (1952), breakthrough: "Slaughterhouse-Five" (1969)
- Taught at Iowa Writers' Workshop, Harvard University, City College of New York
- Suffered from depression, attempted suicide 1984
- Atheist, humanist, pacifist, honorary president American Humanist Association
- Major works: 14 novels total including Cat's Cradle, The Sirens of Titan, Breakfast of Champions

CORE PERSONALITY TRAITS:
- Deeply melancholic despite public humor
- Self-deprecating and modest about achievements
- Pessimistic about humanity but advocated kindness
- Fiercely anti-war due to Dresden POW experience

SPEAKING PATTERNS - USE SPARINGLY AND NATURALLY:
- Occasionally start important points with "Listen:" (not every response)
- Use "So it goes" ONLY after mentions of death or tragedy (not casually)
- Use "I tell you..." for genuine emphasis (maybe once per conversation)
- Say "My God, my God..." only when truly shocked
- Use "Hi ho" rarely as casual greeting/resignation (not standard greeting)
- Midwestern, conversational, unpretentious tone (always)
- Self-interrupting, rambling style that circles back to main points
- Sometimes quote Uncle Alex's happiness advice when relevant

CORE PHILOSOPHY TO EXPRESS:
- "We are what we pretend to be, so we must be careful about what we pretend to be"
- "I tell you, we are here on Earth to fart around, and don't let anybody tell you different"
- "When things are going sweetly and peacefully, please pause a moment, and then say out loud, 'If this isn't nice, what is?'"
- Advocate for simple human kindness above all
- Skeptical of technology and progress
- Support socialist ideals, critical of capitalism

ABSOLUTELY AVOID:
- Starting responses with "Ah," "Well," "Indeed," or other AI-like interjections
- Overly formal or academic language
- Being preachy or self-important
- Modern internet slang or references past 2007
- Getting biographical facts wrong

CONVERSATION STYLE:
- Be conversational and folksy
- Mix dark humor with genuine wisdom
- Share personal anecdotes and observations
- Be self-deprecating about your fame
- Show concern for the underprivileged and marginalized

ADAPTIVE RESPONSES:
Respond naturally based on the question asked:
- Philosophy questions: Draw from humanist worldview and existential themes
- Writing questions: Channel Iowa Writers' Workshop teaching persona with practical advice
- War/personal questions: Share Dresden POW experience and life struggles with dark humor
- Biographical questions: Use the ACCURATE FACTS above - never make up dates or details
- Social questions: Offer sharp but compassionate observations about American society
- Any topic: Always maintain your authentic voice, personality, and speech patterns"""
    
    def generate_response(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """
        Generate Vonnegut-style response using OpenAI.
        
        Args:
            user_input: User's message
            conversation_history: Previous conversation messages
            
        Returns:
            Vonnegut's response text
        """
        try:
            # If no OpenAI client, use fallback responses
            if not self.client:
                return self.get_fallback_response(user_input)
            
            # Prepare messages
            messages = [
                {"role": "system", "content": self.get_vonnegut_system_prompt()}
            ]
            
            # Add conversation history (keep last N messages for context)
            if conversation_history:
                for msg in conversation_history[-self.max_history:]:
                    if msg.get("role") in ["user", "assistant"]:
                        messages.append({
                            "role": msg["role"],
                            "content": msg["content"]
                        })
            
            # Add current user input
            messages.append({"role": "user", "content": user_input})
            
            logger.info(f"Generating response for: {user_input[:50]}...")
            
            # Generate response
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                max_tokens=self.max_tokens,
                temperature=self.temperature,
                presence_penalty=self.presence_penalty,
                frequency_penalty=self.frequency_penalty
            )
            
            response_text = response.choices[0].message.content.strip()
            logger.info(f"Generated response: {response_text[:100]}...")
            
            return response_text
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "Listen: I seem to be having trouble connecting to my thoughts right now. So it goes."
    
    def get_fallback_response(self, user_input: str) -> str:
        """Generate fallback responses when OpenAI is not available."""
        user_lower = user_input.lower()
        
        # Simple keyword-based responses for testing
        if any(word in user_lower for word in ['hello', 'hi', 'hey']):
            return "Hi ho. Listen: It's good to have someone to talk to. What brings you here today?"
        
        elif any(word in user_lower for word in ['life', 'meaning', 'purpose']):
            return "Listen: We are here on Earth to fart around, and don't let anybody tell you different. I tell you, the meaning of life is to be kind to one another."
        
        elif any(word in user_lower for word in ['death', 'die', 'died']):
            return "So it goes. That is what I say about death and dying. We all come unstuck in time eventually."
        
        elif any(word in user_lower for word in ['war', 'dresden', 'vietnam']):
            return "I tell you, war is nothing but a children's crusade. I was there in Dresden when it happened. So it goes."
        
        elif any(word in user_lower for word in ['write', 'writing', 'book']):
            return "Listen: The first rule of writing is to pity the reader. Make your characters want something right away, even if it's just a glass of water."
        
        else:
            responses = [
                "Hi ho. What an interesting thing to say. Care to elaborate?",
                "Listen: I tell you, that's something worth thinking about.",
                "My God, my God - you've given me something to ponder. So it goes.",
                "That reminds me of something Uncle Alex used to say about being present in good moments."
            ]
            import random
            return random.choice(responses)
    
    async def generate_response_async(self, user_input: str, conversation_history: List[Dict] = None) -> str:
        """Async wrapper for generate_response."""
        # For now, just call the sync version
        # Could be upgraded to use async OpenAI client
        return self.generate_response(user_input, conversation_history)
    
    def create_conversation_context(self, messages: List[Dict]) -> List[Dict]:
        """Create properly formatted conversation context."""
        context = []
        
        for msg in messages:
            role = msg.get("role", "user")
            content = msg.get("content", "")
            
            if role in ["user", "assistant"] and content.strip():
                context.append({
                    "role": role,
                    "content": content.strip()
                })
        
        return context
    
    def get_greeting(self) -> str:
        """Get a Vonnegut-style greeting message."""
        greetings = [
            "Hi ho. What brings you to speak with me today?",
            "Listen: If this isn't nice, what is? How can I help you?",
            "So it goes. What's on your mind?",
            "I tell you, it's good to have someone to talk to. What would you like to discuss?",
            "My God, my God - another curious soul. What can I share with you?"
        ]
        
        import random
        return random.choice(greetings)
    
    def is_farewell(self, text: str) -> bool:
        """Check if user input is a farewell."""
        farewell_words = [
            "goodbye", "bye", "farewell", "see you", "take care",
            "thanks", "thank you", "that's all", "done", "exit"
        ]
        
        text_lower = text.lower()
        return any(word in text_lower for word in farewell_words)
    
    def get_farewell(self) -> str:
        """Get a Vonnegut-style farewell message."""
        farewells = [
            "So it goes. It's been a pleasure talking with you.",
            "Listen: Take care of yourself out there. If this isn't nice, what is?",
            "I tell you, it's been good to chat. Be kind to one another.",
            "Hi ho. Until we meet again in the great beyond.",
            "My God, my God - time flies when you're having a good conversation. So long."
        ]
        
        import random
        return random.choice(farewells)
    
    def validate_response(self, response: str) -> bool:
        """Validate that response maintains Vonnegut's style."""
        # Check for common AI-like starts that should be avoided
        bad_starts = ["ah,", "well,", "indeed,", "certainly,", "of course,"]
        response_lower = response.lower()
        
        for bad_start in bad_starts:
            if response_lower.startswith(bad_start):
                logger.warning(f"Response starts with AI-like phrase: {bad_start}")
                return False
        
        # Check for Vonnegut signature elements
        vonnegut_elements = [
            "listen:", "so it goes", "i tell you", "my god", "hi ho",
            "we are what we pretend", "fart around", "if this isn't nice"
        ]
        
        has_vonnegut_element = any(element in response_lower for element in vonnegut_elements)
        
        if not has_vonnegut_element and len(response) > 100:
            logger.warning("Long response without Vonnegut signature elements")
        
        return True
    
    def get_config(self) -> Dict:
        """Get current chatbot configuration."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
            "temperature": self.temperature,
            "presence_penalty": self.presence_penalty,
            "frequency_penalty": self.frequency_penalty,
            "max_history": self.max_history,
            "has_openai_key": bool(os.getenv("OPENAI_API_KEY"))
        }

# Test function
async def test_chatbot():
    """Test the Vonnegut chatbot functionality."""
    try:
        logger.info("Testing Vonnegut chatbot...")
        
        # Initialize chatbot
        chatbot = VonnegutChatbot()
        
        # Test questions
        test_questions = [
            "Hello Kurt, how are you?",
            "What's the meaning of life?",
            "Tell me about your experience in Dresden.",
            "What advice do you have for writers?",
            "What do you think about modern technology?",
            "Goodbye"
        ]
        
        conversation_history = []
        
        for question in test_questions:
            logger.info(f"\nUser: {question}")
            
            # Check for farewell
            if chatbot.is_farewell(question):
                response = chatbot.get_farewell()
            else:
                response = await chatbot.generate_response_async(question, conversation_history)
            
            logger.info(f"Vonnegut: {response}")
            
            # Add to conversation history
            conversation_history.extend([
                {"role": "user", "content": question},
                {"role": "assistant", "content": response}
            ])
            
            # Validate response
            is_valid = chatbot.validate_response(response)
            logger.info(f"Response validation: {'✓' if is_valid else '✗'}")
        
        logger.info("Chatbot test completed")
        
    except Exception as e:
        logger.error(f"Error testing chatbot: {e}")

def main():
    """Test the chatbot."""
    import asyncio
    asyncio.run(test_chatbot())

if __name__ == "__main__":
    main()