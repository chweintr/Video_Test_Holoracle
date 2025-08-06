"""
Voice Activity Detection (VAD) handler using Silero VAD.
Detects speech in audio streams for the conversation system.
"""

import torch
import numpy as np
import logging
from typing import Optional, List, Tuple
import asyncio
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class VADHandler:
    def __init__(self, model_name: str = "silero_vad"):
        self.model_name = model_name
        self.model = None
        self.utils = None
        
        # VAD configuration
        self.sample_rate = 16000  # Silero VAD requires 16kHz
        self.chunk_size = 512  # samples
        self.threshold = 0.5  # Speech probability threshold
        
        # State tracking
        self.speech_buffer = []
        self.silence_buffer = []
        self.is_speaking = False
        self.speech_start_time = None
        self.last_speech_time = None
        
        # Parameters for speech segmentation
        self.min_speech_duration = 0.5  # seconds
        self.max_silence_duration = 1.0  # seconds
        self.max_speech_duration = 30.0  # seconds
        
        # Initialize model
        asyncio.create_task(self.load_model())
    
    async def load_model(self):
        """Load the Silero VAD model."""
        try:
            logger.info("Loading Silero VAD model...")
            
            # Load Silero VAD model
            # This requires: pip install torch torchaudio
            model, utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False,
                onnx=False
            )
            
            self.model = model
            self.utils = utils
            
            # Extract utility functions
            (self.get_speech_timestamps,
             self.save_audio,
             self.read_audio,
             self.VADIterator,
             self.collect_chunks) = utils
            
            logger.info("Silero VAD model loaded successfully")
            
        except Exception as e:
            logger.error(f"Error loading Silero VAD model: {e}")
            logger.info("Falling back to simple energy-based VAD")
            self.model = None
    
    def preprocess_audio(self, audio: np.ndarray, target_sr: int = None) -> torch.Tensor:
        """Preprocess audio for VAD model."""
        if target_sr is None:
            target_sr = self.sample_rate
        
        # Convert to float32 if needed
        if audio.dtype != np.float32:
            if audio.dtype == np.int16:
                audio = audio.astype(np.float32) / 32768.0
            else:
                audio = audio.astype(np.float32)
        
        # Resample if needed (simple linear interpolation)
        if len(audio) == 0:
            return torch.zeros(0, dtype=torch.float32)
        
        # Convert to torch tensor
        audio_tensor = torch.from_numpy(audio).float()
        
        # Ensure correct sample rate (basic resampling)
        # For production, use librosa.resample or torchaudio.transforms.Resample
        if target_sr != self.sample_rate:
            ratio = target_sr / self.sample_rate
            new_length = int(len(audio_tensor) * ratio)
            if new_length > 0:
                indices = torch.linspace(0, len(audio_tensor) - 1, new_length)
                audio_tensor = torch.nn.functional.interpolate(
                    audio_tensor.unsqueeze(0).unsqueeze(0),
                    size=new_length,
                    mode='linear',
                    align_corners=True
                ).squeeze()
        
        return audio_tensor
    
    async def detect_speech(self, audio: np.ndarray) -> float:
        """
        Detect speech in audio chunk and return probability.
        
        Args:
            audio: Audio samples as numpy array
            
        Returns:
            Speech probability (0.0 to 1.0)
        """
        try:
            if self.model is not None:
                return await self.silero_vad_detect(audio)
            else:
                return self.energy_based_vad(audio)
                
        except Exception as e:
            logger.error(f"Error in speech detection: {e}")
            return 0.0
    
    async def silero_vad_detect(self, audio: np.ndarray) -> float:
        """Use Silero VAD model for speech detection."""
        try:
            # Preprocess audio
            audio_tensor = self.preprocess_audio(audio, self.sample_rate)
            
            if len(audio_tensor) < 512:  # Minimum chunk size
                return 0.0
            
            # Run VAD model
            with torch.no_grad():
                speech_prob = self.model(audio_tensor, self.sample_rate).item()
            
            return speech_prob
            
        except Exception as e:
            logger.error(f"Error in Silero VAD: {e}")
            return self.energy_based_vad(audio)
    
    def energy_based_vad(self, audio: np.ndarray) -> float:
        """Simple energy-based VAD fallback."""
        try:
            if len(audio) == 0:
                return 0.0
            
            # Calculate RMS energy
            rms_energy = np.sqrt(np.mean(audio ** 2))
            
            # Simple threshold-based detection
            # This is very basic and should be tuned for your use case
            energy_threshold = 0.01
            
            if rms_energy > energy_threshold:
                # Check for spectral characteristics (very basic)
                # Higher frequencies often indicate speech
                if len(audio) > 100:
                    high_freq_energy = np.sqrt(np.mean(np.diff(audio) ** 2))
                    if high_freq_energy > 0.001:
                        return min(1.0, rms_energy * 10)  # Scale to probability
            
            return 0.0
            
        except Exception as e:
            logger.error(f"Error in energy-based VAD: {e}")
            return 0.0
    
    def update_speech_state(self, speech_prob: float, timestamp: float = None) -> dict:
        """
        Update internal speech state based on current probability.
        
        Args:
            speech_prob: Current speech probability
            timestamp: Current timestamp (optional)
            
        Returns:
            State information dictionary
        """
        if timestamp is None:
            timestamp = len(self.speech_buffer) / self.sample_rate
        
        is_speech = speech_prob > self.threshold
        
        # State transitions
        if is_speech and not self.is_speaking:
            # Start of speech
            self.is_speaking = True
            self.speech_start_time = timestamp
            self.last_speech_time = timestamp
            logger.debug(f"Speech started at {timestamp:.2f}s")
            
        elif is_speech and self.is_speaking:
            # Continuing speech
            self.last_speech_time = timestamp
            
        elif not is_speech and self.is_speaking:
            # Potential end of speech
            silence_duration = timestamp - self.last_speech_time
            
            if silence_duration > self.max_silence_duration:
                # End of speech
                speech_duration = self.last_speech_time - self.speech_start_time
                
                logger.debug(f"Speech ended at {timestamp:.2f}s, duration: {speech_duration:.2f}s")
                
                self.is_speaking = False
                self.speech_start_time = None
                
                # Return speech segment info
                return {
                    'event': 'speech_end',
                    'speech_duration': speech_duration,
                    'valid_speech': speech_duration > self.min_speech_duration,
                    'timestamp': timestamp
                }
        
        # Check for maximum speech duration
        if self.is_speaking and self.speech_start_time:
            speech_duration = timestamp - self.speech_start_time
            if speech_duration > self.max_speech_duration:
                logger.debug(f"Maximum speech duration reached: {speech_duration:.2f}s")
                
                self.is_speaking = False
                self.speech_start_time = None
                
                return {
                    'event': 'speech_timeout',
                    'speech_duration': speech_duration,
                    'valid_speech': True,
                    'timestamp': timestamp
                }
        
        return {
            'event': 'speech_continue' if is_speech else 'silence',
            'is_speaking': self.is_speaking,
            'speech_prob': speech_prob,
            'timestamp': timestamp
        }
    
    async def get_speech_segments(self, audio: np.ndarray) -> List[Tuple[float, float]]:
        """
        Get speech segment timestamps from audio.
        
        Args:
            audio: Full audio buffer
            
        Returns:
            List of (start_time, end_time) tuples for speech segments
        """
        try:
            if self.model is None:
                return await self.get_speech_segments_energy(audio)
            
            # Preprocess audio
            audio_tensor = self.preprocess_audio(audio, self.sample_rate)
            
            # Get speech timestamps using Silero VAD
            speech_timestamps = self.get_speech_timestamps(
                audio_tensor,
                self.model,
                sampling_rate=self.sample_rate,
                threshold=self.threshold,
                min_speech_duration_ms=int(self.min_speech_duration * 1000),
                min_silence_duration_ms=int(self.max_silence_duration * 1000)
            )
            
            # Convert to seconds
            segments = []
            for timestamp in speech_timestamps:
                start_time = timestamp['start'] / self.sample_rate
                end_time = timestamp['end'] / self.sample_rate
                segments.append((start_time, end_time))
            
            return segments
            
        except Exception as e:
            logger.error(f"Error getting speech segments: {e}")
            return []
    
    async def get_speech_segments_energy(self, audio: np.ndarray) -> List[Tuple[float, float]]:
        """Fallback energy-based speech segmentation."""
        try:
            if len(audio) == 0:
                return []
            
            # Simple energy-based segmentation
            chunk_size = int(0.1 * self.sample_rate)  # 100ms chunks
            segments = []
            current_start = None
            
            for i in range(0, len(audio), chunk_size):
                chunk = audio[i:i + chunk_size]
                if len(chunk) == 0:
                    continue
                
                energy = np.sqrt(np.mean(chunk ** 2))
                is_speech = energy > 0.01  # Simple threshold
                
                timestamp = i / self.sample_rate
                
                if is_speech and current_start is None:
                    current_start = timestamp
                elif not is_speech and current_start is not None:
                    duration = timestamp - current_start
                    if duration > self.min_speech_duration:
                        segments.append((current_start, timestamp))
                    current_start = None
            
            # Handle case where audio ends during speech
            if current_start is not None:
                end_time = len(audio) / self.sample_rate
                if end_time - current_start > self.min_speech_duration:
                    segments.append((current_start, end_time))
            
            return segments
            
        except Exception as e:
            logger.error(f"Error in energy-based segmentation: {e}")
            return []
    
    def reset_state(self):
        """Reset VAD state."""
        self.speech_buffer = []
        self.silence_buffer = []
        self.is_speaking = False
        self.speech_start_time = None
        self.last_speech_time = None
        logger.debug("VAD state reset")
    
    def get_config(self) -> dict:
        """Get current VAD configuration."""
        return {
            'model_name': self.model_name,
            'sample_rate': self.sample_rate,
            'threshold': self.threshold,
            'min_speech_duration': self.min_speech_duration,
            'max_silence_duration': self.max_silence_duration,
            'max_speech_duration': self.max_speech_duration,
            'model_loaded': self.model is not None
        }

# Example usage and testing
async def test_vad():
    """Test VAD functionality."""
    logger.info("Testing VAD functionality...")
    
    vad = VADHandler()
    
    # Wait for model to load
    await asyncio.sleep(2)
    
    # Test with synthetic audio
    duration = 5.0  # seconds
    sample_rate = 16000
    
    # Create test audio: speech-like signal + silence
    t = np.linspace(0, duration, int(duration * sample_rate), False)
    
    # Speech-like signal (modulated noise)
    speech_signal = np.random.randn(len(t)) * 0.1
    speech_signal *= (1 + 0.5 * np.sin(2 * np.pi * 5 * t))  # 5Hz modulation
    
    # Add silence periods
    speech_signal[:sample_rate] = 0  # First second: silence
    speech_signal[3*sample_rate:4*sample_rate] = 0  # Fourth second: silence
    
    logger.info(f"Testing with {duration}s of synthetic audio")
    
    # Process in chunks
    chunk_size = int(0.5 * sample_rate)  # 500ms chunks
    
    for i in range(0, len(speech_signal), chunk_size):
        chunk = speech_signal[i:i + chunk_size]
        if len(chunk) == 0:
            continue
        
        speech_prob = await vad.detect_speech(chunk)
        timestamp = i / sample_rate
        
        state = vad.update_speech_state(speech_prob, timestamp)
        
        logger.info(f"t={timestamp:.2f}s: prob={speech_prob:.3f}, event={state['event']}")
        
        if state['event'] in ['speech_end', 'speech_timeout']:
            logger.info(f"  -> Speech segment: {state['speech_duration']:.2f}s")
    
    # Test speech segmentation
    segments = await vad.get_speech_segments(speech_signal)
    logger.info(f"Detected {len(segments)} speech segments:")
    for i, (start, end) in enumerate(segments):
        logger.info(f"  Segment {i+1}: {start:.2f}s - {end:.2f}s ({end-Start:.2f}s)")
    
    logger.info("VAD test complete")

def main():
    """Test the VAD handler."""
    asyncio.run(test_vad())

if __name__ == "__main__":
    main()