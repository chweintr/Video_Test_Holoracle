"""
WebSocket voice conversation server for the Indiana Oracle system.
Handles real-time voice input/output with VAD and TTS integration.
"""

import asyncio
import websockets
import json
import logging
import base64
import io
from typing import Dict, Optional, List
from pathlib import Path
import numpy as np
import soundfile as sf
from datetime import datetime

# Import local modules
from vad_handler import VADHandler
from faq_router import FAQRouter
from vonnegut_chatbot import VonnegutChatbot
from local_tts_lite import LocalTTSHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VoiceConversationServer:
    def __init__(self, host: str = "localhost", port: int = 7081):
        self.host = host
        self.port = port
        
        # Initialize components
        try:
            self.vad_handler = VADHandler()
            logger.info("VAD handler initialized")
        except Exception as e:
            logger.error(f"Error initializing VAD handler: {e}")
            self.vad_handler = None
        
        try:
            self.faq_router = FAQRouter()
            logger.info("FAQ router created (will initialize async)")
        except Exception as e:
            logger.error(f"Error creating FAQ router: {e}")
            self.faq_router = None
        
        try:
            self.vonnegut_chatbot = VonnegutChatbot()
            logger.info("Vonnegut chatbot initialized")
        except Exception as e:
            logger.error(f"Error initializing chatbot: {e}")
            self.vonnegut_chatbot = None
        
        try:
            self.local_tts = LocalTTSHandler()
            logger.info("Local TTS created (will initialize async)")
        except Exception as e:
            logger.error(f"Error creating TTS: {e}")
            self.local_tts = None
        
        # Connected clients
        self.clients: Dict[str, Dict] = {}
        
        # Default voice settings for hologram
        self.voice_settings = {
            'speed': 140,
            'volume': 0.9,
            'intensity': 1.0,
            'emotion': 0.8
        }
        
        # Audio configuration
        self.sample_rate = 16000  # Standard for VAD
        self.chunk_duration = 0.5  # seconds
        self.chunk_size = int(self.sample_rate * self.chunk_duration)
        
        logger.info(f"Voice server initialized on {host}:{port}")
    
    async def register_client(self, websocket) -> str:
        """Register a new client connection."""
        client_id = f"client_{len(self.clients)}_{datetime.now().timestamp()}"
        
        self.clients[client_id] = {
            'websocket': websocket,
            'connected_at': datetime.now(),
            'audio_buffer': [],
            'conversation_state': 'idle',  # idle, listening, processing, speaking
            'session_data': {}
        }
        
        logger.info(f"Client registered: {client_id}")
        return client_id
    
    async def unregister_client(self, client_id: str):
        """Unregister a client connection."""
        if client_id in self.clients:
            del self.clients[client_id]
            logger.info(f"Client unregistered: {client_id}")
    
    async def send_message(self, client_id: str, message: Dict):
        """Send message to a specific client."""
        if client_id not in self.clients:
            return
        
        try:
            websocket = self.clients[client_id]['websocket']
            await websocket.send(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending message to {client_id}: {e}")
            await self.unregister_client(client_id)
    
    async def broadcast_message(self, message: Dict):
        """Broadcast message to all connected clients."""
        for client_id in list(self.clients.keys()):
            await self.send_message(client_id, message)
    
    def decode_audio_data(self, audio_data: str) -> np.ndarray:
        """Decode base64 audio data to numpy array."""
        try:
            # Decode base64
            audio_bytes = base64.b64decode(audio_data)
            
            # Convert to numpy array (assuming 16-bit PCM)
            audio_np = np.frombuffer(audio_bytes, dtype=np.int16)
            
            # Normalize to [-1, 1]
            audio_float = audio_np.astype(np.float32) / 32768.0
            
            return audio_float
        except Exception as e:
            logger.error(f"Error decoding audio data: {e}")
            return np.array([])
    
    def encode_audio_data(self, audio: np.ndarray) -> str:
        """Encode numpy array to base64 audio data."""
        try:
            # Convert to 16-bit PCM
            audio_int16 = (audio * 32767).astype(np.int16)
            
            # Convert to bytes
            audio_bytes = audio_int16.tobytes()
            
            # Encode to base64
            audio_b64 = base64.b64encode(audio_bytes).decode('utf-8')
            
            return audio_b64
        except Exception as e:
            logger.error(f"Error encoding audio data: {e}")
            return ""
    
    async def process_audio_chunk(self, client_id: str, audio_data: str):
        """Process incoming audio chunk from client."""
        try:
            # Decode audio
            audio_chunk = self.decode_audio_data(audio_data)
            
            if len(audio_chunk) == 0:
                return
            
            # Add to client's audio buffer
            self.clients[client_id]['audio_buffer'].extend(audio_chunk)
            
            # Check for speech using VAD
            buffer = np.array(self.clients[client_id]['audio_buffer'])
            
            if len(buffer) >= self.chunk_size:
                # Process chunk with VAD
                speech_prob = await self.vad_handler.detect_speech(buffer[-self.chunk_size:])
                
                # Send VAD result to client
                await self.send_message(client_id, {
                    'type': 'vad_result',
                    'speech_probability': float(speech_prob),
                    'is_speech': speech_prob > 0.5
                })
                
                # If speech detected and enough audio collected
                if speech_prob > 0.5 and len(buffer) > self.sample_rate * 2:  # 2 seconds minimum
                    await self.process_speech_segment(client_id, buffer)
        
        except Exception as e:
            logger.error(f"Error processing audio chunk for {client_id}: {e}")
    
    async def process_speech_segment(self, client_id: str, audio_buffer: np.ndarray):
        """Process a complete speech segment."""
        try:
            # Update client state
            self.clients[client_id]['conversation_state'] = 'processing'
            
            await self.send_message(client_id, {
                'type': 'status',
                'status': 'processing_speech'
            })
            
            # Transcribe audio (placeholder - integrate with your STT service)
            transcription = await self.transcribe_audio(audio_buffer)
            
            if not transcription:
                await self.send_message(client_id, {
                    'type': 'error',
                    'message': 'Could not transcribe audio'
                })
                return
            
            logger.info(f"Transcribed: {transcription}")
            
            # Send transcription to client
            await self.send_message(client_id, {
                'type': 'transcription',
                'text': transcription
            })
            
            # Route through FAQ system first (if available)
            faq_response = None
            if self.faq_router:
                try:
                    faq_response = await self.faq_router.check_faq(transcription)
                except Exception as e:
                    logger.error(f"Error checking FAQ: {e}")
                    faq_response = None
            
            if faq_response:
                # Use FAQ response
                response_text = faq_response['text']
                audio_file = faq_response.get('audio_file')
                
                await self.send_message(client_id, {
                    'type': 'faq_response',
                    'text': response_text,
                    'confidence': faq_response.get('confidence', 0.0)
                })
            else:
                # Route to main chatbot
                response_text = await self.get_chatbot_response(transcription, client_id)
                audio_file = None
            
            # Generate or load TTS audio
            response_audio = None
            
            if audio_file and Path(audio_file).exists():
                # Use pre-generated FAQ audio
                response_audio = await self.load_audio_file(audio_file)
                logger.info(f"Loaded pre-generated audio: {audio_file}")
            else:
                # Generate new TTS audio
                logger.info("Generating TTS audio for response...")
                response_audio = await self.generate_tts_audio(response_text)
                
                if response_audio is not None:
                    logger.info(f"TTS audio generated: {len(response_audio)/self.sample_rate:.2f}s")
                else:
                    logger.error("TTS audio generation failed")
            
            # Send response to client
            if response_audio is not None:
                logger.info("Encoding audio for browser...")
                audio_b64 = self.encode_audio_data(response_audio)
                logger.info(f"Audio encoded: {len(audio_b64)} characters base64")
                
                await self.send_message(client_id, {
                    'type': 'voice_response',
                    'text': response_text,
                    'audio_data': audio_b64,
                    'sample_rate': self.sample_rate
                })
                logger.info("Voice response sent to client")
            else:
                logger.warning("No audio generated, sending text-only response")
                await self.send_message(client_id, {
                    'type': 'text_response',
                    'text': response_text
                })
            
            # Clear audio buffer and reset state
            self.clients[client_id]['audio_buffer'] = []
            self.clients[client_id]['conversation_state'] = 'idle'
            
        except Exception as e:
            logger.error(f"Error processing speech segment for {client_id}: {e}")
            await self.send_message(client_id, {
                'type': 'error',
                'message': 'Error processing speech'
            })
    
    async def transcribe_audio(self, audio: np.ndarray) -> Optional[str]:
        """Transcribe audio to text using STT service."""
        try:
            if len(audio) == 0:
                return None
            
            # Try OpenAI Whisper if API key is available
            if hasattr(self, 'vonnegut_chatbot') and self.vonnegut_chatbot and self.vonnegut_chatbot.client:
                return await self.transcribe_with_openai_whisper(audio)
            else:
                # Fallback: Use browser speech recognition instead
                logger.warning("No OpenAI API key - audio transcription disabled. Use browser speech recognition.")
                return None
            
        except Exception as e:
            logger.error(f"Error in transcription: {e}")
            return None
    
    async def transcribe_with_openai_whisper(self, audio: np.ndarray) -> Optional[str]:
        """Transcribe audio using OpenAI Whisper API."""
        try:
            import tempfile
            import os
            
            # Save audio to temporary WAV file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                # Write audio data to file
                sf.write(temp_path, audio, self.sample_rate)
                
                # Transcribe using OpenAI Whisper
                with open(temp_path, 'rb') as audio_file:
                    transcript = self.vonnegut_chatbot.client.audio.transcriptions.create(
                        model="whisper-1",
                        file=audio_file,
                        language="en"
                    )
                
                transcription_text = transcript.text.strip()
                logger.info(f"Whisper transcription: {transcription_text}")
                return transcription_text
                
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Error in Whisper transcription: {e}")
            return None
    
    async def process_text_input(self, client_id: str, text: str):
        """Process text input directly (from browser speech recognition)."""
        try:
            # Update client state
            self.clients[client_id]['conversation_state'] = 'processing'
            
            await self.send_message(client_id, {
                'type': 'status',
                'status': 'processing'
            })
            
            # Route directly to main chatbot (skip FAQ system)
            response_text = await self.get_chatbot_response(text, client_id)
            
            # Always generate TTS audio for phone call experience
            logger.info("Generating TTS audio for response...")
            response_audio = await self.generate_tts_audio(response_text)
            
            if response_audio is not None:
                logger.info(f"TTS audio generated: {len(response_audio)/self.sample_rate:.2f}s")
                
                # Encode and send voice response with audio
                audio_b64 = self.encode_audio_data(response_audio)
                
                await self.send_message(client_id, {
                    'type': 'voice_response',
                    'text': response_text,
                    'audio_data': audio_b64,
                    'sample_rate': self.sample_rate
                })
                logger.info("Voice response with audio sent to client")
            else:
                logger.warning("No audio generated, sending text-only response")
                await self.send_message(client_id, {
                    'type': 'text_response',
                    'text': response_text
                })
            
            # Update conversation state
            self.clients[client_id]['conversation_state'] = 'idle'
            
        except Exception as e:
            logger.error(f"Error processing text input for {client_id}: {e}")
            await self.send_message(client_id, {
                'type': 'error',
                'message': 'Error processing your message'
            })
    
    async def get_chatbot_response(self, text: str, client_id: str) -> str:
        """Get response from Vonnegut chatbot system."""
        try:
            # Get conversation history for this client
            conversation_history = self.clients[client_id].get('conversation_history', [])
            
            # Generate Vonnegut response
            response = await self.vonnegut_chatbot.generate_response_async(text, conversation_history)
            
            # Update conversation history
            if 'conversation_history' not in self.clients[client_id]:
                self.clients[client_id]['conversation_history'] = []
            
            self.clients[client_id]['conversation_history'].extend([
                {"role": "user", "content": text},
                {"role": "assistant", "content": response}
            ])
            
            # Keep only last 10 exchanges (20 messages)
            if len(self.clients[client_id]['conversation_history']) > 20:
                self.clients[client_id]['conversation_history'] = self.clients[client_id]['conversation_history'][-20:]
            
            return response
            
        except Exception as e:
            logger.error(f"Error getting chatbot response: {e}")
            return "Listen: I seem to be having trouble connecting to my thoughts right now. So it goes."
    
    async def generate_tts_audio(self, text: str) -> Optional[np.ndarray]:
        """Generate TTS audio using local TTS handler."""
        try:
            audio_data = await self.local_tts.synthesize_speech(text)
            
            if audio_data is not None:
                # Send to Audio2Face if available
                if hasattr(self, 'audio2face') and self.audio2face:
                    try:
                        await self.audio2face.process_tts_with_a2f(text, audio_data)
                    except Exception as e:
                        logger.warning(f"Audio2Face processing failed: {e}")
                
                # Send to TouchDesigner if available
                if hasattr(self, 'td_bridge') and self.td_bridge:
                    try:
                        self.td_bridge.send_audio_features(audio_data)
                    except Exception as e:
                        logger.warning(f"TouchDesigner bridge failed: {e}")
            
            return audio_data
            
        except Exception as e:
            logger.error(f"Error generating TTS audio: {e}")
            return None
    
    
    async def load_audio_file(self, audio_path: str) -> Optional[np.ndarray]:
        """Load pre-generated audio file."""
        try:
            audio, sr = sf.read(audio_path)
            
            # Resample if needed
            if sr != self.sample_rate:
                # Simple resampling (use librosa for better quality)
                ratio = self.sample_rate / sr
                new_length = int(len(audio) * ratio)
                audio = np.interp(
                    np.linspace(0, len(audio), new_length),
                    np.arange(len(audio)),
                    audio
                )
            
            return audio
            
        except Exception as e:
            logger.error(f"Error loading audio file {audio_path}: {e}")
            return None
    
    async def handle_client_message(self, client_id: str, message: Dict):
        """Handle incoming message from client."""
        try:
            message_type = message.get('type')
            
            if message_type == 'audio_chunk':
                await self.process_audio_chunk(client_id, message.get('data', ''))
            
            elif message_type == 'start_listening':
                self.clients[client_id]['conversation_state'] = 'listening'
                self.clients[client_id]['audio_buffer'] = []
                await self.send_message(client_id, {
                    'type': 'status',
                    'status': 'listening'
                })
            
            elif message_type == 'stop_listening':
                self.clients[client_id]['conversation_state'] = 'idle'
                
                # Process any remaining audio
                buffer = np.array(self.clients[client_id]['audio_buffer'])
                if len(buffer) > self.sample_rate:  # At least 1 second
                    await self.process_speech_segment(client_id, buffer)
            
            elif message_type == 'transcribed_text':
                # Handle text input directly (from browser speech recognition)
                text = message.get('text', '').strip()
                if text:
                    logger.info(f"Received transcribed text from {client_id}: {text}")
                    await self.process_text_input(client_id, text)
            
            elif message_type == 'voice_settings':
                # Update voice settings for TTS and hologram
                settings = message.get('settings', {})
                self.voice_settings.update(settings)
                logger.info(f"Voice settings updated: {self.voice_settings}")
                
                # Apply settings to TTS engine
                await self.apply_voice_settings_to_tts()
                
                await self.send_message(client_id, {
                    'type': 'settings_updated',
                    'settings': self.voice_settings
                })
            
            elif message_type == 'hologram_audio':
                # Forward hologram data to display integration systems
                await self.send_to_hologram_system(message)
            
            elif message_type == 'ping':
                await self.send_message(client_id, {'type': 'pong'})
            
            else:
                logger.warning(f"Unknown message type from {client_id}: {message_type}")
        
        except Exception as e:
            logger.error(f"Error handling message from {client_id}: {e}")
    
    async def client_handler(self, websocket, path):
        """Handle individual client connections."""
        client_id = await self.register_client(websocket)
        
        try:
            # Send welcome message
            await self.send_message(client_id, {
                'type': 'welcome',
                'client_id': client_id,
                'server_info': {
                    'sample_rate': self.sample_rate,
                    'chunk_size': self.chunk_size,
                    'supported_formats': ['pcm16']
                }
            })
            
            # Handle messages
            async for message_raw in websocket:
                try:
                    message = json.loads(message_raw)
                    await self.handle_client_message(client_id, message)
                except json.JSONDecodeError:
                    logger.error(f"Invalid JSON from {client_id}")
                except Exception as e:
                    logger.error(f"Error processing message from {client_id}: {e}")
        
        except websockets.exceptions.ConnectionClosed:
            logger.info(f"Client {client_id} disconnected")
        except Exception as e:
            logger.error(f"Error with client {client_id}: {e}")
        finally:
            await self.unregister_client(client_id)
    
    async def start_server(self):
        """Start the WebSocket server."""
        logger.info(f"Starting voice conversation server on {self.host}:{self.port}")
        
        # Initialize async components
        if self.faq_router and not getattr(self.faq_router, 'initialized', True):
            try:
                await self.faq_router.initialize()
                logger.info("FAQ router initialized")
            except Exception as e:
                logger.error(f"Error initializing FAQ router: {e}")
                self.faq_router = None
        
        if self.local_tts and not getattr(self.local_tts, 'initialized', True):
            try:
                await self.local_tts.initialize_engines()
                logger.info("Local TTS initialized")
            except Exception as e:
                logger.error(f"Error initializing TTS: {e}")
                # Keep TTS but mark as not fully initialized
        
        # Start WebSocket server
        server = await websockets.serve(
            self.client_handler,
            self.host,
            self.port,
            ping_interval=30,
            ping_timeout=10
        )
        
        logger.info(f"Voice server running on ws://{self.host}:{self.port}")
        
        # Keep server running
        await server.wait_closed()
    
    async def apply_voice_settings_to_tts(self):
        """Apply current voice settings to TTS engine."""
        try:
            if self.local_tts and self.local_tts.pyttsx3_engine:
                # Apply speed setting
                self.local_tts.pyttsx3_engine.setProperty('rate', self.voice_settings['speed'])
                
                # Apply volume setting 
                self.local_tts.pyttsx3_engine.setProperty('volume', self.voice_settings['volume'])
                
                logger.info(f"Applied TTS settings: speed={self.voice_settings['speed']}, volume={self.voice_settings['volume']}")
        except Exception as e:
            logger.error(f"Error applying voice settings to TTS: {e}")
    
    async def send_to_hologram_system(self, hologram_data):
        """Send hologram audio data to display integration systems."""
        try:
            # Extract audio characteristics for particle control
            intensity = hologram_data.get('intensity', 1.0)
            emotion = hologram_data.get('emotion', 0.8)
            volume = hologram_data.get('volume', 0.9)
            
            # Log hologram data for integration with TouchDesigner/OSC
            logger.info(f"Hologram particle data: intensity={intensity}, emotion={emotion}, volume={volume}")
            
            # TODO: Send to TouchDesigner via OSC bridge
            # TODO: Send to Audio2Face integration
            # TODO: Send to any other display systems
            
            # For now, just broadcast to all clients for debugging
            await self.broadcast_message({
                'type': 'hologram_data',
                'intensity': intensity,
                'emotion': emotion,
                'volume': volume,
                'timestamp': hologram_data.get('timestamp')
            })
            
        except Exception as e:
            logger.error(f"Error sending to hologram system: {e}")
    
    def run(self):
        """Run the server."""
        try:
            asyncio.run(self.start_server())
        except KeyboardInterrupt:
            logger.info("Server stopped by user")
        except Exception as e:
            logger.error(f"Server error: {e}")

def main():
    """Start the voice conversation server."""
    server = VoiceConversationServer()
    server.run()

if __name__ == "__main__":
    main()