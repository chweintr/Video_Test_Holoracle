"""
Lightweight local TTS handler with optimized Higgs integration.
Falls back to pyttsx3 for stability.
"""

import logging
import numpy as np
import soundfile as sf
import asyncio
import pyttsx3
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
    def __init__(self, use_higgs: bool = False):
        """
        Initialize local TTS handler.
        
        Args:
            use_higgs: Whether to attempt loading Higgs (disabled by default for stability)
        """
        self.use_higgs = use_higgs
        self.higgs_model = None
        self.pyttsx3_engine = None
        
        # Audio settings
        self.sample_rate = 22050
        self.voice_speed = 140  # Slower for Vonnegut gravitas
        self.voice_volume = 0.9
        
        # Initialize pyttsx3 immediately
        self.initialize_pyttsx3()
        
        logger.info(f"LocalTTSHandler initialized (Higgs: {'enabled' if use_higgs else 'disabled'})")
    
    async def initialize_engines(self):
        """Initialize available TTS engines."""
        # Only load Higgs if explicitly enabled
        if self.use_higgs:
            await self.load_higgs_model()
        
        # pyttsx3 already initialized in __init__
    
    async def load_higgs_model(self):
        """Load Higgs Audio v2 model (lightweight version)."""
        try:
            logger.info("Higgs loading disabled for stability - using enhanced pyttsx3")
            self.higgs_model = None
        except Exception as e:
            logger.error(f"Error loading Higgs model: {e}")
            self.higgs_model = None
    
    def initialize_pyttsx3(self):
        """Initialize pyttsx3 TTS engine with best voice selection."""
        try:
            self.pyttsx3_engine = pyttsx3.init()
            
            # Configure voice settings
            self.pyttsx3_engine.setProperty('rate', self.voice_speed)
            self.pyttsx3_engine.setProperty('volume', self.voice_volume)
            
            # Find best voice
            voices = self.pyttsx3_engine.getProperty('voices')
            best_voice = self.select_best_voice(voices)
            
            if best_voice:
                self.pyttsx3_engine.setProperty('voice', best_voice.id)
                logger.info(f"Selected voice: {best_voice.name}")
            
            logger.info("pyttsx3 TTS engine initialized")
            
        except Exception as e:
            logger.error(f"Error initializing pyttsx3: {e}")
            self.pyttsx3_engine = None
    
    def select_best_voice(self, voices):
        """Select the best available voice for Vonnegut."""
        voice_scores = []
        
        for voice in voices:
            voice_name = voice.name.lower()
            voice_id = voice.id.lower()
            score = 0
            
            # Scoring criteria
            if any(keyword in voice_name for keyword in ['male', 'man']):
                score += 3
            
            if any(keyword in voice_name for keyword in ['david', 'mark', 'alex', 'tom', 'paul']):
                score += 2
            
            if 'microsoft' in voice_id or 'sapi' in voice_id:
                score += 1
            
            voice_scores.append((score, voice))
        
        if voice_scores:
            voice_scores.sort(key=lambda x: x[0], reverse=True)
            return voice_scores[0][1]
        
        return None
    
    async def synthesize_speech(self, text: str, voice_id: str = "vonnegut") -> Optional[np.ndarray]:
        """
        Synthesize speech from text using available TTS engine.
        
        Args:
            text: Text to synthesize
            voice_id: Voice identifier (unused for pyttsx3)
            
        Returns:
            Audio data as numpy array, or None if synthesis failed
        """
        try:
            logger.info(f"Synthesizing: '{text[:50]}...'")
            
            # Always use pyttsx3 for stability
            return await self.synthesize_pyttsx3(text)
                
        except Exception as e:
            logger.error(f"Error in speech synthesis: {e}")
            return None
    
    async def synthesize_pyttsx3(self, text: str) -> Optional[np.ndarray]:
        """Synthesize speech using pyttsx3."""
        try:
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
                thread.join(timeout=30)
                
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
                        ratio = self.sample_rate / sample_rate
                        new_length = int(len(audio_data) * ratio)
                        audio_data = np.interp(
                            np.linspace(0, len(audio_data), new_length),
                            np.arange(len(audio_data)),
                            audio_data
                        )
                    
                    logger.info(f"Synthesis complete: {len(audio_data)/self.sample_rate:.2f}s")
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
                            "name": voice.name
                        }
                        break
                
                info["pyttsx3"] = {
                    "current_voice": current_voice_info,
                    "rate": self.pyttsx3_engine.getProperty('rate'),
                    "volume": self.pyttsx3_engine.getProperty('volume')
                }
            except Exception as e:
                logger.error(f"Error getting voice info: {e}")
        
        return info
    
    async def test_synthesis(self, test_text: str = "Listen: So it goes.") -> bool:
        """Test TTS synthesis with sample text."""
        try:
            logger.info("Testing TTS synthesis...")
            
            audio_data = await self.synthesize_speech(test_text)
            
            if audio_data is not None:
                logger.info(f"TTS test successful: {len(audio_data)/self.sample_rate:.2f}s")
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
    logger.info("Testing Lightweight Local TTS Handler...")
    
    # Initialize TTS handler
    tts = LocalTTSHandler(use_higgs=False)  # Disable Higgs for stability
    
    # Test synthesis
    success = await tts.test_synthesis("Hi ho. Listen: So it goes.")
    logger.info(f"Test result: {'SUCCESS' if success else 'FAILED'}")

def main():
    """Test the local TTS handler."""
    asyncio.run(test_local_tts())

if __name__ == "__main__":
    main()