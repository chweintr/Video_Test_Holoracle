"""
NVIDIA Audio2Face Integration for Indiana Oracle Voice System
Sends TTS audio to Audio2Face for real-time facial animation and lip sync
"""

import asyncio
import aiohttp
import base64
import json
import numpy as np
import soundfile as sf
from pathlib import Path
from typing import Optional, Dict, Any
import logging
from io import BytesIO
import struct

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Audio2FaceIntegration:
    def __init__(self, config_path: str = "../config/audio2face_config.json"):
        """
        Initialize Audio2Face integration.
        
        Args:
            config_path: Path to configuration file with API credentials
        """
        self.config = self.load_config(config_path)
        self.api_key = self.config['audio2face']['api_key']
        self.endpoint = self.config['audio2face'].get('endpoint', 'http://localhost:8011/A2F/Player/StreamAudio')
        self.instance_name = self.config['audio2face'].get('instance_name', 'Audio2Face')
        
        # Audio settings
        self.sample_rate = 22050  # Match TTS output
        self.emotion_map = {
            'neutral': {'arousal': 0.5, 'valence': 0.5},
            'thoughtful': {'arousal': 0.3, 'valence': 0.4},
            'sardonic': {'arousal': 0.4, 'valence': 0.3},
            'melancholic': {'arousal': 0.2, 'valence': 0.2},
            'amused': {'arousal': 0.6, 'valence': 0.7}
        }
        
        # WebSocket for real-time communication
        self.ws_endpoint = self.config['audio2face'].get('ws_endpoint', 'ws://localhost:8011/A2F/Stream')
        self.ws_connection = None
        
        logger.info("Audio2Face integration initialized")
    
    def load_config(self, config_path: str) -> Dict:
        """Load configuration from JSON file."""
        config_file = Path(config_path)
        if not config_file.exists():
            # Create default config
            default_config = {
                "audio2face": {
                    "api_key": "your-api-key-here",
                    "endpoint": "http://localhost:8011/A2F/Player/StreamAudio",
                    "instance_name": "Audio2Face"
                }
            }
            config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(config_file, 'w') as f:
                json.dump(default_config, f, indent=2)
            logger.warning(f"Created default config at {config_path}")
            
        with open(config_file, 'r') as f:
            return json.load(f)
    
    async def connect_websocket(self):
        """Establish WebSocket connection for real-time streaming."""
        try:
            import websockets
            self.ws_connection = await websockets.connect(self.ws_endpoint)
            logger.info("Connected to Audio2Face WebSocket")
            
            # Send initial configuration
            config_msg = {
                "type": "configure",
                "api_key": self.api_key,
                "instance": self.instance_name,
                "sample_rate": self.sample_rate
            }
            await self.ws_connection.send(json.dumps(config_msg))
            
        except Exception as e:
            logger.error(f"Failed to connect WebSocket: {e}")
            self.ws_connection = None
    
    async def send_audio_to_a2f(self, audio_data: np.ndarray, emotion: str = "neutral") -> bool:
        """
        Send audio data to Audio2Face for lip sync animation.
        
        Args:
            audio_data: Audio samples as numpy array
            emotion: Emotional state for expression mapping
            
        Returns:
            Success status
        """
        try:
            # Prepare audio data
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio
            audio_data = np.clip(audio_data, -1.0, 1.0)
            
            # If WebSocket is available, use real-time streaming
            if self.ws_connection:
                return await self.stream_audio_realtime(audio_data, emotion)
            else:
                # Fall back to HTTP API
                return await self.send_audio_http(audio_data, emotion)
                
        except Exception as e:
            logger.error(f"Error sending audio to Audio2Face: {e}")
            return False
    
    async def stream_audio_realtime(self, audio_data: np.ndarray, emotion: str) -> bool:
        """Stream audio in real-time via WebSocket."""
        try:
            # Get emotion parameters
            emotion_params = self.emotion_map.get(emotion, self.emotion_map['neutral'])
            
            # Chunk audio for streaming (100ms chunks)
            chunk_size = int(self.sample_rate * 0.1)  # 100ms
            
            for i in range(0, len(audio_data), chunk_size):
                chunk = audio_data[i:i + chunk_size]
                
                # Convert to bytes
                audio_bytes = chunk.tobytes()
                
                # Create message
                message = {
                    "type": "audio_chunk",
                    "data": base64.b64encode(audio_bytes).decode('utf-8'),
                    "timestamp": i / self.sample_rate,
                    "emotion": emotion_params
                }
                
                await self.ws_connection.send(json.dumps(message))
                
                # Small delay to simulate real-time
                await asyncio.sleep(0.05)
            
            # Send end-of-stream marker
            await self.ws_connection.send(json.dumps({"type": "end_stream"}))
            
            logger.info(f"Streamed {len(audio_data)/self.sample_rate:.2f}s of audio to Audio2Face")
            return True
            
        except Exception as e:
            logger.error(f"Error in real-time streaming: {e}")
            return False
    
    async def send_audio_http(self, audio_data: np.ndarray, emotion: str) -> bool:
        """Send audio via HTTP API (fallback method)."""
        try:
            # Convert to WAV format in memory
            buffer = BytesIO()
            sf.write(buffer, audio_data, self.sample_rate, format='WAV')
            buffer.seek(0)
            wav_data = buffer.read()
            
            # Prepare request
            headers = {
                'Authorization': f'Bearer {self.api_key}',
                'Content-Type': 'audio/wav'
            }
            
            # Add emotion metadata
            emotion_params = self.emotion_map.get(emotion, self.emotion_map['neutral'])
            params = {
                'instance': self.instance_name,
                'arousal': emotion_params['arousal'],
                'valence': emotion_params['valence']
            }
            
            # Send request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.endpoint,
                    data=wav_data,
                    headers=headers,
                    params=params
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info(f"Audio sent to Audio2Face: {result}")
                        return True
                    else:
                        error = await response.text()
                        logger.error(f"Audio2Face API error: {response.status} - {error}")
                        return False
                        
        except Exception as e:
            logger.error(f"Error sending audio via HTTP: {e}")
            return False
    
    async def send_blendshape_data(self, blendshapes: Dict[str, float]):
        """
        Send manual blendshape values for fine control.
        
        Args:
            blendshapes: Dictionary of blendshape names and values (0-1)
        """
        try:
            if self.ws_connection:
                message = {
                    "type": "blendshapes",
                    "data": blendshapes,
                    "timestamp": asyncio.get_event_loop().time()
                }
                await self.ws_connection.send(json.dumps(message))
            else:
                logger.warning("No WebSocket connection for blendshape data")
                
        except Exception as e:
            logger.error(f"Error sending blendshape data: {e}")
    
    def analyze_text_emotion(self, text: str) -> str:
        """
        Analyze text to determine emotional tone for facial expression.
        
        Args:
            text: The text being spoken
            
        Returns:
            Emotion label
        """
        text_lower = text.lower()
        
        # Simple keyword-based emotion detection
        if any(word in text_lower for word in ['sad', 'melancholy', 'death', 'gone']):
            return 'melancholic'
        elif any(word in text_lower for word in ['think', 'wonder', 'perhaps', 'maybe']):
            return 'thoughtful'
        elif any(word in text_lower for word in ['funny', 'laugh', 'joke', 'amusing']):
            return 'amused'
        elif any(word in text_lower for word in ['ironic', 'typical', 'figures']):
            return 'sardonic'
        else:
            return 'neutral'
    
    async def process_tts_with_a2f(self, text: str, audio_data: np.ndarray) -> bool:
        """
        Process TTS output with Audio2Face integration.
        
        Args:
            text: The text that was spoken
            audio_data: The generated audio
            
        Returns:
            Success status
        """
        try:
            # Analyze emotion from text
            emotion = self.analyze_text_emotion(text)
            logger.info(f"Detected emotion: {emotion}")
            
            # Send to Audio2Face
            success = await self.send_audio_to_a2f(audio_data, emotion)
            
            # Send additional expression data based on punctuation
            if self.ws_connection:
                # Eyebrow raise on questions
                if '?' in text:
                    await self.send_blendshape_data({
                        'browInnerUp': 0.5,
                        'browOuterUp': 0.3
                    })
                
                # Slight smile on exclamations
                elif '!' in text:
                    await self.send_blendshape_data({
                        'mouthSmile': 0.3,
                        'cheekPuff': 0.1
                    })
            
            return success
            
        except Exception as e:
            logger.error(f"Error processing TTS with A2F: {e}")
            return False
    
    async def set_idle_animation(self):
        """Set idle animation when not speaking."""
        try:
            if self.ws_connection:
                # Subtle breathing animation
                message = {
                    "type": "idle_animation",
                    "preset": "breathing",
                    "intensity": 0.3
                }
                await self.ws_connection.send(json.dumps(message))
                
        except Exception as e:
            logger.error(f"Error setting idle animation: {e}")
    
    async def disconnect(self):
        """Clean up connections."""
        try:
            if self.ws_connection:
                await self.ws_connection.close()
                logger.info("Disconnected from Audio2Face")
        except Exception as e:
            logger.error(f"Error disconnecting: {e}")

# Integration with TouchDesigner
class TouchDesignerBridge:
    """Bridge between Audio2Face and TouchDesigner for particle effects."""
    
    def __init__(self, osc_port: int = 9000):
        """Initialize OSC communication with TouchDesigner."""
        try:
            from pythonosc import udp_client
            self.osc_client = udp_client.SimpleUDPClient("localhost", osc_port)
            self.enabled = True
            logger.info(f"TouchDesigner OSC bridge initialized on port {osc_port}")
        except ImportError:
            logger.warning("python-osc not installed. TouchDesigner bridge disabled.")
            self.enabled = False
    
    def send_audio_features(self, audio_data: np.ndarray):
        """Send audio analysis to TouchDesigner."""
        if not self.enabled:
            return
            
        try:
            # Simple audio analysis
            rms = np.sqrt(np.mean(audio_data**2))
            
            # Frequency analysis (simple version)
            fft = np.fft.rfft(audio_data)
            freqs = np.fft.rfftfreq(len(audio_data), 1/22050)
            
            # Band analysis
            low = np.mean(np.abs(fft[(freqs < 250)]))
            mid = np.mean(np.abs(fft[(freqs >= 250) & (freqs < 2000)]))
            high = np.mean(np.abs(fft[(freqs >= 2000)]))
            
            # Send to TouchDesigner
            self.osc_client.send_message("/audio/level", float(rms))
            self.osc_client.send_message("/audio/low", float(low))
            self.osc_client.send_message("/audio/mid", float(mid))
            self.osc_client.send_message("/audio/high", float(high))
            
        except Exception as e:
            logger.error(f"Error sending to TouchDesigner: {e}")
    
    def send_blendshapes(self, blendshapes: Dict[str, float]):
        """Send Audio2Face blendshapes to TouchDesigner."""
        if not self.enabled:
            return
            
        try:
            for name, value in blendshapes.items():
                self.osc_client.send_message(f"/a2f/blendshape/{name}", float(value))
        except Exception as e:
            logger.error(f"Error sending blendshapes: {e}")

# Example usage
async def test_audio2face():
    """Test Audio2Face integration."""
    # Initialize
    a2f = Audio2FaceIntegration()
    await a2f.connect_websocket()
    
    # Test with sample audio
    test_text = "Listen: So it goes. That's what I always say about these things."
    test_audio = np.sin(2 * np.pi * 440 * np.linspace(0, 2, 44100))  # 2 second test tone
    
    # Process with Audio2Face
    success = await a2f.process_tts_with_a2f(test_text, test_audio)
    
    if success:
        logger.info("Audio2Face test successful!")
    else:
        logger.error("Audio2Face test failed")
    
    # Cleanup
    await a2f.disconnect()

if __name__ == "__main__":
    asyncio.run(test_audio2face())