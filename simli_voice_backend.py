#!/usr/bin/env python3
"""
Simli Voice Backend - Connects Simli widget to GPT-4o + RAG + ElevenLabs voice system
"""
import os
import asyncio
import base64
import json
import logging
from typing import Optional
import aiohttp
import numpy as np
from dotenv import load_dotenv

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Load environment variables from .env file
load_dotenv()

# Import the voice system components
from voice_system import VoiceSystem
from rag_system import SimpleRAGSystem

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Simli Voice Backend", version="1.0.0")

# Add CORS middleware for Simli widget
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global variables for voice system
voice_system = None
rag_system = None

class SimliVoiceBackend:
    def __init__(self):
        self.voice_system = None
        self.rag_system = None
        self.active_connections = []
        
    async def initialize_systems(self):
        """Initialize the voice and RAG systems"""
        try:
            logger.info("Initializing voice and RAG systems...")
            
            # Check environment variables
            openai_key = os.getenv("OPENAI_API_KEY")
            elevenlabs_key = os.getenv("ELEVENLABS_API_KEY")
            
            if not openai_key:
                logger.warning("OPENAI_API_KEY not found - some features may not work")
            if not elevenlabs_key:
                logger.warning("ELEVENLABS_API_KEY not found - voice synthesis may not work")
            
            # Initialize RAG system
            try:
                self.rag_system = SimpleRAGSystem()
                await self.rag_system.load_knowledge_base("indiana_knowledge_base.pkl")
                logger.info("RAG system initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize RAG system: {e}")
                # Continue without RAG system
                self.rag_system = None
            
            # Initialize voice system
            try:
                self.voice_system = VoiceSystem()
                await self.voice_system.initialize()
                logger.info("Voice system initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize voice system: {e}")
                # Continue without voice system
                self.voice_system = None
            
            # Return True if at least one system initialized
            if self.rag_system is not None or self.voice_system is not None:
                logger.info(f"Systems initialization completed - RAG: {self.rag_system is not None}, Voice: {self.voice_system is not None}")
                return True
            else:
                logger.error("No systems could be initialized - check environment variables and dependencies")
                return False
                
        except Exception as e:
            logger.error(f"Failed to initialize systems: {e}")
            return False
    
    async def process_audio_input(self, audio_data: bytes, persona: str = "indiana") -> dict:
        """Process audio input through the voice system"""
        try:
            logger.info(f"Processing audio input for persona: {persona}")
            
            # Convert audio to text using voice system
            text_response = await self.voice_system.process_audio_input(audio_data, persona)
            
            # Generate AI response using RAG
            ai_response = await self.rag_system.get_response(text_response, persona)
            
            # Convert AI response to speech
            audio_response = await self.voice_system.text_to_speech(ai_response, persona)
            
            # Encode audio response as base64
            audio_base64 = base64.b64encode(audio_response).decode('utf-8')
            
            return {
                "success": True,
                "text_response": text_response,
                "ai_response": ai_response,
                "audio_response": audio_base64,
                "audio_format": "wav"
            }
            
        except Exception as e:
            logger.error(f"Error processing audio input: {e}")
            return {
                "success": False,
                "error": str(e)
            }

# Initialize the backend
backend = SimliVoiceBackend()

# Mount static files for assets
if os.path.exists("assets"):
    app.mount("/assets", StaticFiles(directory="assets"), name="assets")

@app.on_event("startup")
async def startup_event():
    """Initialize systems on startup"""
    success = await backend.initialize_systems()
    if not success:
        logger.error("Failed to initialize systems on startup")

@app.get("/api/status")
async def api_status():
    """API status endpoint"""
    # Check if systems are initialized
    voice_ready = backend.voice_system is not None
    rag_ready = backend.rag_system is not None
    
    # Systems are considered initialized if at least one is ready
    systems_initialized = voice_ready or rag_ready
    
    return {
        "message": "Simli Voice Backend",
        "status": "running",
        "systems_initialized": systems_initialized,
        "voice_system_ready": voice_ready,
        "rag_system_ready": rag_ready,
        "environment": {
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "elevenlabs_key": bool(os.getenv("ELEVENLABS_API_KEY")),
            "knowledge_base_exists": os.path.exists("indiana_knowledge_base.pkl")
        }
    }

@app.get("/")
async def root():
    """Serve the main Simli integration HTML"""
    if os.path.exists("working_simli_integration.html"):
        return FileResponse("working_simli_integration.html")
    else:
        return {"message": "Simli Voice Backend is running. HTML interface not found."}

@app.get("/simli-test")
async def simli_test():
    """Serve the simple Simli test HTML"""
    if os.path.exists("simple_simli_test.html"):
        return FileResponse("simple_simli_test.html")
    else:
        return {"message": "simple_simli_test.html not found"}

@app.get("/kiosk")
async def oracle_kiosk():
    """Serve the Oracle Kiosk interface"""
    if os.path.exists("oracle_kiosk_interface.html"):
        return FileResponse("oracle_kiosk_interface.html")
    else:
        return {"message": "oracle_kiosk_interface.html not found"}

@app.get("/holographic")
async def oracle_holographic():
    """Serve the Holographic Oracle interface with frame overlay"""
    if os.path.exists("oracle_kiosk_holographic.html"):
        return FileResponse("oracle_kiosk_holographic.html")
    else:
        return {"message": "oracle_kiosk_holographic.html not found"}

@app.get("/cdn-test")
async def simli_cdn_test():
    """Serve the Simli CDN test page"""
    if os.path.exists("simli_cdn_test.html"):
        return FileResponse("simli_cdn_test.html")
    else:
        return {"message": "simli_cdn_test.html not found"}

@app.get("/v3")
async def oracle_kiosk_v3():
    """Serve the Oracle Kiosk v3.0 - Fresh version without cache issues"""
    if os.path.exists("oracle_kiosk_v3.html"):
        return FileResponse("oracle_kiosk_v3.html")
    else:
        return {"message": "oracle_kiosk_v3.html not found"}

@app.get("/simli-config")
async def get_simli_config():
    """Expose Simli token/agent configuration from environment for the frontend.

    Looks for SIMLI_TOKEN first, then SIMLI_API_KEY (backward compat). Also allows
    overriding default agent via SIMLI_AGENT_ID. Returns minimal info to avoid
    leaking keys in logs.
    """
    token = os.getenv("SIMLI_TOKEN") or os.getenv("SIMLI_API_KEY")
    agent_id = os.getenv("SIMLI_AGENT_ID")

    # Fallback agent id to Indiana persona if not explicitly provided
    if not agent_id:
        agent_id = "0c2b8b04-5274-41f1-a21c-d5c98322efa9"

    return {
        "token_present": bool(token),
        "token": token or "",
        "agentId": agent_id,
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "voice_system": backend.voice_system is not None,
        "rag_system": backend.rag_system is not None
    }

@app.get("/mock")
async def mock_page():
    """Serve the simplified mock avatar page."""
    if os.path.exists("mock_avatar.html"):
        return FileResponse("mock_avatar.html")
    return {"message": "mock_avatar.html not found"}

@app.get("/debug-env")
async def debug_environment():
    """Debug endpoint to see what environment variables are available"""
    import os
    
    # Get all environment variables that might be relevant
    env_vars = {}
    for key, value in os.environ.items():
        if any(keyword in key.upper() for keyword in ['OPENAI', 'ELEVEN', 'SIMLI', 'HEYGEN', 'API', 'KEY']):
            # Only show first/last few chars for security
            if value:
                masked_value = f"{value[:8]}...{value[-4:]}" if len(value) > 12 else "***MASKED***"
                env_vars[key] = masked_value
            else:
                env_vars[key] = "EMPTY"
    
    return {
        "environment_variables": env_vars,
        "total_env_vars": len(os.environ),
        "working_directory": os.getcwd(),
        "python_path": os.environ.get("PYTHONPATH", "Not set"),
        "direct_checks": {
            "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY") is not None,
            "ELEVENLABS_API_KEY": os.getenv("ELEVENLABS_API_KEY") is not None,
            "SIMLI_API_KEY": os.getenv("SIMLI_API_KEY") is not None,
            "SIMLI_FACE_ID": os.getenv("SIMLI_FACE_ID") is not None
        }
    }

@app.post("/process-audio")
async def process_audio(audio_data: dict):
    """Process audio input from Simli widget with persona routing"""
    try:
        # Extract audio data and persona
        audio_base64 = audio_data.get("audio")
        persona = audio_data.get("persona", "indiana")
        
        if not audio_base64:
            raise HTTPException(status_code=400, detail="No audio data provided")
        
        # Validate persona
        valid_personas = ["bigfoot", "indiana", "vonnegut"]
        if persona not in valid_personas:
            persona = "indiana"  # Default fallback
        
        logger.info(f"Processing audio for persona: {persona}")
        
        # Decode base64 audio
        audio_bytes = base64.b64decode(audio_base64)
        
        # Process through voice system with persona-specific routing
        result = await backend.process_audio_input(audio_bytes, persona)
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in process-audio endpoint: {e}")
        return JSONResponse(
            status_code=500,
            content={"success": False, "error": str(e)}
        )

@app.get("/personas")
async def get_personas():
    """Get available personas and their configurations"""
    return {
        "personas": [
            {
                "id": "bigfoot",
                "name": "Brown County Bigfoot",
                "description": "Legendary cryptid storyteller of Indiana's forests",
                "simli_face_id": "6926a39d-638b-49c5-9328-79efa034e9a4",
                "voice": "stock-simli",
                "knowledge": "cryptid-folklore"
            },
            {
                "id": "indiana", 
                "name": "Hoosier Oracle",
                "description": "Eternal consciousness of Indiana's history and culture",
                "simli_face_id": "0c2b8b04-5274-41f1-a21c-d5c98322efa9",
                "voice": "elevenlabs-hoosier",
                "knowledge": "indiana-history"
            },
            {
                "id": "vonnegut",
                "name": "Kurt Vonnegut", 
                "description": "Indianapolis author with dark humor and humanist wisdom",
                "simli_face_id": "6ebf0aa7-6fed-443d-a4c6-fd1e3080b215",
                "voice": "elevenlabs-vonnegut",
                "knowledge": "vonnegut-corpus"
            }
        ]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    backend.active_connections.append(websocket)
    
    try:
        while True:
            # Receive message from Simli widget
            data = await websocket.receive_text()
            message = json.loads(data)
            
            if message.get("type") == "audio":
                # Process audio input
                audio_base64 = message.get("audio")
                persona = message.get("persona", "indiana")
                
                if audio_base64:
                    audio_bytes = base64.b64decode(audio_base64)
                    result = await backend.process_audio_input(audio_bytes, persona)
                    
                    # Send response back to Simli widget
                    await websocket.send_text(json.dumps(result))
            
            elif message.get("type") == "ping":
                # Respond to ping
                await websocket.send_text(json.dumps({"type": "pong"}))
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
    finally:
        if websocket in backend.active_connections:
            backend.active_connections.remove(websocket)

@app.post("/initialize")
async def initialize_systems():
    """Manually initialize systems"""
    try:
        success = await backend.initialize_systems()
        
        # Get detailed status
        status = {
            "success": success,
            "voice_system": backend.voice_system is not None,
            "rag_system": backend.rag_system is not None,
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "elevenlabs_key": bool(os.getenv("ELEVENLABS_API_KEY")),
            "knowledge_base_exists": os.path.exists("indiana_knowledge_base.pkl"),
            "systems_initialized": (backend.voice_system is not None or backend.rag_system is not None)
        }
        
        if success:
            status["message"] = "Systems initialized successfully"
        else:
            status["message"] = "Failed to initialize systems - check logs for details"
            
        return status
        
    except Exception as e:
        logger.error(f"Error in manual initialization: {e}")
        return {
            "success": False,
            "error": str(e),
            "message": "Exception during initialization",
            "voice_system": backend.voice_system is not None,
            "rag_system": backend.rag_system is not None,
            "openai_key": bool(os.getenv("OPENAI_API_KEY")),
            "elevenlabs_key": bool(os.getenv("ELEVENLABS_API_KEY")),
            "knowledge_base_exists": os.path.exists("indiana_knowledge_base.pkl")
        }

if __name__ == "__main__":
    # Get port from environment variable (for Railway)
    port = int(os.environ.get("PORT", 8083))
    
    # Run the server
    uvicorn.run(
        "simli_voice_backend:app",
        host="0.0.0.0",
        port=port,
        reload=True,
        log_level="info"
    )

# For Vercel deployment
app_instance = app 