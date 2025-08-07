import os
import requests
import time
from typing import Optional, Dict, Any, Union
import openai
from elevenlabs import generate, save, Voice, VoiceSettings
from pydantic import BaseModel
from config.settings import settings
import logging

logger = logging.getLogger(__name__)

class VoiceConfig(BaseModel):
    text: str
    voice_id: Optional[str] = None
    model_id: Optional[str] = "eleven_multilingual_v2"
    provider: str = "elevenlabs"  # "elevenlabs" or "openai"
    emotion: Optional[str] = None
    tempo: Optional[float] = 1.0
    stability: float = 0.48
    similarity_boost: float = 0.75
    style: Optional[float] = 0.0
    use_speaker_boost: bool = True

class VoiceService:
    def __init__(self):
        self.eleven_key = settings.ELEVEN_API_KEY
        self.openai_key = settings.OPENAI_API_KEY
        
        if self.openai_key:
            openai.api_key = self.openai_key
    
    async def generate_voice(self, config: VoiceConfig) -> bytes:
        """Generate voice-over from text using specified provider"""
        if config.provider == "elevenlabs":
            return await self._generate_elevenlabs(config)
        elif config.provider == "openai":
            return await self._generate_openai(config)
        else:
            raise ValueError(f"Unknown provider: {config.provider}")
    
    async def _generate_elevenlabs(self, config: VoiceConfig) -> bytes:
        """Generate voice using ElevenLabs API"""
        if not self.eleven_key:
            raise ValueError("ElevenLabs API key not configured")
        
        # Default voice IDs
        voice_map = {
            "narrator": "JBFqnCBsd6RMkjVDRZzb",  # George
            "female": "EXAVITQu4vr4xnSDxMaL",     # Bella
            "young": "jsCqWAovK2LkecY7zXl4",      # Adam
            "mature": "IKne3meq5aSn9XLyUdCD",     # Daniel
        }
        
        voice_id = config.voice_id or voice_map.get("narrator")
        
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": self.eleven_key,
            "Content-Type": "application/json"
        }
        
        payload = {
            "text": config.text,
            "model_id": config.model_id,
            "voice_settings": {
                "stability": config.stability,
                "similarity_boost": config.similarity_boost,
                "style": config.style,
                "use_speaker_boost": config.use_speaker_boost
            }
        }
        
        # Add emotion if specified
        if config.emotion:
            payload["voice_settings"]["emotion"] = config.emotion
        
        # Adjust tempo if needed
        if config.tempo != 1.0:
            payload["voice_settings"]["speed"] = config.tempo
        
        try:
            response = requests.post(
                f"{url}?output_format=mp3_44100_128",
                json=payload,
                headers=headers,
                timeout=60
            )
            response.raise_for_status()
            return response.content
        except requests.exceptions.RequestException as e:
            logger.error(f"ElevenLabs API error: {e}")
            raise
    
    async def _generate_openai(self, config: VoiceConfig) -> bytes:
        """Generate voice using OpenAI TTS API"""
        if not self.openai_key:
            raise ValueError("OpenAI API key not configured")
        
        # OpenAI voice options
        voice_map = {
            "alloy": "alloy",
            "echo": "echo",
            "fable": "fable",
            "onyx": "onyx",
            "nova": "nova",
            "shimmer": "shimmer"
        }
        
        voice = config.voice_id or "alloy"
        model = "tts-1-hd"  # Higher quality
        
        try:
            response = openai.audio.speech.create(
                model=model,
                voice=voice,
                input=config.text,
                speed=config.tempo
            )
            
            return response.content
        except Exception as e:
            logger.error(f"OpenAI TTS error: {e}")
            raise
    
    async def generate_voice_with_emotion(
        self,
        text: str,
        emotion: str,
        voice_id: Optional[str] = None
    ) -> bytes:
        """Generate voice with specific emotion"""
        config = VoiceConfig(
            text=text,
            emotion=emotion,
            voice_id=voice_id,
            stability=0.45,  # Lower for more expressive
            similarity_boost=0.8
        )
        return await self.generate_voice(config)
    
    async def generate_batch_voices(
        self,
        texts: list[str],
        voice_id: Optional[str] = None,
        provider: str = "elevenlabs"
    ) -> list[bytes]:
        """Generate multiple voice-overs in batch"""
        results = []
        for text in texts:
            config = VoiceConfig(
                text=text,
                voice_id=voice_id,
                provider=provider
            )
            audio = await self.generate_voice(config)
            results.append(audio)
            # Small delay to avoid rate limiting
            time.sleep(0.5)
        
        return results
    
    def get_voice_options(self, provider: str = "elevenlabs") -> Dict[str, Any]:
        """Get available voice options for a provider"""
        if provider == "elevenlabs":
            return {
                "voices": {
                    "narrator": "George - Warm, mature narrator",
                    "female": "Bella - Young female voice",
                    "young": "Adam - Young male voice",
                    "mature": "Daniel - Mature British accent"
                },
                "emotions": ["neutral", "happy", "sad", "angry", "surprised", "fear"],
                "models": ["eleven_multilingual_v2", "eleven_monolingual_v1"]
            }
        elif provider == "openai":
            return {
                "voices": {
                    "alloy": "Neutral, balanced",
                    "echo": "Warm, engaging",
                    "fable": "Expressive, dynamic",
                    "onyx": "Deep, authoritative",
                    "nova": "Friendly, conversational",
                    "shimmer": "Clear, articulate"
                },
                "models": ["tts-1", "tts-1-hd"]
            }
        else:
            return {}

# Singleton instance
voice_service = VoiceService()