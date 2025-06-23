from pydantic import BaseModel
from typing import List, Optional

class TTSRequest(BaseModel):
    text: str
    language: str = 'en-US'
    gender: str = 'female'
    emotion: str = 'neutral'
    output_filename: Optional[str] = None

class TTSResponse(BaseModel):
    duration_seconds: float
    language: str
    gender: str
    emotion: str
    voice_name: str

class SupportedLanguages(BaseModel):
    languages: List[str]

class SupportedVoices(BaseModel):
    voices: dict  # Will contain the voice mapping structure

class HealthResponse(BaseModel):
    status: str
    available_languages: List[str]
    available_emotions: List[str]