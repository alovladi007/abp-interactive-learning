import os
import requests
import time
import json
from typing import Optional, Dict, Any, List
from pydantic import BaseModel
from config.settings import settings
import logging
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)

class MusicConfig(BaseModel):
    prompt: str
    duration: int = 60  # seconds
    genre: Optional[str] = None
    mood: Optional[str] = None
    tempo: Optional[int] = 90  # BPM
    instruments: Optional[List[str]] = None
    provider: str = "suno"  # "suno" or "musicgen"
    model_version: str = "V4_5"
    instrumental: bool = True
    quality: str = "high"  # "low", "medium", "high"

class MusicService:
    def __init__(self):
        self.suno_key = settings.SUNO_API_KEY
        self.suno_base_url = "https://api.sunoapi.org"
        
    async def generate_music(self, config: MusicConfig) -> Dict[str, Any]:
        """Generate music based on configuration"""
        if config.provider == "suno":
            return await self._generate_suno(config)
        elif config.provider == "musicgen":
            return await self._generate_musicgen(config)
        else:
            raise ValueError(f"Unknown provider: {config.provider}")
    
    async def _generate_suno(self, config: MusicConfig) -> Dict[str, Any]:
        """Generate music using Suno API"""
        if not self.suno_key:
            raise ValueError("Suno API key not configured")
        
        # Build enhanced prompt
        prompt_parts = [config.prompt]
        
        if config.instrumental:
            prompt_parts.append("instrumental")
        
        if config.genre:
            prompt_parts.append(f"{config.genre} genre")
        
        if config.mood:
            prompt_parts.append(f"{config.mood} mood")
        
        if config.tempo:
            prompt_parts.append(f"{config.tempo} BPM")
        
        if config.instruments:
            prompt_parts.append(f"featuring {', '.join(config.instruments)}")
        
        # Add quality descriptors
        if config.quality == "high":
            prompt_parts.extend(["high-fidelity", "studio quality", "mastered"])
        
        enhanced_prompt = ", ".join(prompt_parts)
        
        url = f"{self.suno_base_url}/generate-music"
        headers = {
            "x-api-key": self.suno_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "prompt": enhanced_prompt,
            "model": config.model_version,
            "duration": config.duration,
            "stream": False,
            "instrumental": config.instrumental
        }
        
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers,
                timeout=120
            )
            response.raise_for_status()
            
            result = response.json()
            
            return {
                "url": result.get("music_url"),
                "id": result.get("generation_id"),
                "duration": config.duration,
                "prompt": enhanced_prompt,
                "provider": "suno",
                "created_at": datetime.utcnow().isoformat()
            }
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Suno API error: {e}")
            raise
    
    async def _generate_musicgen(self, config: MusicConfig) -> Dict[str, Any]:
        """Generate music using local MusicGen model"""
        # This would integrate with a local MusicGen deployment
        # For now, returning a placeholder
        logger.info("MusicGen integration not yet implemented")
        
        return {
            "url": None,
            "id": f"musicgen_{int(time.time())}",
            "duration": config.duration,
            "prompt": config.prompt,
            "provider": "musicgen",
            "created_at": datetime.utcnow().isoformat(),
            "status": "pending_implementation"
        }
    
    async def generate_cinematic_music(
        self,
        scene_description: str,
        duration: int = 60,
        climax_at: Optional[int] = None
    ) -> Dict[str, Any]:
        """Generate cinematic music for video scenes"""
        
        # Build cinematic prompt
        prompt_parts = [
            f"Cinematic instrumental music for: {scene_description}",
            "orchestral elements",
            "emotional depth",
            "film score quality"
        ]
        
        if climax_at:
            prompt_parts.append(f"building to climax at {climax_at} seconds")
        
        config = MusicConfig(
            prompt=" ".join(prompt_parts),
            duration=duration,
            genre="cinematic",
            mood="epic",
            instrumental=True,
            quality="high"
        )
        
        return await self.generate_music(config)
    
    async def generate_background_music(
        self,
        style: str,
        duration: int = 60,
        energy_level: str = "medium"
    ) -> Dict[str, Any]:
        """Generate background music for different content types"""
        
        style_presets = {
            "corporate": {
                "genre": "corporate",
                "mood": "uplifting",
                "instruments": ["piano", "strings", "light percussion"]
            },
            "tutorial": {
                "genre": "ambient",
                "mood": "calm",
                "instruments": ["soft synths", "gentle piano"]
            },
            "action": {
                "genre": "electronic",
                "mood": "energetic",
                "instruments": ["synths", "drums", "bass"]
            },
            "emotional": {
                "genre": "orchestral",
                "mood": "emotional",
                "instruments": ["strings", "piano", "woodwinds"]
            }
        }
        
        preset = style_presets.get(style, style_presets["corporate"])
        
        # Adjust tempo based on energy level
        tempo_map = {
            "low": 70,
            "medium": 90,
            "high": 120,
            "very_high": 140
        }
        
        config = MusicConfig(
            prompt=f"{style} background music, {energy_level} energy",
            duration=duration,
            genre=preset["genre"],
            mood=preset["mood"],
            tempo=tempo_map.get(energy_level, 90),
            instruments=preset["instruments"],
            instrumental=True,
            quality="high"
        )
        
        return await self.generate_music(config)
    
    async def generate_music_variations(
        self,
        base_prompt: str,
        num_variations: int = 3,
        duration: int = 60
    ) -> List[Dict[str, Any]]:
        """Generate multiple variations of a music theme"""
        
        variations = []
        moods = ["uplifting", "dramatic", "peaceful"]
        tempos = [80, 100, 120]
        
        for i in range(min(num_variations, 3)):
            config = MusicConfig(
                prompt=f"{base_prompt} - variation {i+1}",
                duration=duration,
                mood=moods[i],
                tempo=tempos[i],
                instrumental=True,
                quality="high"
            )
            
            result = await self.generate_music(config)
            variations.append(result)
            
            # Delay to avoid rate limiting
            await asyncio.sleep(2)
        
        return variations
    
    def get_music_presets(self) -> Dict[str, Any]:
        """Get available music generation presets"""
        return {
            "genres": [
                "cinematic", "corporate", "ambient", "electronic",
                "orchestral", "rock", "jazz", "classical", "world"
            ],
            "moods": [
                "uplifting", "dramatic", "peaceful", "energetic",
                "mysterious", "happy", "sad", "tense", "relaxing"
            ],
            "instruments": [
                "piano", "strings", "brass", "woodwinds", "percussion",
                "synths", "guitar", "bass", "drums", "vocals"
            ],
            "quality_levels": ["low", "medium", "high"],
            "duration_limits": {
                "min": 10,
                "max": 300,
                "recommended": 60
            }
        }

# Singleton instance
music_service = MusicService()