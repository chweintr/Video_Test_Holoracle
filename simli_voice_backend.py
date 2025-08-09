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

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import uvicorn

# Load environment variables from .env file (don't override production)
if os.getenv("RAILWAY_ENVIRONMENT") != "production":
    load_dotenv(override=False)

# Import the voice system components
from voice_system import VoiceSystem
from personas.persona_rag_system import SimpleRAGSystem, PersonaRAGSystem

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
            
            # Initialize persona-specific RAG system
            try:
                self.rag_system = SimpleRAGSystem()  # Keep for backward compatibility
                self.persona_rag_system = PersonaRAGSystem()
                await self.rag_system.load_knowledge_base("indiana_knowledge_base.pkl")
                logger.info("Persona RAG system initialized successfully")
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
        """Process audio input through the persona-specific voice system"""
        try:
            logger.info(f"Processing audio input for persona: {persona}")
            
            # Convert audio to text using voice system
            text_response = await self.voice_system.process_audio_input(audio_data, persona)
            
            # Generate AI response - ONLY use custom system for Vonnegut
            if persona == "vonnegut" and hasattr(self, 'persona_rag_system') and self.persona_rag_system:
                ai_response = await self.persona_rag_system.get_persona_response(persona, text_response)
                logger.info(f"Using enhanced Vonnegut corpus RAG system")
            else:
                # For bigfoot and indiana, use original system (bigfoot uses Simli default AI anyway)
                ai_response = await self.rag_system.get_response(text_response, persona)
                logger.info(f"Using standard RAG for {persona} (bigfoot uses Simli default)")
                
                # Special note for bigfoot - this won't actually be called since bigfoot uses Simli's brain
                if persona == "bigfoot":
                    logger.info("Note: Bigfoot should use Simli's default AI, not this backend")
            
            # Convert AI response to speech
            audio_response = await self.voice_system.text_to_speech(ai_response, persona)
            
            # Encode audio response as base64
            audio_base64 = base64.b64encode(audio_response).decode('utf-8')
            
            return {
                "success": True,
                "text_response": text_response,
                "ai_response": ai_response,
                "audio_response": audio_base64,
                "audio_format": "wav",
                "persona_system": "enhanced" if hasattr(self, 'persona_rag_system') else "fallback"
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

@app.get("/enhanced")
async def oracle_kiosk_enhanced():
    """Serve the Enhanced Oracle Kiosk with Vonnegut corpus integration"""
    if os.path.exists("oracle_kiosk_enhanced.html"):
        return FileResponse("oracle_kiosk_enhanced.html")
    else:
        return {"message": "oracle_kiosk_enhanced.html not found"}

@app.get("/compose")
async def oracle_kiosk_compose():
    """Serve the Compose Oracle Kiosk using Simli Compose API"""
    if os.path.exists("oracle_kiosk_compose.html"):
        return FileResponse("oracle_kiosk_compose.html")
    else:
        return {"message": "oracle_kiosk_compose.html not found"}

@app.get("/widget")
async def oracle_kiosk_widget():
    """Serve the Simli Widget kiosk (agentId + e2e token)."""
    if os.path.exists("oracle_kiosk_widget.html"):
        return FileResponse("oracle_kiosk_widget.html")
    else:
        return {"message": "oracle_kiosk_widget.html not found"}

@app.get("/preview")
async def oracle_kiosk_preview():
    """Serve the visual-only kiosk preview (no Simli)."""
    if os.path.exists("oracle_kiosk_preview.html"):
        return FileResponse("oracle_kiosk_preview.html")
    else:
        return {"message": "oracle_kiosk_preview.html not found"}

@app.get("/master")
async def oracle_kiosk_master():
    """Serve the Master Oracle Kiosk with 3 different visual avatars"""
    if os.path.exists("oracle_kiosk_master.html"):
        return FileResponse("oracle_kiosk_master.html")
    else:
        return {"message": "oracle_kiosk_master.html not found"}

@app.get("/webrtc")
async def oracle_kiosk_webrtc():
    """Serve the WebRTC Compose Oracle Kiosk with actual Simli WebRTC"""
    if os.path.exists("oracle_kiosk_webrtc.html"):
        return FileResponse("oracle_kiosk_webrtc.html")
    else:
        return {"message": "oracle_kiosk_webrtc.html not found"}

@app.get("/bigfoot-test")
async def bigfoot_test():
    """Serve the Bigfoot test page - Step 1: Get avatar in glass case"""
    if os.path.exists("bigfoot_test.html"):
        return FileResponse("bigfoot_test.html")
    else:
        return {"message": "bigfoot_test.html not found"}

@app.get("/simli-config")
async def get_simli_config():
    """Expose Simli token/agent configuration from environment for the frontend.

    Looks for SIMLI_TOKEN first, then SIMLI_API_KEY (backward compat). Also allows
    overriding default agent via SIMLI_AGENT_ID. Returns minimal info to avoid
    leaking keys in logs.
    """
    token = os.getenv("SIMLI_TOKEN") or os.getenv("SIMLI_API_KEY")
    agent_id = os.getenv("SIMLI_AGENT_ID") or os.getenv("SIMLI_FACE_ID")

    # Fallback agent id to Indiana persona if not explicitly provided
    if not agent_id:
        agent_id = "76ed1ae8-720c-45de-918c-cac46984412d"

    return {
        "token_present": bool(token),
        # Do not include the raw token here for security; use /simli-token to fetch a fresh session token
        "token": "", 
        "agentId": agent_id,
    }

@app.post("/simli-compose/session")
@app.get("/simli-compose/session")
async def simli_compose_session(request: Request, persona: Optional[str] = None, faceId: Optional[str] = None):
    """Create a Simli Compose session token using faceId (Compose model).

    Resolution priority:
    1) explicit faceId query/body
    2) persona -> SIMLI_FACE_ID_{PERSONA} env
    3) persona -> built-in mapping from /personas
    """
    # Sanitize API key
    api_key = (os.getenv("SIMLI_API_KEY") or "").strip()
    while api_key.startswith("="):
        api_key = api_key[1:].lstrip()

    # Also parse JSON body (POST)
    try:
        if request.method.upper() == "POST" and request.headers.get("content-type", "").startswith("application/json"):
            body = await request.json()
            body_face = body.get("faceId") or body.get("face")
            body_persona = body.get("persona") or body.get("name")
            if not faceId and body_face:
                faceId = body_face
            if not persona and body_persona:
                persona = body_persona
    except Exception:
        pass

    # Normalize persona
    if persona:
        norm = persona.strip().lower()
        persona = {
            "hoosier": "indiana",
            "indiana-oracle": "indiana",
            "indiana_ai": "indiana",
            "indiana": "indiana",
            "kurt": "vonnegut",
            "vonnegut": "vonnegut",
            "bigfoot": "bigfoot",
        }.get(norm, norm)

    # Resolve faceId - CHECK ENV FIRST, then builtin mapping
    if not faceId and persona:
        env_key = f"SIMLI_FACE_ID_{persona.upper()}"
        faceId = os.getenv(env_key)
        logger.info(f"Checking {env_key}: {faceId}")
    if not faceId and persona:
        # Built-in mapping - UPDATED WITH CORRECT AGENT IDs  
        builtin = {
            "bigfoot": "4a857f92-feee-4b70-b973-290baec4d545",
            "indiana": "76ed1ae8-720c-45de-918c-cac46984412d", 
            "vonnegut": "7bcb45a5-839c-4f1a-b6f9-4ebcdf457264",
        }
        faceId = builtin.get(persona)
        logger.info(f"Using builtin faceId for {persona}: {faceId}")

    if not api_key:
        logger.error("SIMLI_API_KEY not set or empty")
        return JSONResponse(status_code=400, content={
            "error": "SIMLI_API_KEY not set",
            "message": "Set SIMLI_API_KEY in environment to mint compose session tokens"
        })
    if not faceId:
        logger.error(f"faceId not resolved for persona {persona}. Checked env var and builtin mapping.")
        return JSONResponse(status_code=400, content={
            "error": "faceId not resolved", 
            "message": f"Provide faceId or persona (with SIMLI_FACE_ID_{persona.upper()} set)",
            "debug": f"persona={persona}, env_key=SIMLI_FACE_ID_{persona.upper()}"
        })

    url = "https://api.simli.ai/startAudioToVideoSession"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers={"Content-Type": "application/json"},
                json={"apiKey": api_key, "faceId": faceId},
                timeout=15,
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    return JSONResponse(status_code=resp.status, content={
                        "error": data,
                        "message": "Failed to create Simli Compose session"
                    })
                # Expect a token field; pass faceId back for client embed
                token = data.get("session_token") or data.get("token")
                if not token:
                    return JSONResponse(status_code=500, content={
                        "error": data,
                        "message": "Compose token not found in response"
                    })
                return {"token": token, "faceId": faceId, "source": "compose"}
    except Exception as e:
        logger.error(f"Simli compose session error: {e}")
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "Error while creating Simli Compose session"
        })

@app.post("/simli-compose/speak")
async def simli_compose_speak(request: dict):
    """Send text to speak through Simli Compose session"""
    try:
        persona = request.get("persona", "indiana")
        text = request.get("text", "")
        
        if not text:
            return JSONResponse(status_code=400, content={
                "error": "No text provided",
                "message": "Text is required for speech"
            })
        
        logger.info(f"Compose speak request for {persona}: {text[:50]}...")
        
        # For now, just acknowledge the request
        # In a full implementation, this would send the text to the active Compose session
        return {
            "success": True,
            "message": f"Speech queued for {persona}",
            "text": text,
            "persona": persona
        }
        
    except Exception as e:
        logger.error(f"Compose speak error: {e}")
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "Error sending speech to Compose session"
        })

@app.get("/simli-token")
@app.post("/simli-token")
async def create_simli_session_token(request: Request, agentId: Optional[str] = None, persona: Optional[str] = None):
    """Create a short-lived Simli session token using SIMLI_API_KEY.

    Priority of agent selection:
    1) explicit query param agentId
    2) persona→agent mapping from /personas
    3) env SIMLI_AGENT_ID or SIMLI_FACE_ID
    4) default hoosier fallback id
    """
    api_key = (os.getenv("SIMLI_API_KEY") or "").strip()
    # Remove any accidental leading equals signs and stray whitespace
    while api_key.startswith("="):
        api_key = api_key[1:].lstrip()
    logger.info(f"DEBUG: SIMLI_API_KEY raw = {repr(os.getenv('SIMLI_API_KEY'))}")
    logger.info(f"DEBUG: SIMLI_API_KEY sanitized = {repr(api_key)}")

    # Try to read persona/agentId from JSON body as well (POST)
    try:
        if request.method.upper() == "POST" and request.headers.get("content-type", "").startswith("application/json"):
            body = await request.json()
            body_agent = body.get("agentId") or body.get("agent")
            body_persona = body.get("persona") or body.get("name")
            if not agentId and body_agent:
                agentId = body_agent
            if not persona and body_persona:
                persona = body_persona
    except Exception:
        pass

    # Normalize persona and synonyms
    if persona:
        norm = persona.strip().lower()
        persona = {
            "hoosier": "indiana",
            "indiana-oracle": "indiana",
            "indiana_ai": "indiana",
            "indiana": "indiana",
            "kurt": "vonnegut",
            "vonnegut": "vonnegut",
            "bigfoot": "bigfoot",
        }.get(norm, norm)

    # Resolve agent ID with strict fallbacks (never return null)
    resolved_agent_id = None
    if agentId:
        resolved_agent_id = agentId
    elif persona:
        # Allow per-persona overrides via SIMLI_AGENT_ID_INDIANA / _VONNEGUT / _BIGFOOT
        env_key = f"SIMLI_AGENT_ID_{persona.upper()}"
        resolved_agent_id = os.getenv(env_key)
        if not resolved_agent_id:
            resolved_agent_id = os.getenv("SIMLI_AGENT_ID")
    else:
        resolved_agent_id = os.getenv("SIMLI_AGENT_ID")

    if not resolved_agent_id:
        return JSONResponse(status_code=400, content={
            "error": "SIMLI_AGENT_ID not configured",
            "message": "Provide agentId in query/body, or set SIMLI_AGENT_ID (or SIMLI_AGENT_ID_{INDIANA|VONNEGUT|BIGFOOT}) in environment."
        })

    # If an explicit session token is configured, return it (legacy behavior)
    configured_session_token = os.getenv("SIMLI_TOKEN")
    if configured_session_token:  # Use session token if available, include agentId
        return {"token": configured_session_token, "agentId": resolved_agent_id, "source": "env_session_token"}

    if not api_key:
        return JSONResponse(status_code=400, content={
            "error": "SIMLI_API_KEY not set",
            "message": "Set SIMLI_API_KEY in environment to let the backend mint session tokens"
        })

    url = "https://api.simli.ai/createE2ESessionToken"
    try:
        async with aiohttp.ClientSession() as session:
            async with session.post(
                url,
                headers={
                    "Content-Type": "application/json",
                },
                json={"simliAPIKey": api_key},  # Confirmed working format
                timeout=15,
            ) as resp:
                data = await resp.json()
                if resp.status != 200:
                    # Fallback: if SIMLI_TOKEN is configured, return it so frontend can proceed
                    env_token = os.getenv("SIMLI_TOKEN")
                    if env_token:
                        logger.warning(f"Simli API returned {resp.status}; falling back to SIMLI_TOKEN from env")
                        return {"token": env_token, "agentId": resolved_agent_id, "source": "env_fallback", "api_status": resp.status, "api_error": data}
                    return JSONResponse(status_code=resp.status, content={
                        "error": data,
                        "message": "Failed to create Simli session token"
                    })
                # API returns session_token field (confirmed)
                token = data.get("session_token")
                if not token:
                    return JSONResponse(status_code=500, content={
                        "error": data,
                        "message": "Simli token not found in response"
                    })
                # Return both token and agentId - widget needs both
                return {"token": token, "agentId": resolved_agent_id, "source": "api"}
    except Exception as e:
        logger.error(f"Simli token generation error: {e}")
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "Error while creating Simli session token"
        })

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

@app.post("/test-vonnegut-text")
async def test_vonnegut_text(request: dict):
    """Test endpoint to directly send text to Vonnegut's enhanced RAG system"""
    try:
        text = request.get("text", "")
        if not text:
            return JSONResponse(status_code=400, content={"error": "No text provided"})
        
        logger.info(f"Testing Vonnegut with text: {text}")
        
        # Use persona RAG directly for text-to-text testing
        if hasattr(backend, 'persona_rag_system') and backend.persona_rag_system:
            response = await backend.persona_rag_system.get_persona_response("vonnegut", text)
            
            return {
                "success": True,
                "text_input": text,
                "vonnegut_response": response,
                "system": "enhanced_corpus",
                "message": "Using authentic Vonnegut corpus and personality"
            }
        else:
            return JSONResponse(status_code=503, content={
                "error": "Persona RAG system not available",
                "message": "Enhanced Vonnegut system not initialized"
            })
            
    except Exception as e:
        logger.error(f"Error in test-vonnegut-text endpoint: {e}")
        return JSONResponse(status_code=500, content={
            "error": str(e),
            "message": "Failed to process Vonnegut text"
        })

@app.get("/personas")
async def get_personas():
    """Get available personas and their configurations"""
    return {
        "personas": [
            {
                "id": "bigfoot",
                "name": "Brown County Bigfoot",
                "description": "Legendary cryptid storyteller of Indiana's forests",
                "simli_face_id": "4a857f92-feee-4b70-b973-290baec4d545",
                "voice": "stock-simli",
                "knowledge": "cryptid-folklore"
            },
            {
                "id": "indiana", 
                "name": "Hoosier Oracle",
                "description": "Eternal consciousness of Indiana's history and culture",
                "simli_face_id": "76ed1ae8-720c-45de-918c-cac46984412d",
                "voice": "elevenlabs-hoosier",
                "knowledge": "indiana-history"
            },
            {
                "id": "vonnegut",
                "name": "Kurt Vonnegut", 
                "description": "Indianapolis author with dark humor and humanist wisdom",
                "simli_face_id": "7bcb45a5-839c-4f1a-b6f9-4ebcdf457264",
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