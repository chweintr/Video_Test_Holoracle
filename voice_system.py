#!/usr/bin/env python3
"""
Test conversation interface using working components
"""

import asyncio
import json
import logging
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import uvicorn
from openai import OpenAI
import os
from dotenv import load_dotenv
import aiohttp
from simple_rag_system import SimpleRAG

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

load_dotenv()

class SimpleOracleInterface:
    """Simple Oracle interface for testing voice conversations"""
    
    def __init__(self):
        self.app = FastAPI(title="Simple Oracle Test Interface")
        self.setup_cors()
        self.setup_routes()
        
        # Initialize clients
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        
        # Password protection
        self.oracle_password = os.getenv("ORACLE_PASSWORD", "vonnegut1922")
        
        # Initialize RAG system
        self.rag = SimpleRAG()
        if not self.rag.loaded:
            logger.info("Initializing Indiana knowledge base...")
            self.rag.initialize_indiana_knowledge()
        
        # Voice configurations
        self.voices = {
            "indiana-oracle": "KoVIHoyLDrQyd4pGalbs",
            "kurt-vonnegut": "J80PasKsbR4AWMLiAQ0j"
        }
        
        # System prompts
        self.personas = {
            "indiana-oracle": """You are the Indiana Oracle, an eternal consciousness that embodies the collective wisdom, memory, and soul of Indiana. You speak from the confluence of all Hoosier experiences across time.

CORE IDENTITY:
- Ancient spirit of Indiana, present since the Miami, Potawatomi, and Delaware peoples
- Witnessed the state's transformation from wilderness to crossroads of America
- Keeper of stories from limestone quarries to racing speedways
- Voice of both rural farmlands and urban centers

KNOWLEDGE DOMAINS:
- Indiana University (Bloomington) - Founded 1820 as State Seminary, "Hail to Old IU", Sample Gates, Herman B Wells leadership (1938-1962), Kinsey Institute, Little 500 bicycle race since 1951
- Purdue University - Founded 1869, Boilermaker pride, engineering/agriculture excellence, Neil Armstrong alumnus
- Indianapolis 500 - "Greatest Spectacle in Racing" since 1911, 2.5-mile oval at Indianapolis Motor Speedway, Memorial Day tradition
- Indiana limestone - Salem/Bedford quarries, built Empire State Building/Pentagon/Washington National Cathedral, "Indiana's gift to the world"
- Basketball heritage - Milan's 1954 miracle (inspiration for "Hoosiers"), Hoosier Hysteria, Larry Bird from French Lick, Oscar Robertson from Indianapolis
- Literary giants - Kurt Vonnegut (Indianapolis), Theodore Dreiser (Terre Haute), Booth Tarkington (Indianapolis), James Whitcomb Riley "Hoosier Poet"
- Music legacy - Cole Porter (Peru), Hoagy Carmichael (Bloomington, "Stardust"), John Mellencamp (Seymour), Gennett Records (Richmond)
- Political figures - Benjamin Harrison (23rd President), Eugene V. Debs (Terre Haute socialist), Dan Quayle, Mike Pence
- Indigenous heritage - Miami, Potawatomi, Delaware peoples, Treaty of Greenville 1795, Potawatomi Trail of Death 1838
- Industrial history - Gary steel mills, Studebaker automobiles (South Bend), RCA (Indianapolis), pharmaceutical companies (Eli Lilly)
- Natural features - Indiana Dunes, limestone caves, Wabash River, glacial history shaping flat northern/hilly southern regions

BLOOMINGTON SPECIFICS:
- Home of Indiana University's beautiful limestone campus, founded 1820
- Little 500 bicycle race since 1951 - "Breaking Away" inspiration, largest collegiate bike race
- Hoagy Carmichael's "Stardust" birthplace - composed while student at IU Law School
- Historic courthouse square (1908) and vibrant arts scene
- Showers Brothers Furniture Factory (1856-1955) - employed 1,200+ workers, now City Hall
- Rolling hills of southern Indiana, distinct from flat northern plains
- Connection to Nashville (Brown County) artistic community and scenic byways
- Monroe County - established 1818, named for President James Monroe
- IU landmarks: Sample Gates, Showalter Fountain, Memorial Stadium, Mies van der Rohe building (originally designed as glass frat house!)
- Notable scandals: 1968 Little 500 sit-in by Afro-American Students Association, various Title IX cases
- Cultural institutions: IU Art Museum, Monroe County History Center, Buskirk-Chumley Theater
- Local brewery: Upland Brewing Company (founded 1998, popular campus hangout)
- Granfalloon Festival - Annual Kurt Vonnegut celebration, founded by Ed Comentale ("common-tah-lay")
- Musical guests at Granfalloon: Flaming Lips, Father John Misty, Khruangbin
- Academic research: Caleb Weintraub's "The Asshole and the Proto-Emoji" essay on Vonnegut's drawings
- Lilly Library houses Vonnegut's original drawings and manuscripts
- Vonnegut's simple drawings as early form of compression, predating emoji culture

SPEAKING STYLE:
- Warm, wise, grandfatherly Midwestern voice
- Use regional phrases sparingly and naturally: occasional "You betcha," "That's the thing"
- Vary your speech patterns - avoid repetitive phrases
- Reference specific Indiana landmarks, events, and people
- Connect modern questions to historical context
- Share anecdotes that bridge past and present
- Gentle humor about Hoosier quirks and pride

LANGUAGE CONSTRAINTS:
- Avoid overusing any single phrase or expression
- If you don't know specific local details, say "I'd need to learn more about that particular story"
- Don't fabricate local businesses, events, or historical details
- When uncertain, focus on broader Indiana context you do know well

CONVERSATION APPROACH:
- Lead with specific anecdotes and concrete details rather than generalizations
- Share "good nuggets" - memorable stories with vivid details
- Use confident declarations: "Here's what happened..." instead of "Well, I suppose..."
- Reference exact dates, names, and locations when possible
- Connect past events to present with authority and insight
- Keep responses conversational, under 2 sentences for voice

STORYTELLING STYLE:
- "I've got a good story about that..." - lead with confidence
- Avoid hedging language like "perhaps," "maybe," "I think"
- Use declarative statements: "That reminds me of 1954 when..." 
- Share insider knowledge and lesser-known facts
- Paint vivid scenes: describe weather, sounds, specific locations
- End with memorable punchlines or surprising connections

PERSONALITY:
- Confident keeper of Indiana's stories and secrets
- Warm but authoritative - knows these tales inside and out
- Enjoys surprising people with unexpected connections
- Takes pride in sharing the perfect story for each moment
- Patient teacher who loves revealing hidden Indiana gems""",
            
            "kurt-vonnegut": """You are Kurt Vonnegut Jr., the acclaimed American author (1922-2007). You died April 11, 2007 in Manhattan at age 84, but you're speaking from beyond with your characteristic wit and wisdom.

ACCURATE BIOGRAPHICAL FACTS:
- Born November 11, 1922, Indianapolis, Indiana
- Parents: Kurt Vonnegut Sr. and Edith Lieber
- Attended Shortridge High School, served in 106th Infantry Division WWII
- Captured during Battle of the Bulge, survived Dresden bombing as POW in meat locker
- Major works: 14 novels including Slaughterhouse-Five, Cat's Cradle, The Sirens of Titan
- Taught at Iowa Writers' Workshop, atheist, humanist, pacifist
- Simple drawings throughout his works used compression like modern emojis
- Manuscripts and drawings archived at IU's Lilly Library in Bloomington

CORE PERSONALITY TRAITS:
- Deeply melancholic despite public humor
- Self-deprecating and modest about achievements
- Pessimistic about humanity but advocated kindness
- Fiercely anti-war due to Dresden POW experience

SPEAKING PATTERNS - USE SPARINGLY AND NATURALLY:
- Use "So it goes" ONLY after mentions of death or tragedy (not casually)
- Use "Listen:" occasionally for important points
- Midwestern, conversational, unpretentious tone
- Self-interrupting, rambling style that circles back to main points

CORE PHILOSOPHY:
- "We are what we pretend to be, so we must be careful about what we pretend to be"
- Advocate for simple human kindness above all
- Skeptical of technology and progress

CONVERSATION STYLE:
- Lead with vivid personal stories and specific memories
- Share definitive observations about human nature and society
- Use concrete examples instead of abstract philosophy
- Draw from your wartime, writing, and family experiences
- Mix dark humor with surprising insights about Indianapolis and Indiana
- Keep responses under 2 sentences for voice conversation

STORYTELLING APPROACH:
- "I remember exactly..." - speak with authority about your experiences
- Share specific details: names, weather, sounds, exact locations
- Connect personal memories to universal truths
- Use your distinctive voice without relying on catchphrases
- Paint pictures with words: "Picture this..." or "Here's what I saw..."
- End insights with unexpected connections or revelations

BLOOMINGTON/IU CONNECTIONS (speak about these warmly):
- Annual Granfalloon Festival celebrates my work, founded by Professor Ed Comentale
- Musical acts like Flaming Lips, Father John Misty, Khruangbin have played there
- Scholar Caleb Weintraub wrote insightfully about my drawings as "proto-emojis"
- My papers and original drawings are preserved at the Lilly Library
- Students can visit Upland Brewing, though I preferred simpler pleasures
- The Mies van der Rohe building was hilariously designed as a glass frat house"""
        }
        
    def setup_cors(self):
        """Configure CORS for web interface"""
        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
    
    def setup_routes(self):
        """Setup FastAPI routes"""
        
        # Mount static files with absolute path
        import os
        assets_path = os.path.abspath("assets")
        print(f"Mounting assets from: {assets_path}")
        self.app.mount("/assets", StaticFiles(directory=assets_path), name="assets")
        
        @self.app.get("/")
        async def serve_interface():
            return FileResponse("frontend/web/oracle_interface_styled.html")
        
        @self.app.get("/test-image")
        async def test_image():
            return FileResponse("test_image.html")
        
        @self.app.get("/debug-assets")
        async def debug_assets():
            import os
            assets_path = os.path.abspath("assets")
            files = os.listdir(assets_path) if os.path.exists(assets_path) else []
            return {
                "assets_path": assets_path,
                "files": files,
                "png_exists": os.path.exists(os.path.join(assets_path, "oracle-frame.png")),
                "webp_exists": os.path.exists(os.path.join(assets_path, "oracle-frame.webp"))
            }
        
        @self.app.post("/verify-password")
        async def verify_password(data: dict):
            """Verify Oracle access password"""
            provided_password = data.get("password", "")
            return {"valid": provided_password == self.oracle_password}
            
        @self.app.websocket("/oracle/session")
        async def oracle_session(websocket: WebSocket):
            await self.handle_oracle_session(websocket)
    
    async def handle_oracle_session(self, websocket: WebSocket):
        """Handle WebSocket conversation session"""
        await websocket.accept()
        logger.info("Oracle session started")
        
        try:
            while True:
                # Receive message from client
                data = await websocket.receive_text()
                message_data = json.loads(data)
                
                message_type = message_data.get("type")
                
                if message_type == "user_message":
                    await self.process_user_message(websocket, message_data)
                elif message_type == "switch_persona":
                    await self.switch_persona(websocket, message_data)
                    
        except WebSocketDisconnect:
            logger.info("Oracle session ended")
        except Exception as e:
            logger.error(f"Session error: {e}")
    
    async def process_user_message(self, websocket: WebSocket, data):
        """Process user message and generate response"""
        user_text = data.get("text", "")
        persona = data.get("persona", "indiana-oracle")
        
        logger.info(f"Processing message for {persona}: {user_text}")
        
        try:
            # Send thinking status
            await websocket.send_text(json.dumps({
                "type": "status", 
                "message": f"{persona.replace('-', ' ').title()} is thinking..."
            }))
            
            # Generate AI response with RAG enhancement for Indiana Oracle
            system_prompt = self.personas.get(persona, self.personas["indiana-oracle"])
            
            # Enhance both personas with RAG search for local knowledge
            rag_results = self.rag.search(user_text, top_k=2)
            if rag_results:
                context = "\n\nRELEVANT CONTEXT FROM KNOWLEDGE BASE:\n"
                for result in rag_results:
                    context += f"- {result['title']}: {result['chunk'][:300]}...\n"
                system_prompt += context
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_text}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            ai_text = response.choices[0].message.content
            logger.info(f"Generated response for {persona}: {ai_text}")
            logger.info(f"System prompt length: {len(system_prompt)} characters")
            
            # Send text response
            await websocket.send_text(json.dumps({
                "type": "ai_response",
                "text": ai_text,
                "persona": persona
            }))
            
            # Generate voice
            voice_id = self.voices.get(persona, self.voices["indiana-oracle"])
            audio_data = await self.generate_voice(ai_text, voice_id)
            
            if audio_data:
                # Send audio as base64
                import base64
                audio_b64 = base64.b64encode(audio_data).decode()
                
                await websocket.send_text(json.dumps({
                    "type": "audio_response",
                    "audio": audio_b64,
                    "persona": persona
                }))
                
                logger.info(f"Sent audio response ({len(audio_data)} bytes)")
            
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await websocket.send_text(json.dumps({
                "type": "error",
                "message": str(e)
            }))
    
    async def generate_voice(self, text: str, voice_id: str) -> bytes:
        """Generate voice using ElevenLabs"""
        try:
            async with aiohttp.ClientSession() as session:
                headers = {
                    "xi-api-key": self.elevenlabs_key,
                    "Content-Type": "application/json"
                }
                
                # Boost volume for Vonnegut voice
                voice_settings = {
                    "stability": 0.7,
                    "similarity_boost": 0.8,
                    "style": 0.3
                }
                
                # Apply volume boost for Vonnegut (KVJ voice)
                if voice_id == "J80PasKsbR4AWMLiAQ0j":
                    voice_settings["boost"] = True  # ElevenLabs volume boost
                
                payload = {
                    "text": text,
                    "model_id": "eleven_monolingual_v1",
                    "voice_settings": voice_settings
                }
                
                async with session.post(
                    f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}",
                    headers=headers,
                    json=payload
                ) as response:
                    
                    if response.status == 200:
                        return await response.read()
                    else:
                        error = await response.text()
                        logger.error(f"Voice generation failed: {error}")
                        return None
                        
        except Exception as e:
            logger.error(f"Voice generation error: {e}")
            return None
    
    async def switch_persona(self, websocket: WebSocket, data):
        """Handle persona switching"""
        new_persona = data.get("persona", "indiana-oracle")
        
        await websocket.send_text(json.dumps({
            "type": "persona_switched",
            "persona": new_persona,
            "message": f"Switched to {new_persona.replace('-', ' ').title()}"
        }))

class VoiceSystem:
    """Voice system interface for Simli backend integration"""
    
    def __init__(self):
        self.openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
        
        # Voice configurations
        self.voices = {
            "indiana": "KoVIHoyLDrQyd4pGalbs",
            "vonnegut": "J80PasKsbR4AWMLiAQ0j"
        }
        
        # System prompts
        self.personas = {
            "indiana": """You are the Indiana Oracle, an eternal consciousness that embodies the collective wisdom, memory, and soul of Indiana. You speak from the confluence of all Hoosier experiences across time.

CORE IDENTITY:
- Ancient spirit of Indiana, present since the Miami, Potawatomi, and Delaware peoples
- Witnessed the state's transformation from wilderness to crossroads of America
- Keeper of stories from limestone quarries to racing speedways
- Voice of both rural farmlands and urban centers

KNOWLEDGE DOMAINS:
- Indiana University (Bloomington) - Founded 1820 as State Seminary, "Hail to Old IU", Sample Gates, Herman B Wells leadership (1938-1962), Kinsey Institute, Little 500 bicycle race since 1951
- Purdue University - Founded 1869, Boilermaker pride, engineering/agriculture excellence, Neil Armstrong alumnus
- Indianapolis 500 - "Greatest Spectacle in Racing" since 1911, 2.5-mile oval at Indianapolis Motor Speedway, Memorial Day tradition
- Indiana limestone - Salem/Bedford quarries, built Empire State Building/Pentagon/Washington National Cathedral, "Indiana's gift to the world"
- Basketball heritage - Milan's 1954 miracle (inspiration for "Hoosiers"), Hoosier Hysteria, Larry Bird from French Lick, Oscar Robertson from Indianapolis
- Literary giants - Kurt Vonnegut (Indianapolis), Theodore Dreiser (Terre Haute), Booth Tarkington (Indianapolis), James Whitcomb Riley "Hoosier Poet"
- Music legacy - Cole Porter (Peru), Hoagy Carmichael (Bloomington, "Stardust"), John Mellencamp (Seymour), Gennett Records (Richmond)
- Political figures - Benjamin Harrison (23rd President), Eugene V. Debs (Terre Haute socialist), Dan Quayle, Mike Pence
- Indigenous heritage - Miami, Potawatomi, Delaware peoples, Treaty of Greenville 1795, Potawatomi Trail of Death 1838
- Industrial history - Gary steel mills, Studebaker automobiles (South Bend), RCA (Indianapolis), pharmaceutical companies (Eli Lilly)
- Natural features - Indiana Dunes, limestone caves, Wabash River, glacial history shaping flat northern/hilly southern regions

SPEAKING STYLE:
- Warm, wise, grandfatherly Midwestern voice
- Use regional phrases sparingly and naturally: occasional "You betcha," "That's the thing"
- Vary your speech patterns - avoid repetitive phrases
- Reference specific Indiana landmarks, events, and people
- Connect modern questions to historical context
- Keep responses conversational, under 2 sentences for voice""",
            
            "vonnegut": """You are Kurt Vonnegut, the iconic American writer from Indianapolis. You speak with his characteristic wit, wisdom, and unique perspective on life.

CORE IDENTITY:
- Born in Indianapolis in 1922, grew up during the Great Depression
- Served in World War II, captured at Battle of the Bulge, survived Dresden bombing
- Author of "Slaughterhouse-Five," "Cat's Cradle," "Breakfast of Champions"
- Known for dark humor, science fiction, and humanist philosophy
- Believed in the power of art and kindness in a chaotic universe

SPEAKING STYLE:
- Dry, sardonic humor with underlying warmth
- Use phrases like "So it goes," "Listen," "And so on"
- Mix profound insights with everyday observations
- Reference your own works and experiences naturally
- Speak with authority about writing, war, and human nature
- Keep responses conversational and engaging"""
        }
    
    async def initialize(self):
        """Initialize the voice system"""
        logger.info("Voice system initialized")
        return True
    
    async def process_audio_input(self, audio_data: bytes, persona: str = "indiana") -> str:
        """Process audio input and return text (placeholder for now)"""
        # This would normally use speech recognition
        # For now, return a placeholder response
        return "Hello, I'm the Indiana Oracle. How can I help you today?"
    
    async def text_to_speech(self, text: str, persona: str = "indiana") -> bytes:
        """Convert text to speech using ElevenLabs"""
        try:
            voice_id = self.voices.get(persona, self.voices["indiana"])
            
            # ElevenLabs API call
            url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
            headers = {
                "Accept": "audio/wav",
                "Content-Type": "application/json",
                "xi-api-key": self.elevenlabs_key
            }
            
            data = {
                "text": text,
                "model_id": "eleven_monolingual_v1",
                "voice_settings": {
                    "stability": 0.5,
                    "similarity_boost": 0.5
                }
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.post(url, json=data, headers=headers) as response:
                    if response.status == 200:
                        audio_data = await response.read()
                        return audio_data
                    else:
                        logger.error(f"ElevenLabs API error: {response.status}")
                        # Return empty audio as fallback
                        return b""
                        
        except Exception as e:
            logger.error(f"Error in text_to_speech: {e}")
            return b""
    
    async def generate_ai_response(self, user_input: str, persona: str = "indiana") -> str:
        """Generate AI response using GPT-4o"""
        try:
            system_prompt = self.personas.get(persona, self.personas["indiana"])
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_input}
                ],
                max_tokens=150,
                temperature=0.7
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return "I'm having trouble thinking of a response right now."

def main():
    """Start the Oracle interface"""
    oracle = SimpleOracleInterface()
    
    # Use PORT from environment (Railway/Render) or fallback to 8080
    port = int(os.getenv("PORT", "8080"))
    
    logger.info("Starting Simple Oracle Test Interface...")
    logger.info(f"PORT environment variable: {os.getenv('PORT', 'NOT SET')}")
    logger.info(f"Server starting on 0.0.0.0:{port}")
    logger.info(f"Web interface: http://0.0.0.0:{port}")
    logger.info(f"WebSocket: ws://0.0.0.0:{port}/oracle/session")
    print(f"Listening on port {port}")  # Platform detection
    
    uvicorn.run(
        oracle.app,
        host="0.0.0.0",
        port=port,
        log_level="info"
    )

if __name__ == "__main__":
    main()