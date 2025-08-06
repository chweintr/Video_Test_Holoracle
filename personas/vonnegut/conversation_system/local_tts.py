"""
Local TTS handler supporting Higgs Audio v2 and pyttsx3 fallback.
Completely removes ElevenLabs dependency for fully local voice synthesis.
"""

import logging
import numpy as np
import soundfile as sf
import asyncio
import pyttsx3
import io
import tempfile
import os
import sys
from pathlib import Path
from typing import Optional, Dict, Any
import threading
import queue

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LocalTTSHandler:
    def __init__(self, model_path: Optional[str] = None):
        """
        Initialize local TTS handler.
        
        Args:
            model_path: Path to trained Higgs model (optional)
        """
        self.model_path = model_path
        self.higgs_model = None
        self.pyttsx3_engine = None
        
        # Audio settings
        self.sample_rate = 22050
        self.voice_speed = 150  # WPM for pyttsx3
        self.voice_volume = 0.8
        
        # Initialize TTS engines immediately for basic functionality
        self.initialized = False
        self.initialize_pyttsx3()  # Initialize pyttsx3 right away
        
        logger.info("LocalTTSHandler initialized")
    
    async def initialize_engines(self):
        """Initialize available TTS engines."""
        # Try to load Higgs model first
        await self.load_higgs_model()
        
        # Initialize pyttsx3 as fallback
        self.initialize_pyttsx3()
    
    async def load_higgs_model(self):
        """Load Higgs Audio v2 model."""
        try:
            # Add Higgs path to sys.path
            higgs_path = Path(__file__).parent.parent / "higgs-audio"
            if higgs_path.exists() and str(higgs_path) not in sys.path:
                sys.path.insert(0, str(higgs_path))
            
            logger.info("Loading Higgs Audio v2...")
            
            # Import Higgs Audio v2
            try:
                from boson_multimodal.serve.serve_engine import HiggsAudioServeEngine
                from boson_multimodal.data_types import ChatMLSample, Message
                
                # Disable CUDA to avoid dtype issues
                import torch
                torch.cuda.is_available = lambda: False
                
                # Initialize Higgs serve engine
                self.higgs_model = HiggsAudioServeEngine(
                    model_name_or_path="bosonai/higgs-audio-v2-generation-3B-base",
                    audio_tokenizer_name_or_path="bosonai/higgs-audio-v2-tokenizer",
                    device="cpu",
                    torch_dtype=torch.float32,
                    kv_cache_lengths=[512]  # Smaller cache for faster generation
                )
                
                # Store the data types for later use
                self.ChatMLSample = ChatMLSample
                self.Message = Message
                
                logger.info("Higgs Audio v2 loaded successfully")
                
            except ImportError as e:
                logger.warning(f"Higgs Audio v2 not available: {e}")
                self.higgs_model = None
            except Exception as e:
                logger.warning(f"Error initializing Higgs: {e}")
                self.higgs_model = None
                
        except Exception as e:
            logger.error(f"Error loading Higgs model: {e}")
            self.higgs_model = None
    
    def initialize_pyttsx3(self):
        """Initialize pyttsx3 TTS engine."""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            
            # Configure voice settings
            self.pyttsx3_engine.setProperty('rate', self.voice_speed)
            self.pyttsx3_engine.setProperty('volume', self.voice_volume)
            
            # Try to find a suitable voice
            voices = self.pyttsx3_engine.getProperty('voices')
            
            # Enhanced voice selection for better Vonnegut-like sound
            best_voice = None
            voice_scores = []
            
            for voice in voices:
                voice_name = voice.name.lower()
                voice_id = voice.id.lower()
                score = 0
                
                # Prefer male voices
                if any(keyword in voice_name for keyword in ['male', 'man', 'masculine']):
                    score += 3
                
                # Look for mature/older sounding voices
                if any(keyword in voice_name for keyword in ['david', 'mark', 'alex', 'tom', 'paul', 'william', 'richard']):
                    score += 2
                
                # Prefer SAPI voices (usually better quality on Windows)
                if 'sapi' in voice_id or 'microsoft' in voice_id:
                    score += 1
                
                # Avoid obviously robotic voices
                if any(keyword in voice_name for keyword in ['robotic', 'synthetic', 'computer']):
                    score -= 2
                
                # Platform-specific preferences
                if sys.platform.startswith('win'):
                    # Windows: prefer David, Mark, or Zira voices
                    if any(name in voice_name for name in ['david', 'mark']):
                        score += 3
                elif sys.platform.startswith('darwin'):
                    # macOS: prefer Alex, Tom, or Daniel
                    if any(name in voice_name for name in ['alex', 'tom', 'daniel']):
                        score += 3
                
                voice_scores.append((score, voice))
                logger.debug(f"Voice: {voice.name} (Score: {score})")
            
            # Select best voice
            if voice_scores:
                voice_scores.sort(key=lambda x: x[0], reverse=True)
                best_voice = voice_scores[0][1]
                self.pyttsx3_engine.setProperty('voice', best_voice.id)
                logger.info(f"Selected voice: {best_voice.name} (Score: {voice_scores[0][0]})")
            else:
                logger.info("Using default system voice")
            
            # Optimize voice settings for more natural speech
            self.voice_speed = 140  # Slightly slower for more gravitas
            self.voice_volume = 0.9
            self.pyttsx3_engine.setProperty('rate', self.voice_speed)
            self.pyttsx3_engine.setProperty('volume', self.voice_volume)
            
            logger.info("pyttsx3 TTS engine initialized")
            
        except Exception as e:
            logger.error(f"Error initializing pyttsx3: {e}")
            self.pyttsx3_engine = None
    
    async def synthesize_speech(self, text: str, voice_id: str = "vonnegut") -> Optional[np.ndarray]:
        """
        Synthesize speech from text using available TTS engine.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier (for Higgs models)
            
        Returns:
            Audio data as numpy array, or None if synthesis failed
        """
        try:
            logger.info(f"Synthesizing speech: '{text[:50]}...'")
            logger.info(f"Available engines - Higgs: {self.higgs_model is not None}, pyttsx3: {self.pyttsx3_engine is not None}")
            
            # Try Higgs model first
            if self.higgs_model:
                logger.info("Using Higgs model for synthesis")
                return await self.synthesize_higgs(text, voice_id)
            
            # Fall back to pyttsx3
            elif self.pyttsx3_engine:
                logger.info("Using pyttsx3 for synthesis")
                return await self.synthesize_pyttsx3(text)
            
            else:
                logger.error("No TTS engine available")
                return None
                
        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def synthesize_higgs(self, text: str, voice_id: str = "vonnegut") -> Optional[np.ndarray]:
        """Synthesize speech using Higgs Audio v2."""
        try:
            logger.info(f"Synthesizing with Higgs: {text[:50]}...")
            
            if not self.higgs_model:
                logger.warning("Higgs model not loaded")
                return None
            
            # Create message for Higgs
            message = self.Message(role="user", content=[text])
            sample = self.ChatMLSample(messages=[message])
            
            # Generate audio
            response = self.higgs_model.generate(
                chat_ml_sample=sample,
                max_new_tokens=100,  # Limit for faster generation
                temperature=0.8,
                force_audio_gen=True  # Force audio generation
            )
            
            if response.audio is not None:
                logger.info(f"Higgs synthesis complete: {len(response.audio)/response.sampling_rate:.2f}s")
                
                # Resample if necessary
                if response.sampling_rate != self.sample_rate:
                    # Simple resampling
                    ratio = self.sample_rate / response.sampling_rate
                    new_length = int(len(response.audio) * ratio)
                    audio_data = np.interp(
                        np.linspace(0, len(response.audio), new_length),
                        np.arange(len(response.audio)),
                        response.audio
                    )
                    return audio_data.astype(np.float32)
                else:
                    return response.audio.astype(np.float32)
            else:
                logger.warning("Higgs generated no audio")
                return None
            
        except Exception as e:
            logger.error(f"Error in Higgs synthesis: {e}")
            import traceback
            traceback.print_exc()
            return None
    
    async def synthesize_pyttsx3(self, text: str) -> Optional[np.ndarray]:
        """Synthesize speech using pyttsx3."""
        try:
            logger.info(f"Synthesizing with pyttsx3: {text[:50]}...")
            
            if not self.pyttsx3_engine:
                logger.error("pyttsx3 engine not available")
                return None
            
            # Create temporary file for audio output
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            try:
                # Use threading to avoid blocking
                synthesis_complete = threading.Event()
                error_queue = queue.Queue()
                
                def synthesis_thread():
                    try:
                        self.pyttsx3_engine.save_to_file(text, temp_path)
                        self.pyttsx3_engine.runAndWait()
                        synthesis_complete.set()
                    except Exception as e:
                        error_queue.put(e)
                        synthesis_complete.set()
                
                thread = threading.Thread(target=synthesis_thread)
                thread.start()
                
                # Wait for synthesis to complete (with timeout)
                thread.join(timeout=30)  # 30 second timeout
                
                if not synthesis_complete.is_set():
                    logger.error("pyttsx3 synthesis timed out")
                    return None
                
                if not error_queue.empty():
                    error = error_queue.get()
                    logger.error(f"pyttsx3 synthesis error: {error}")
                    return None
                
                # Load the generated audio file
                if os.path.exists(temp_path):
                    audio_data, sample_rate = sf.read(temp_path)
                    
                    # Resample if necessary
                    if sample_rate != self.sample_rate:
                        # Simple resampling (use librosa for better quality in production)
                        ratio = self.sample_rate / sample_rate
                        new_length = int(len(audio_data) * ratio)
                        audio_data = np.interp(
                            np.linspace(0, len(audio_data), new_length),
                            np.arange(len(audio_data)),
                            audio_data
                        )
                    
                    logger.info(f"pyttsx3 synthesis complete: {len(audio_data)/self.sample_rate:.2f}s")
                    return audio_data.astype(np.float32)
                else:
                    logger.error("pyttsx3 failed to create audio file")
                    return None
                    
            finally:
                # Clean up temporary file
                if os.path.exists(temp_path):
                    os.unlink(temp_path)
                    
        except Exception as e:
            logger.error(f"Error in pyttsx3 synthesis: {e}")
            return None
    
    def get_available_engines(self) -> Dict[str, bool]:
        """Get status of available TTS engines."""
        return {
            "higgs": self.higgs_model is not None,
            "pyttsx3": self.pyttsx3_engine is not None
        }
    
    def get_voice_info(self) -> Dict[str, Any]:
        """Get information about current voice settings."""
        info = {
            "sample_rate": self.sample_rate,
            "engines": self.get_available_engines()
        }
        
        if self.pyttsx3_engine:
            try:
                voices = self.pyttsx3_engine.getProperty('voices')
                current_voice = self.pyttsx3_engine.getProperty('voice')
                
                current_voice_info = None
                for voice in voices:
                    if voice.id == current_voice:
                        current_voice_info = {
                            "id": voice.id,
                            "name": voice.name,
                            "age": getattr(voice, 'age', 'unknown'),
                            "gender": getattr(voice, 'gender', 'unknown')
                        }
                        break
                
                info["pyttsx3"] = {
                    "current_voice": current_voice_info,
                    "available_voices": len(voices),
                    "rate": self.pyttsx3_engine.getProperty('rate'),
                    "volume": self.pyttsx3_engine.getProperty('volume')
                }
            except Exception as e:
                logger.error(f"Error getting voice info: {e}")
        
        return info
    
    def set_voice_settings(self, speed: Optional[int] = None, volume: Optional[float] = None):
        """Update voice settings for pyttsx3."""
        try:
            if self.pyttsx3_engine:
                if speed is not None:
                    self.voice_speed = speed
                    self.pyttsx3_engine.setProperty('rate', speed)
                
                if volume is not None:
                    self.voice_volume = volume
                    self.pyttsx3_engine.setProperty('volume', volume)
                
                logger.info(f"Voice settings updated: speed={self.voice_speed}, volume={self.voice_volume}")
        
        except Exception as e:
            logger.error(f"Error updating voice settings: {e}")
    
    async def test_synthesis(self, test_text: str = "Listen: So it goes. This is a test of the voice synthesis system.") -> bool:
        """Test TTS synthesis with sample text."""
        try:
            logger.info("Testing TTS synthesis...")
            
            audio_data = await self.synthesize_speech(test_text)
            
            if audio_data is not None:
                logger.info(f"TTS test successful: {len(audio_data)/self.sample_rate:.2f}s of audio")
                
                # Save test audio file
                test_path = "tts_test_output.wav"
                sf.write(test_path, audio_data, self.sample_rate)
                logger.info(f"Test audio saved: {test_path}")
                
                return True
            else:
                logger.error("TTS test failed: no audio generated")
                return False
                
        except Exception as e:
            logger.error(f"TTS test error: {e}")
            return False

# Test function
async def test_local_tts():
    """Test the local TTS functionality."""
    logger.info("Testing Local TTS Handler...")
    
    # Initialize TTS handler
    tts = LocalTTSHandler()
    
    # Wait for initialization
    await asyncio.sleep(2)
    
    # Get engine info
    engines = tts.get_available_engines()
    voice_info = tts.get_voice_info()
    
    logger.info(f"Available engines: {engines}")
    logger.info(f"Voice info: {voice_info}")
    
    # Test synthesis
    test_phrases = [
        "Hi ho. Listen: This is a test of the local TTS system.",
        "So it goes. I tell you, technology keeps marching on.",
        "My God, my God - we are what we pretend to be."
    ]
    
    for phrase in test_phrases:
        success = await tts.test_synthesis(phrase)
        logger.info(f"Test phrase synthesis: {'✓' if success else '✗'}")
        
        if success:
            break  # Stop after first successful test
    
    logger.info("Local TTS test completed")

def main():
    """Test the local TTS handler."""
    asyncio.run(test_local_tts())

if __name__ == "__main__":
    main()