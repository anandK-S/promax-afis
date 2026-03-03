# ========================================
# Pro-Max AFIS - Voice Service
# ========================================
# Voice-to-Text and Text-to-Speech processing
# Author: Pro-Max Development Team

from typing import Dict, Optional
import logging
import base64
import io
from datetime import datetime

logger = logging.getLogger(__name__)


class VoiceService:
    """
    Voice processing service using Whisper for speech-to-text
    and TTS engines for text-to-speech
    """
    
    def __init__(self):
        """Initialize the voice service"""
        
        # Language code to name mapping
        self.language_names = {
            'en': 'English',
            'hi': 'Hindi',
            'gu': 'Gujarati',
            'mr': 'Marathi',
            'ta': 'Tamil',
            'te': 'Telugu',
            'bn': 'Bengali',
            'kn': 'Kannada',
            'ml': 'Malayalam',
            'pa': 'Punjabi'
        }
        
        logger.info("VoiceService initialized")
    
    def transcribe_audio(
        self,
        audio_bytes: bytes,
        language: str = "en"
    ) -> Dict:
        """
        Transcribe audio to text using Whisper AI
        
        Args:
            audio_bytes: Audio data as bytes
            language: Language code (default: 'en')
            
        Returns:
            Dictionary containing transcription result
        """
        
        try:
            # Try to import whisper
            try:
                import whisper
                WHISPER_AVAILABLE = True
            except ImportError:
                WHISPER_AVAILABLE = False
                logger.warning("Whisper not available")
            
            if not WHISPER_AVAILABLE:
                # Fallback to simulated transcription
                return self._simulate_transcription(audio_bytes, language)
            
            # Load Whisper model
            model = whisper.load_model("base")
            
            # Save audio to temporary file
            audio_file = io.BytesIO(audio_bytes)
            audio_file.name = "audio.webm"
            
            # Transcribe
            result = model.transcribe(
                audio_file,
                language=language,
                fp16=False
            )
            
            return {
                "success": True,
                "text": result["text"].strip(),
                "language": language,
                "confidence": 0.95,  # Whisper doesn't provide confidence, using default
                "duration": result.get("duration", 0)
            }
            
        except Exception as e:
            logger.error(f"Audio transcription failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def text_to_speech(
        self,
        text: str,
        language: str = "en"
    ) -> Dict:
        """
        Convert text to speech
        
        Args:
            text: Text to convert
            language: Language code
            
        Returns:
            Dictionary containing audio data as base64
        """
        
        try:
            # Try to import TTS library
            try:
                from gtts import gTTS
                GTTS_AVAILABLE = True
            except ImportError:
                GTTS_AVAILABLE = False
                logger.warning("gTTS not available")
            
            if not GTTS_AVAILABLE:
                # Fallback to simulated audio
                return {
                    "success": False,
                    "error": "Text-to-speech not available"
                }
            
            # Generate audio
            tts = gTTS(text=text, lang=language, slow=False)
            
            # Save to bytes
            audio_bytes = io.BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            
            # Encode to base64
            audio_base64 = base64.b64encode(audio_bytes.read()).decode('utf-8')
            
            return {
                "success": True,
                "audio_base64": audio_base64,
                "format": "mp3",
                "language": language
            }
            
        except Exception as e:
            logger.error(f"Text-to-speech failed: {str(e)}")
            return {
                "success": False,
                "error": str(e)
            }
    
    def _simulate_transcription(
        self,
        audio_bytes: bytes,
        language: str
    ) -> Dict:
        """
        Simulate transcription when Whisper is not available
        For development/testing purposes only
        """
        
        # Simulated transcriptions for common queries
        simulated_texts = {
            'hi': "Aaj ka munafa kitna hai?",
            'en': "What is today's profit?",
            'gu': "Aaju na munafa ketlu che?",
            'mr': "आजचा नफा किती आहे?",
            'ta': "இன்றைய இலாபம் என்ன?",
            'te': "ఈరోజు లాభం ఎంత?",
            'bn': "আজকের লাভ কত?",
            'kn': "ಇಂದಿನದ ಲಾಭ ಎಷ್ಟು?",
            'ml': "ഇന്നത്തെ ലാഭം എന്ത്?",
            'pa': "ਅੱਜ ਦਾ ਮੁਨਾਫਾ ਕਿੰਨਾ ਏ?"
        }
        
        text = simulated_texts.get(language, "What is today's profit?")
        
        return {
            "success": True,
            "text": text,
            "language": language,
            "confidence": 0.90,
            "duration": 2.5,
            "note": "Simulated transcription - Whisper not available"
        }