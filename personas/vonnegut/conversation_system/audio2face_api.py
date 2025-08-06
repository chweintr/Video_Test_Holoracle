"""
NVIDIA Audio2Face API Integration (Cloud Service)
Using NVIDIA's cloud API for facial animation from audio
"""

import asyncio
import aiohttp
import base64
import json
import numpy as np
from typing import Optional, Dict, Any, List
import logging
from pathlib import Path
import soundfile as sf
from io import BytesIO

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Audio2FaceAPI:
    def __init__(self, api_key: str = None):
        """
        Initialize Audio2Face API client.
        
        Args:
            api_key: NVIDIA API key (nvapi-...)
        """
        # Load API key from config if not provided
        if not api_key:
            config_path = Path("../config/audio2face_config.json")
            if config_path.exists():
                with open(config_path, 'r') as f:
                    config = json.load(f)
                    api_key = config['audio2face']['api_key']
        
        self.api_key = api_key
        self.base_url = "https://ai.api.nvidia.com/v1/a2f/generatemotion"
        
        # Audio settings
        self.sample_rate = 22050  # A2F API expects 16kHz or 22.05kHz
        
        logger.info("Audio2Face API client initialized")
    
    async def generate_facial_animation(self, 
                                      audio_data: np.ndarray, 
                                      emotion: str = "neutral",
                                      face_model: str = "mark") -> Optional[Dict]:
        """
        Generate facial animation data from audio using NVIDIA's API.
        
        Args:
            audio_data: Audio as numpy array
            emotion: Emotion preset (neutral, happy, sad, angry)
            face_model: Face model to use (mark, claire, etc.)
            
        Returns:
            Animation data with blendshapes and timing
        """
        try:
            # Convert audio to required format
            audio_bytes = self.prepare_audio(audio_data)
            
            # Prepare request
            headers = {
                "Authorization": f"Bearer {self.api_key}",
                "Content-Type": "application/json",
                "Accept": "application/json"
            }
            
            # Create request payload
            payload = {
                "audio": {
                    "content": base64.b64encode(audio_bytes).decode('utf-8'),
                    "encoding": "WAV",
                    "sample_rate": self.sample_rate
                },
                "face_params": {
                    "face_model": face_model,
                    "emotion": emotion,
                    "emotion_strength": 0.7,
                    "blink_frequency": 0.3  # Natural blinking
                },
                "output_format": "blendshapes"  # or "vertices" for mesh data
            }
            
            # Make API request
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                ) as response:
                    if response.status == 200:
                        result = await response.json()
                        logger.info("Successfully generated facial animation")
                        return self.parse_animation_data(result)
                    else:
                        error = await response.text()
                        logger.error(f"API error {response.status}: {error}")
                        return None
                        
        except Exception as e:
            logger.error(f"Error generating facial animation: {e}")
            return None
    
    def prepare_audio(self, audio_data: np.ndarray) -> bytes:
        """Convert audio to WAV format required by API."""
        # Ensure correct sample rate
        if len(audio_data.shape) > 1:
            audio_data = audio_data.mean(axis=1)  # Convert to mono
        
        # Normalize audio
        audio_data = np.clip(audio_data, -1.0, 1.0)
        
        # Convert to WAV bytes
        buffer = BytesIO()
        sf.write(buffer, audio_data, self.sample_rate, format='WAV', subtype='PCM_16')
        buffer.seek(0)
        
        return buffer.read()
    
    def parse_animation_data(self, api_response: Dict) -> Dict:
        """Parse API response into usable animation data."""
        try:
            animation_data = {
                "duration": api_response.get("duration", 0),
                "fps": api_response.get("fps", 30),
                "blendshapes": [],
                "metadata": api_response.get("metadata", {})
            }
            
            # Extract blendshape animation curves
            if "animation" in api_response:
                for frame in api_response["animation"]["frames"]:
                    frame_data = {
                        "time": frame["timestamp"],
                        "blendshapes": frame["blendshapes"],
                        "head_rotation": frame.get("head_rotation", [0, 0, 0]),
                        "eye_gaze": frame.get("eye_gaze", [0, 0])
                    }
                    animation_data["blendshapes"].append(frame_data)
            
            # Extract key blendshape channels
            animation_data["channels"] = {
                "jawOpen": [],
                "mouthSmile": [],
                "browInnerUp": [],
                "eyeBlink": []
            }
            
            for frame in animation_data["blendshapes"]:
                bs = frame["blendshapes"]
                animation_data["channels"]["jawOpen"].append(bs.get("jawOpen", 0))
                animation_data["channels"]["mouthSmile"].append(bs.get("mouthSmileLeft", 0))
                animation_data["channels"]["browInnerUp"].append(bs.get("browInnerUp", 0))
                animation_data["channels"]["eyeBlink"].append(bs.get("eyeBlinkLeft", 0))
            
            return animation_data
            
        except Exception as e:
            logger.error(f"Error parsing animation data: {e}")
            return None
    
    async def generate_from_text_and_audio(self, text: str, audio_data: np.ndarray) -> Optional[Dict]:
        """
        Generate animation with text context for better lip sync.
        
        Args:
            text: The spoken text
            audio_data: The audio data
            
        Returns:
            Animation data
        """
        # Analyze text for emotion
        emotion = self.analyze_emotion(text)
        
        # Generate animation
        animation = await self.generate_facial_animation(audio_data, emotion)
        
        if animation:
            # Add text-based enhancements
            animation["text"] = text
            animation["words"] = text.split()
            animation["emotion"] = emotion
            
        return animation
    
    def analyze_emotion(self, text: str) -> str:
        """Simple emotion detection from text."""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['sad', 'sorry', 'death', 'gone']):
            return 'sad'
        elif any(word in text_lower for word in ['happy', 'joy', 'wonderful', 'great']):
            return 'happy'
        elif any(word in text_lower for word in ['angry', 'mad', 'furious', 'damn']):
            return 'angry'
        else:
            return 'neutral'
    
    def export_to_json(self, animation_data: Dict, output_path: str):
        """Export animation data to JSON for use in other applications."""
        with open(output_path, 'w') as f:
            json.dump(animation_data, f, indent=2)
        logger.info(f"Exported animation to {output_path}")
    
    def export_to_csv(self, animation_data: Dict, output_path: str):
        """Export blendshape curves to CSV for import into 3D software."""
        import csv
        
        with open(output_path, 'w', newline='') as f:
            writer = csv.writer(f)
            
            # Header
            channels = list(animation_data["channels"].keys())
            writer.writerow(["time"] + channels)
            
            # Data
            num_frames = len(animation_data["blendshapes"])
            for i in range(num_frames):
                row = [animation_data["blendshapes"][i]["time"]]
                for channel in channels:
                    row.append(animation_data["channels"][channel][i])
                writer.writerow(row)
        
        logger.info(f"Exported animation curves to {output_path}")

# Integration with your voice system
class VoiceToFacebridge:
    """Bridge between TTS output and Audio2Face API."""
    
    def __init__(self, api_key: str = None):
        self.a2f_api = Audio2FaceAPI(api_key)
        self.animation_cache = {}
        
    async def process_response(self, text: str, audio_data: np.ndarray) -> Dict:
        """
        Process a voice response to generate facial animation.
        
        Args:
            text: The spoken text
            audio_data: TTS audio output
            
        Returns:
            Complete response package with audio and animation
        """
        # Check cache first
        cache_key = hash(text[:50])  # Simple cache key
        if cache_key in self.animation_cache:
            logger.info("Using cached animation")
            animation = self.animation_cache[cache_key]
        else:
            # Generate new animation
            animation = await self.a2f_api.generate_from_text_and_audio(text, audio_data)
            
            # Cache for common responses
            if animation and len(self.animation_cache) < 100:
                self.animation_cache[cache_key] = animation
        
        return {
            "text": text,
            "audio": audio_data,
            "animation": animation,
            "duration": len(audio_data) / 22050,
            "ready": animation is not None
        }
    
    def get_blendshape_at_time(self, animation: Dict, time: float) -> Dict:
        """Get interpolated blendshape values at specific time."""
        if not animation or not animation.get("blendshapes"):
            return {}
        
        frames = animation["blendshapes"]
        fps = animation.get("fps", 30)
        frame_num = int(time * fps)
        
        if frame_num >= len(frames):
            return frames[-1]["blendshapes"] if frames else {}
        
        return frames[frame_num]["blendshapes"]

# Example usage
async def test_audio2face_api():
    """Test the Audio2Face API integration."""
    # Initialize
    bridge = VoiceToFacebridge()
    
    # Test text and audio
    test_text = "Hi ho. Listen: So it goes. That's what I always say."
    
    # Generate simple test audio (replace with actual TTS)
    duration = 3.0
    t = np.linspace(0, duration, int(22050 * duration))
    test_audio = np.sin(2 * np.pi * 440 * t) * 0.3  # Simple tone
    
    # Process
    result = await bridge.process_response(test_text, test_audio)
    
    if result["animation"]:
        print("Animation generated successfully!")
        print(f"Duration: {result['animation']['duration']}s")
        print(f"FPS: {result['animation']['fps']}")
        print(f"Frames: {len(result['animation']['blendshapes'])}")
        
        # Export for testing
        bridge.a2f_api.export_to_json(result["animation"], "test_animation.json")
        bridge.a2f_api.export_to_csv(result["animation"], "test_animation.csv")
    else:
        print("Failed to generate animation")

if __name__ == "__main__":
    asyncio.run(test_audio2face_api())