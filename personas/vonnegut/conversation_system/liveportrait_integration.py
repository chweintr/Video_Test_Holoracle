"""
LivePortrait Integration for Indiana Oracle
Real-time facial animation using LivePortrait
"""

import asyncio
import numpy as np
from pathlib import Path
import cv2
import torch
from typing import Optional, Dict, Any, Tuple
import logging
import json
import base64
from io import BytesIO
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LivePortraitIntegration:
    def __init__(self, source_image_path: str = None):
        """
        Initialize LivePortrait for real-time facial animation.
        
        Args:
            source_image_path: Path to source portrait (Vonnegut image)
        """
        self.source_image_path = source_image_path or "../assets/vonnegut_portrait.jpg"
        self.model = None
        self.source_latent = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Frame settings
        self.output_size = (512, 512)  # Can be 256x256 for faster performance
        self.fps = 25
        
        # Initialize model
        self._init_model()
        
        logger.info(f"LivePortrait initialized on {self.device}")
    
    def _init_model(self):
        """Initialize LivePortrait model."""
        try:
            # Add LivePortrait to path
            import sys
            liveportrait_path = Path(__file__).parent.parent / "LivePortrait"
            if liveportrait_path.exists():
                sys.path.insert(0, str(liveportrait_path))
            
            # Import LivePortrait modules
            from src.live_portrait_pipeline import LivePortraitPipeline
            from src.config.inference_config import InferenceConfig
            
            # Load config
            config = InferenceConfig()
            config.device = self.device
            config.output_dir = "./output"
            
            # Initialize pipeline
            self.model = LivePortraitPipeline(config)
            
            # Load source image
            if Path(self.source_image_path).exists():
                self.load_source_image(self.source_image_path)
            
            logger.info("LivePortrait model loaded successfully")
            
        except ImportError as e:
            logger.error(f"LivePortrait not installed: {e}")
            logger.info("Please install LivePortrait following install_liveportrait.md")
            self.model = None
        except Exception as e:
            logger.error(f"Error initializing LivePortrait: {e}")
            self.model = None
    
    def load_source_image(self, image_path: str):
        """Load and preprocess source portrait."""
        try:
            # Load image
            source_img = cv2.imread(image_path)
            source_img = cv2.cvtColor(source_img, cv2.COLOR_BGR2RGB)
            
            # Resize if needed
            if source_img.shape[:2] != self.output_size:
                source_img = cv2.resize(source_img, self.output_size)
            
            # Precompute source latent for efficiency
            if self.model:
                self.source_latent = self.model.prepare_source(source_img)
            
            self.source_image = source_img
            logger.info(f"Source image loaded: {image_path}")
            
        except Exception as e:
            logger.error(f"Error loading source image: {e}")
    
    def blendshapes_to_landmarks(self, blendshapes: Dict[str, float]) -> np.ndarray:
        """
        Convert Audio2Face blendshapes to facial landmarks.
        
        Args:
            blendshapes: Dictionary of blendshape values
            
        Returns:
            68 facial landmarks as numpy array
        """
        # Initialize neutral face landmarks (68 points)
        landmarks = self.get_neutral_landmarks()
        
        # Map blendshapes to landmark movements
        if blendshapes.get('jawOpen', 0) > 0:
            # Move jaw landmarks down
            jaw_indices = list(range(48, 68))  # Mouth landmarks
            landmarks[jaw_indices, 1] += blendshapes['jawOpen'] * 20
        
        if blendshapes.get('mouthSmile', 0) > 0:
            # Move mouth corners up and out
            landmarks[48, 0] -= blendshapes['mouthSmile'] * 10  # Left corner
            landmarks[54, 0] += blendshapes['mouthSmile'] * 10  # Right corner
            landmarks[[48, 54], 1] -= blendshapes['mouthSmile'] * 5
        
        if blendshapes.get('browInnerUp', 0) > 0:
            # Raise eyebrows
            brow_indices = list(range(17, 27))
            landmarks[brow_indices, 1] -= blendshapes['browInnerUp'] * 10
        
        if blendshapes.get('eyeBlinkLeft', 0) > 0:
            # Close left eye
            left_eye = list(range(36, 42))
            landmarks[left_eye[1:4], 1] += blendshapes['eyeBlinkLeft'] * 5
        
        if blendshapes.get('eyeBlinkRight', 0) > 0:
            # Close right eye
            right_eye = list(range(42, 48))
            landmarks[right_eye[1:4], 1] += blendshapes['eyeBlinkRight'] * 5
        
        return landmarks
    
    def get_neutral_landmarks(self) -> np.ndarray:
        """Get neutral face landmarks (68 points)."""
        # Simplified neutral face landmarks
        # In practice, extract from source image using dlib/mediapipe
        landmarks = np.array([
            # Jaw line (17 points)
            [100, 200], [105, 220], [110, 240], [120, 260], [130, 275],
            [145, 285], [165, 295], [185, 300], [205, 295], [225, 285],
            [240, 275], [250, 260], [260, 240], [265, 220], [270, 200],
            [275, 180], [280, 160],
            
            # Right eyebrow (5 points)
            [120, 140], [130, 135], [145, 135], [160, 140], [170, 145],
            
            # Left eyebrow (5 points)
            [200, 145], [210, 140], [225, 135], [240, 135], [250, 140],
            
            # Nose bridge (4 points)
            [185, 165], [185, 180], [185, 195], [185, 210],
            
            # Nose tip (5 points)
            [165, 220], [175, 225], [185, 230], [195, 225], [205, 220],
            
            # Right eye (6 points)
            [130, 165], [140, 160], [155, 160], [165, 165], [155, 170], [140, 170],
            
            # Left eye (6 points)
            [205, 165], [215, 160], [230, 160], [240, 165], [230, 170], [215, 170],
            
            # Outer mouth (12 points)
            [150, 250], [160, 245], [170, 240], [185, 242], [200, 240],
            [210, 245], [220, 250], [210, 260], [200, 265], [185, 267],
            [170, 265], [160, 260],
            
            # Inner mouth (8 points)
            [160, 250], [170, 248], [185, 250], [200, 248], [210, 250],
            [200, 255], [185, 257], [170, 255]
        ], dtype=np.float32)
        
        return landmarks
    
    async def animate_frame(self, driving_data: Dict) -> Optional[np.ndarray]:
        """
        Animate source portrait with driving data.
        
        Args:
            driving_data: Can contain:
                - blendshapes: Audio2Face blendshapes
                - landmarks: Direct facial landmarks
                - expression: Expression coefficients
                
        Returns:
            Animated frame as numpy array
        """
        if not self.model or self.source_latent is None:
            return None
        
        try:
            # Convert input to driving signal
            if 'blendshapes' in driving_data:
                landmarks = self.blendshapes_to_landmarks(driving_data['blendshapes'])
            elif 'landmarks' in driving_data:
                landmarks = np.array(driving_data['landmarks'])
            else:
                return None
            
            # Generate animated frame
            animated_frame = self.model.generate(
                source_latent=self.source_latent,
                driving_landmarks=landmarks
            )
            
            return animated_frame
            
        except Exception as e:
            logger.error(f"Error animating frame: {e}")
            return None
    
    async def process_audio_to_animation(self, audio_data: np.ndarray, 
                                       blendshapes_data: List[Dict]) -> List[np.ndarray]:
        """
        Process audio and blendshapes into animated frames.
        
        Args:
            audio_data: Audio waveform
            blendshapes_data: List of blendshape dictionaries per frame
            
        Returns:
            List of animated frames
        """
        frames = []
        
        for blendshapes in blendshapes_data:
            frame = await self.animate_frame({'blendshapes': blendshapes})
            if frame is not None:
                frames.append(frame)
        
        return frames
    
    def create_video(self, frames: List[np.ndarray], output_path: str, fps: int = 25):
        """Save animated frames as video."""
        if not frames:
            return
        
        height, width = frames[0].shape[:2]
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        
        for frame in frames:
            # Convert RGB to BGR for OpenCV
            frame_bgr = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)
        
        out.release()
        logger.info(f"Video saved: {output_path}")

# Real-time streaming version
class LivePortraitStream:
    """Stream animated frames in real-time."""
    
    def __init__(self, liveportrait: LivePortraitIntegration):
        self.liveportrait = liveportrait
        self.is_streaming = False
        self.frame_buffer = asyncio.Queue(maxsize=30)
        
    async def start_stream(self, websocket):
        """Start streaming animated frames to client."""
        self.is_streaming = True
        
        # Producer task
        async def produce_frames():
            while self.is_streaming:
                # Get latest blendshapes from queue
                if not self.frame_buffer.empty():
                    driving_data = await self.frame_buffer.get()
                    frame = await self.liveportrait.animate_frame(driving_data)
                    
                    if frame is not None:
                        # Encode frame
                        _, buffer = cv2.imencode('.jpg', frame)
                        frame_base64 = base64.b64encode(buffer).decode('utf-8')
                        
                        # Send to client
                        await websocket.send(json.dumps({
                            'type': 'animated_frame',
                            'frame': frame_base64,
                            'timestamp': driving_data.get('timestamp', 0)
                        }))
                
                await asyncio.sleep(1/30)  # 30 FPS
        
        await produce_frames()
    
    async def add_driving_data(self, data: Dict):
        """Add driving data to animation queue."""
        if not self.frame_buffer.full():
            await self.frame_buffer.put(data)
    
    def stop_stream(self):
        """Stop streaming."""
        self.is_streaming = False

# Integration with existing voice system
class VonnegutAnimator:
    """Animate Vonnegut portrait based on speech."""
    
    def __init__(self):
        # Use your Vonnegut portrait
        self.portrait_path = "../assets/vonnegut_portrait.jpg"
        self.liveportrait = LivePortraitIntegration(self.portrait_path)
        self.stream = LivePortraitStream(self.liveportrait)
        
    async def animate_speech(self, text: str, audio_data: np.ndarray, 
                           blendshapes: List[Dict]) -> str:
        """
        Create animated video of Vonnegut speaking.
        
        Args:
            text: Spoken text
            audio_data: Audio waveform
            blendshapes: Audio2Face blendshapes
            
        Returns:
            Path to output video
        """
        # Process animation
        frames = await self.liveportrait.process_audio_to_animation(
            audio_data, blendshapes
        )
        
        # Save video
        output_path = f"output/vonnegut_{hash(text[:20])}.mp4"
        self.liveportrait.create_video(frames, output_path)
        
        return output_path

# Example usage
async def test_liveportrait():
    """Test LivePortrait integration."""
    animator = VonnegutAnimator()
    
    # Test with simple blendshapes
    test_blendshapes = [
        {'jawOpen': 0.0, 'mouthSmile': 0.0},
        {'jawOpen': 0.3, 'mouthSmile': 0.1},
        {'jawOpen': 0.5, 'mouthSmile': 0.2},
        {'jawOpen': 0.3, 'mouthSmile': 0.3},
        {'jawOpen': 0.0, 'mouthSmile': 0.5},
    ]
    
    frames = []
    for bs in test_blendshapes:
        frame = await animator.liveportrait.animate_frame({'blendshapes': bs})
        if frame is not None:
            frames.append(frame)
    
    if frames:
        animator.liveportrait.create_video(frames, "test_animation.mp4", fps=5)
        print(f"Created test animation with {len(frames)} frames")
    else:
        print("Failed to generate frames")

if __name__ == "__main__":
    asyncio.run(test_liveportrait())