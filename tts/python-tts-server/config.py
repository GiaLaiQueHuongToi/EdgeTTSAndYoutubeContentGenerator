# Configuration settings for the TTS server

class Config:
    DEBUG = True  # Set to False in production
    SERVER_PORT = 9999  # Port for the server to run on
    SERVER_HOST = '0.0.0.0'
    
    # Edge TTS settings
    DEFAULT_VOICE = 'en-US-AriaNeural'
    DEFAULT_RATE = '+0%'
    DEFAULT_PITCH = '+0Hz'
    
    # File settings
    TEMP_AUDIO_DIR = 'temp_audio'
    MAX_TEXT_LENGTH = 5000  # Limit text length for safety
    
    # Supported voice styles for different emotions
    VOICE_STYLES = {
        'neutral': '',
        'cheerful': 'cheerful',
        'sad': 'sad',
        'angry': 'angry',
        'excited': 'excited',
        'friendly': 'friendly',
        'hopeful': 'hopeful',
        'shouting': 'shouting',
        'terrified': 'terrified',
        'unfriendly': 'unfriendly',
        'whispering': 'whispering'
    }
    
    # Popular voices with emotion support
    EMOTION_SUPPORTED_VOICES = [
        # English voices
        'en-US-AriaNeural',
        'en-US-JennyNeural',
        'en-US-GuyNeural',
        'en-GB-SoniaNeural',
        'en-AU-NatashaNeural',
        # Vietnamese voices
        'vi-VN-NamMinhNeural',
        'vi-VN-HoaiMyNeural'
    ]
    
    # Vietnamese specific voices
    VIETNAMESE_VOICES = {
        'male': 'vi-VN-NamMinhNeural',
        'female': 'vi-VN-HoaiMyNeural'
    }
    
    # Default Vietnamese voice
    DEFAULT_VIETNAMESE_VOICE = 'vi-VN-HoaiMyNeural'

class ProductionConfig(Config):
    DEBUG = False

class DevelopmentConfig(Config):
    DEBUG = True

# Default config
config = DevelopmentConfig()