import edge_tts
import tempfile
import os
import asyncio
import uuid
from mutagen.mp3 import MP3
from typing import Dict, List, Optional
from ..models.tts_models import TTSRequest, TTSResponse, SupportedLanguages, SupportedVoices, HealthResponse

class TTSService:
    def __init__(self):
        self.default_voices = {
            'en-US': {'female': 'en-US-AriaNeural', 'male': 'en-US-GuyNeural'},
            'vi-VN': {'female': 'vi-VN-HoaiMyNeural', 'male': 'vi-VN-NamMinhNeural'},
            'ja-JP': {'female': 'ja-JP-NanamiNeural', 'male': 'ja-JP-KeitaNeural'},
            'ko-KR': {'female': 'ko-KR-SunHiNeural', 'male': 'ko-KR-InJoonNeural'},
            'zh-CN': {'female': 'zh-CN-XiaoxiaoNeural', 'male': 'zh-CN-YunxiNeural'},
            'es-ES': {'female': 'es-ES-ElviraNeural', 'male': 'es-ES-AlvaroNeural'},
            'fr-FR': {'female': 'fr-FR-DeniseNeural', 'male': 'fr-FR-HenriNeural'},
            'de-DE': {'female': 'de-DE-KatjaNeural', 'male': 'de-DE-ConradNeural'},
        }
        
        self.emotion_prosody = {
            'neutral': {'rate': '+0%', 'pitch': '+0Hz'},
            'cheerful': {'rate': '+10%', 'pitch': '+5Hz'},
            'sad': {'rate': '-15%', 'pitch': '-10Hz'},
            'angry': {'rate': '+5%', 'pitch': '-5Hz'},
            'excited': {'rate': '+20%', 'pitch': '+10Hz'},
            'formal': {'rate': '-5%', 'pitch': '+0Hz'},
            'funny': {'rate': '+10%', 'pitch': '+15Hz'},
            'calm': {'rate': '-10%', 'pitch': '-2Hz'},
            'whisper': {'rate': '-20%', 'pitch': '-5Hz'},
        }

    async def synthesize_speech(self, request: TTSRequest) -> Dict:
        try:
            if not request.text.strip():
                return {
                    'success': False,
                    'error': 'Text cannot be empty',
                    'status_code': 400
                }

            # Generate audio
            audio_file, duration, voice_name = await self._generate_audio(
                text=request.text,
                language=request.language,
                gender=request.gender,
                emotion=request.emotion,
                output_filename=request.output_filename
            )

            if not audio_file:
                return {
                    'success': False,
                    'error': 'Failed to generate audio',
                    'status_code': 500
                }

            # Read audio data
            with open(audio_file, 'rb') as f:
                audio_data = f.read()

            # Create metadata response
            metadata = TTSResponse(
                duration_seconds=duration,
                language=request.language,
                gender=request.gender,
                emotion=request.emotion,
                voice_name=voice_name
            )

            # Clean up temp file
            self.cleanup_file(audio_file)

            return {
                'success': True,
                'audio_data': audio_data,        # ← Raw binary data (bytes)
                'metadata': metadata,            # ← Metadata without URL
                'content_type': 'audio/mpeg',   # ← For HTTP response
                'status_code': 200
            }

        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status_code': 500
            }

    async def _generate_audio(
        self,
        text: str,
        language: str = 'en-US',
        gender: str = 'female',
        emotion: str = 'neutral',
        output_filename: Optional[str] = None
    ) -> tuple:
        # Generate unique filename if not provided
        if not output_filename:
            temp_dir = tempfile.gettempdir()
            unique_id = str(uuid.uuid4())
            output_filename = os.path.join(temp_dir, f"tts_{unique_id}.mp3")

        voice_name = self._get_voice_name(language, gender)
        
        # Get prosody settings for emotion
        prosody_settings = self.emotion_prosody.get(emotion, self.emotion_prosody['neutral'])
        current_rate = prosody_settings['rate']
        current_pitch = prosody_settings['pitch']

    
        communicate = edge_tts.Communicate(
            text=text,
            voice=voice_name,
            rate=current_rate,
            pitch=current_pitch
        )

        try:
            await communicate.save(output_filename)
            print(f"Successfully saved audio to: {output_filename}")
        except Exception as e:
            print(f"Error saving audio using communicate.save(): {e}")
            # Fallback to streaming
            audio_buffer = bytearray()
            try:
                async for chunk in communicate.stream():
                    if chunk["type"] == "audio":
                        audio_buffer.extend(chunk["data"])
                
                if not audio_buffer:
                    raise Exception("No audio data received from stream")
                
                with open(output_filename, "wb") as f:
                    f.write(audio_buffer)
                print(f"Successfully streamed and saved audio to: {output_filename}")
            except Exception as stream_e:
                raise Exception(f"Error streaming and saving audio: {stream_e}")

        # Get duration of the saved file
        duration_seconds = self._get_audio_duration(output_filename)
        
        return output_filename, duration_seconds, voice_name

    def _get_voice_name(self, language: str, gender: str) -> str:
        voice_map = self.default_voices.get(language, self.default_voices['en-US'])
        voice_name = voice_map.get(gender, voice_map.get('female') or voice_map.get('male'))
        
        if not voice_name:
            print(f"Could not find a voice for {language} / {gender}. Using default en-US-AriaNeural.")
            voice_name = 'en-US-AriaNeural'
        
        return voice_name

    def _get_audio_duration(self, file_path: str) -> float:
        duration_seconds = 0.0
        
        if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
            try:
                audio_info = MP3(file_path)
                duration_seconds = audio_info.info.length
                print(f"Duration of '{file_path}': {duration_seconds:.2f} seconds")
            except Exception as e:
                print(f"Error reading duration from '{file_path}': {e}")
                # Could add pydub fallback here if needed
        else:
            print(f"Output file '{file_path}' does not exist or is empty")
            
        return round(duration_seconds, 3)

    def get_supported_languages(self) -> SupportedLanguages:
        return SupportedLanguages(languages=list(self.default_voices.keys()))

    def get_supported_voices(self) -> SupportedVoices:
        return SupportedVoices(voices=self.default_voices)

    def get_supported_emotions(self) -> Dict[str, List[str]]:
        return {'emotions': list(self.emotion_prosody.keys())}

    def get_health_status(self) -> HealthResponse:
        return HealthResponse(
            status='ok',
            available_languages=list(self.default_voices.keys()),
            available_emotions=list(self.emotion_prosody.keys())
        )

    def cleanup_file(self, file_path: str):
        try:
            if file_path and os.path.exists(file_path):
                os.remove(file_path)
                print(f"Cleaned up file: {file_path}")
        except OSError as e:
            print(f"Error cleaning up file {file_path}: {e}")