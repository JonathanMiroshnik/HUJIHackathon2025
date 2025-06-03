"""
Utility Functions for Speech and Text Processing

This module contains helper functions used across the project for speech-to-text 
conversion and formatted display of information.

Example usage:
    from utils import transcribe_audio_to_text, print_title
    
    # Transcribe an audio file to text.
    text = transcribe_audio_to_text("recording.mp3", "medium")
    
    # Print a formatted title
    print_title("Transcription Result")
    print(text)
"""

from speech_to_text import convert_speech_to_text
from typing import Optional


def transcribe_audio_to_text(audio_file_path: str, model_type: str = "base") -> str:
    """
    Convert an audio file to text using speech recognition.
    A convenient wrapper around the speech_to_text conversion function.

    Args:
        audio_file_path (str): Path to your audio file (supports mp3, wav, m4a, etc.)
        model_type (str): Which model to use for transcription:
            - "fast": Quick transcription, good for most cases
            - "base" (default): Better accuracy, but slower
            - "small": High accuracy, even slower
            - "medium": Best accuracy, slowest

    Returns:
        str: The transcribed text from your audio file
        
    Examples:
        # Basic usage with default model (base)
        text = transcribe_audio_to_text("recording.mp3")
        
        # Using a faster model
        text = transcribe_audio_to_text("recording.mp3", "fast")
        
        # Using the most accurate model
        text = transcribe_audio_to_text("important_interview.mp3", "medium")
    """
    return convert_speech_to_text(audio_file_path, model_type=model_type.lower())


# def text_to_audio(text, output_file="output.mp3", slow=False):
#     """
#     Convert text to an audio file using text-to-speech.
#     Great for creating voice-overs, audio guides, or accessibility features.
#
#     Args:
#         text (str): The English text you want to convert to speech
#         output_file (str): Where to save the audio file (default: "output.mp3")
#         slow (bool): If True, speaks more slowly (default: False)
#
#     Returns:
#         str: Path to the created audio file
#     """
#     return convert_text_to_speech(text, output_file=output_file, slow=slow)


def print_title(title: str) -> None:
    """
    Print a formatted title with separator lines.
    
    Args:
        title (str): The title text to display
        
    Example:
        print_title("Processing Results")
        # Output:
        # ================================================================================
        # ==============================  Processing Results  ============================
        # ================================================================================
    """
    terminal_width = 80
    
    # Create top and bottom borders
    border = "=" * terminal_width
    
    # Calculate padding for centered title
    padding = (terminal_width - len(title) - 4) // 2
    title_line = "=" * padding + "  " + title + "  " + "=" * padding
    
    # Adjust if odd length
    if len(title_line) < terminal_width:
        title_line += "="
    
    # Print formatted title
    print("\n" + border)
    print(title_line)
    print(border)


# # Example usage
# if __name__ == "__main__":
#     # Example of printing a title
#     print_title("Example Title")
    
#     # Example of transcription (commented out as it requires an audio file)
#     # text = transcribe_audio_to_text("example.mp3", "fast")
#     # print(f"Transcription result: {text[:50]}...")
