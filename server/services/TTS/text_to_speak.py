"""
Google TTS Service - Offline Text-to-Speech Conversion

This module provides functions to convert text to speech using Google's Text-to-Speech (gTTS) service.
It offers an offline mode that works without continuous internet connection (after initial download).

Language codes: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
Example codes: 'en' (English), 'es' (Spanish), 'fr' (French), 'he' (Hebrew), 'ar' (Arabic)

Example usage:
    from text_to_speech import convert_text_to_speech_offline
    
    # Basic usage with default parameters (English)
    audio_path = convert_text_to_speech_offline("Hello, this is a test")
    
    # Advanced usage with custom language and output path
    audio_path = convert_text_to_speech_offline(
        text="Hola, esto es una prueba",
        language="es",  # Spanish
        output_file="spanish_output.mp3"
    )
"""

from gtts import gTTS
from typing import Optional
from playsound3 import playsound


# Configure minimal logging
import logging
logging.basicConfig(level=logging.WARNING)

# Default values
DEFAULT_OUTPUT_PATH = "output.mp3"
DEFAULT_LANGUAGE = "en"  # English

# Common language codes
LANG_ENGLISH = "en"
LANG_SPANISH = "es" 
LANG_FRENCH = "fr"
LANG_HEBREW = "he"
LANG_ARABIC = "ar"
LANG_GERMAN = "de"
LANG_ITALIAN = "it"
LANG_JAPANESE = "ja"
LANG_CHINESE = "zh"
LANG_RUSSIAN = "ru"

class TextToSpeechConverter:
    def convert_text_to_speech_offline(self, text: str, output_file: Optional[str] = DEFAULT_OUTPUT_PATH, 
                                    language: str = DEFAULT_LANGUAGE, slow: bool = False) -> str:
        """
        Convert text to speech using Google's offline Text-to-Speech service.
        
        Args:
            text (str): The text to convert to speech
            output_file (str): The name of the output audio file (default: "output.mp3")
            language (str): The language code (default: "en" for English)
                            See: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
            slow (bool): If True, speaks more slowly (default: False)
        
        Returns:
            str: Path to the generated audio file
            
        Examples:
            # Basic usage
            path = convert_text_to_speech_offline("Hello world")
            
            # With custom language and output path
            path = convert_text_to_speech_offline(
                text="Bonjour le monde", 
                language="fr",  # French
                output_file="french_audio.mp3"
            )
            
            # With slow speech
            path = convert_text_to_speech_offline(
                text="This is spoken slowly",
                slow=True
            )
        """
        try:
            print("[1/3] Starting offline text-to-speech conversion...")
            print(f"[2/3] Converting text to speech (language: {language})...")
            
            tts = gTTS(text=text, lang=language, slow=slow)
            
            print(f"[3/3] Saving audio file to {output_file}...")
            tts.save(output_file)
            
            print(f"✓ Offline TTS completed successfully! File saved to {output_file}")
            return output_file

        except Exception as e:
            print(f"❌ Error: Failed to convert text to speech: {str(e)}")
            raise


    def exelarate(self, sample_text_arabic):
        output_file_arabic = "arabic_output.mp3"
        print(f"Converting Arabic sample text to speech...")
        result_path = self.convert_text_to_speech_offline(
            sample_text_arabic,
            output_file=output_file_arabic,
            language=LANG_ARABIC  # explicitly using Arabic language code
        )
        print(f"Arabic audio saved to: {result_path}")
        playsound('arabic_output.mp3')


# if __name__ == "__main__":
#     # Arabic example
#     tts = TextToSpeechConverter()
#     tts.exelarate("مرحبا بك في عالم البرمجة")
