"""
Microsoft Edge TTS Service - Online Text-to-Speech Conversion

This module provides functions to convert text to speech using Microsoft's Edge TTS online service.
It requires an internet connection but offers high-quality voices.

Available voices can be found at: https://speech.microsoft.com/portal/voicegallery

Example usage:
    from edge_tts_service import edge_tts_convert
    
    # Basic usage with default parameters
    audio_path = edge_tts_convert("Hello, this is a test")
    
    # Advanced usage with custom voice and output path
    audio_path = edge_tts_convert(
        text="Hello, this is a test",
        voice="en-US-SteffanNeural",  # Male voice
        output_path="custom_output.mp3"
    )
"""

import asyncio
from typing import Optional

import edge_tts

# Configure minimal logging
import logging

logging.basicConfig(level=logging.WARNING)

# Common voice options
VOICE_FEMALE_US = "en-US-EmmaMultilingualNeural"
VOICE_MALE_US = "en-US-SteffanNeural"
VOICE_FEMALE_UK = "en-GB-SoniaNeural"
VOICE_MALE_UK = "en-GB-RyanNeural"
VOICE_HEBREW_FEMALE = "he-IL-HilaNeural"
VOICE_HEBREW_MALE = "he-IL-AvriNeural"
VOICE_ARABIC_FEMALE = "ar-SA-ZariyahNeural"
VOICE_ARABIC_MALE = "ar-SA-HamedNeural"
VOICE_SPANISH_FEMALE = "es-ES-ElviraNeural"
VOICE_SPANISH_MALE = "es-ES-AlvaroNeural"

# Default values
DEFAULT_OUTPUT_PATH = 'output.mp3'
DEFAULT_VOICE = VOICE_FEMALE_US


async def convert_text_to_speech_online(text: str, voice: str, output_path: str) -> str:
    """
    Convert text to speech using Microsoft Edge TTS (online service).
    
    Args:
        text (str): Text to convert to speech
        voice (str): Voice to use for speech synthesis
        output_path (str): Path to save the output audio file
        
    Returns:
        str: Path to the created audio file
    """
    tts = edge_tts.Communicate(text=text, voice=voice, rate="-10%")
    await tts.save(output_path)
    return output_path


def edge_tts_convert(text: str, voice: Optional[str] = DEFAULT_VOICE,
                     output_path: Optional[str] = DEFAULT_OUTPUT_PATH) -> str:
    """
    Convert text to speech using Microsoft Edge TTS (online service).
    This is a synchronous wrapper for the async function.
    
    Args:
        text (str): Text to convert to speech
        voice (str): Voice to use for speech synthesis (default: en-US-EmmaMultilingualNeural)
        output_path (str): Path to save the output audio file (default: output.mp3)
        
    Returns:
        str: Path to the created audio file
        
    Examples:
        # Basic usage
        path = edge_tts_convert("Hello world")
        
        # With custom voice and output path
        path = edge_tts_convert(
            text="Testing text to speech",
            voice="en-US-SteffanNeural", 
            output_path="custom_file.mp3"
        )
    """
    print("[1/3] Starting online text-to-speech conversion (Microsoft Edge TTS)...")
    print(f"[2/3] Converting text using voice: {voice}...")
    result = asyncio.run(convert_text_to_speech_online(text, voice, output_path))
    print(f"[3/3] Audio saved to {output_path}")
    print(f"✓ Online TTS completed successfully!")
    return result


# # Example usage
# if __name__ == "__main__":
#     # Simple example of converting text to speech
#     sample_text = "Hello, this is a test of the Microsoft Edge text to speech service."
#     output_file = "edge_tts_example.mp3"

#     print(f"Converting sample text to speech...")
#     result_path = edge_tts_convert(sample_text, output_path=output_file)
#     print(f"Audio saved to: {result_path}")

#     # Multilingual example (uncomment to test)
#     # voices_and_texts = {
#     #     VOICE_MALE_US: "This is an American male voice.",
#     #     VOICE_FEMALE_UK: "This is a British female voice.",
#     #     VOICE_HEBREW_FEMALE: "זוהי דוגמה לקול נשי בעברית.",
#     #     VOICE_SPANISH_MALE: "Esta es una voz masculina en español."
#     # }
#     # for voice, text in voices_and_texts.items():
#     #     output = f"{voice.split('-')[0]}_example.mp3"
#     #     edge_tts_convert(text=text, voice=voice, output_path=output)
