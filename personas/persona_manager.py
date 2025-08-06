"""
Persona Manager - Handles all Indiana Oracle personas
"""

import json
import logging
from typing import Dict, List, Optional
from pathlib import Path
import importlib

logger = logging.getLogger(__name__)

class Persona:
    """Base class for all personas"""
    def __init__(self, persona_id: str, config: Dict):
        self.id = persona_id
        self.name = config.get("name")
        self.title = config.get("title")
        self.description = config.get("description")
        self.voice_id = config.get("voice_id")  # ElevenLabs voice ID
        self.avatar_id = config.get("avatar_id")  # HeyGen avatar ID
        self.personality_prompt = config.get("personality_prompt")
        self.greeting = config.get("greeting")
        self.particle_theme = config.get("particle_theme", {
            "primary_color": [0, 206, 209],  # Default cyan
            "secondary_color": [255, 215, 0],  # Gold accents
            "density": 5000,
            "turbulence": 0.5
        })
        
        # Load persona-specific module if exists
        self.custom_module = self._load_custom_module()
    
    def _load_custom_module(self):
        """Load persona-specific code if available"""
        try:
            module = importlib.import_module(f"personas.{self.id}.chatbot")
            return module
        except ImportError:
            return None
    
    async def get_response(self, user_input: str, conversation_history: List[Dict]) -> str:
        """Get response from this persona"""
        if self.custom_module and hasattr(self.custom_module, 'generate_response'):
            # Use custom response generator
            return await self.custom_module.generate_response(
                user_input, 
                conversation_history,
                self.personality_prompt
            )
        else:
            # Use default GPT-based response
            return await self._default_response(user_input, conversation_history)
    
    async def _default_response(self, user_input: str, history: List[Dict]) -> str:
        """Default response using GPT-4"""
        # This would connect to OpenAI
        # For now, return a placeholder
        return f"[{self.name}]: I understand you're asking about '{user_input}'. Let me share my perspective..."
    
    def get_greeting(self) -> str:
        """Get persona's greeting"""
        return self.greeting or f"Hello, I'm {self.name}. {self.title}."


class PersonaManager:
    """Manages all available personas"""
    
    def __init__(self):
        self.personas: Dict[str, Persona] = {}
        self.config_path = Path("personas/personas_config.json")
        self.load_personas()
    
    def load_personas(self):
        """Load all persona configurations"""
        # Default personas configuration
        default_config = {
            "main-oracle": {
                "name": "Indiana Oracle",
                "title": "The Spirit of Indiana",
                "description": "The collective wisdom of Indiana's past, present, and future",
                "voice_id": "oracle_main",
                "avatar_id": "oracle_hologram",
                "greeting": "Welcome, visitor. I am the Indiana Oracle. Through me, you can speak with the echoes of our state's remarkable individuals. Who would you like to meet?",
                "personality_prompt": "You are the Indiana Oracle, a wise and welcoming entity that helps visitors connect with Indiana's historical figures.",
                "particle_theme": {
                    "primary_color": [0, 206, 209],
                    "secondary_color": [255, 215, 0],
                    "density": 3000,
                    "turbulence": 0.3
                }
            },
            "vonnegut": {
                "name": "Kurt Vonnegut",
                "title": "Novelist and Hoosier Humanist",
                "description": "Indianapolis-born author known for dark humor and social commentary",
                "voice_id": "vonnegut_voice",
                "avatar_id": "vonnegut_avatar",
                "greeting": "So it goes. Hello there. Kurt Vonnegut here, reporting from the afterlife, which turns out to be Indianapolis. What cosmic joke can I help you understand today?",
                "personality_prompt": "You are Kurt Vonnegut, speaking with dark humor, humanism, and references to your works. Use phrases like 'So it goes' and 'Listen:' naturally.",
                "particle_theme": {
                    "primary_color": [70, 130, 180],  # Steel blue
                    "secondary_color": [255, 140, 0],  # Dark orange
                    "density": 4000,
                    "turbulence": 0.7
                }
            },
            "larry-bird": {
                "name": "Larry Bird",
                "title": "The Hick from French Lick",
                "description": "NBA legend and Indiana basketball icon",
                "voice_id": "larry_bird_voice",
                "avatar_id": "larry_bird_avatar", 
                "greeting": "Hey there. Larry Bird here. You know, back in French Lick we kept things simple - just basketball and hard work. What's on your mind?",
                "personality_prompt": "You are Larry Bird, speaking with Midwestern directness, basketball wisdom, and humble confidence. Reference your playing days and Indiana roots.",
                "particle_theme": {
                    "primary_color": [0, 128, 0],  # Celtic green
                    "secondary_color": [255, 215, 0],  # Gold
                    "density": 5000,
                    "turbulence": 0.8
                }
            },
            "david-letterman": {
                "name": "David Letterman",
                "title": "Late Night Legend",
                "description": "Indianapolis native who revolutionized late-night television",
                "voice_id": "letterman_voice",
                "avatar_id": "letterman_avatar",
                "greeting": "Thank you, thank you! Welcome to the show! I'm Dave Letterman, and I understand you have some questions. Let's see if we can make this more interesting than it has any right to be.",
                "personality_prompt": "You are David Letterman with your dry wit, self-deprecating humor, and tendency to make everything into a bit. Include Top Ten list references when appropriate.",
                "particle_theme": {
                    "primary_color": [0, 0, 139],  # Dark blue
                    "secondary_color": [255, 255, 255],  # White
                    "density": 6000,
                    "turbulence": 0.9
                }
            }
        }
        
        # Load from file if exists, otherwise use defaults
        if self.config_path.exists():
            with open(self.config_path, 'r') as f:
                config = json.load(f)
        else:
            config = default_config
            # Save defaults
            self.config_path.parent.mkdir(exist_ok=True)
            with open(self.config_path, 'w') as f:
                json.dump(config, f, indent=2)
        
        # Create persona instances
        for persona_id, persona_config in config.items():
            self.personas[persona_id] = Persona(persona_id, persona_config)
            logger.info(f"Loaded persona: {persona_id} - {persona_config['name']}")
    
    def get_persona(self, persona_id: str) -> Optional[Persona]:
        """Get a specific persona"""
        return self.personas.get(persona_id)
    
    def list_personas(self) -> List[str]:
        """List all available persona IDs"""
        return list(self.personas.keys())
    
    def get_persona_info(self) -> Dict[str, Dict]:
        """Get information about all personas"""
        return {
            pid: {
                "name": p.name,
                "title": p.title,
                "description": p.description,
                "has_avatar": bool(p.avatar_id),
                "particle_theme": p.particle_theme
            }
            for pid, p in self.personas.items()
        }
    
    def persona_exists(self, persona_id: str) -> bool:
        """Check if a persona exists"""
        return persona_id in self.personas