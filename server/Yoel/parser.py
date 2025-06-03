"""
Parser module for extracting Hebrew and Arabic text from tagged content.
"""

import re
from typing import List, Tuple


def extract_tagged_text(text: str) -> List[Tuple[str, str]]:
    """
    Extract Hebrew and Arabic text from a string containing <he> and <ar> tags.
    
    Args:
        text (str): Input string containing Hebrew and Arabic text with tags
                   like <he>Hebrew text</he> and <ar>Arabic text</ar>
    
    Returns:
        List[Tuple[str, str]]: List of tuples where each tuple contains:
                              - The extracted text (without tags)
                              - The language identifier ("Hebrew" or "Arabic")
                              
    Examples:
        >>> text = "<he>שלום</he> <ar>مرحبا</ar> some untagged text <he>עולם</he>"
        >>> extract_tagged_text(text)
        [('שלום', 'Hebrew'), ('مرحبا', 'Arabic'), ('עולם', 'Hebrew')]
        
        >>> text = "<he>incomplete tag and <ar>العربية</ar> normal <he>עברית</he>"
        >>> extract_tagged_text(text)
        [('العربية', 'Arabic'), ('עברית', 'Hebrew')]
    """
    if not text or not isinstance(text, str):
        return []
    
    result = []
    
    # Find all Hebrew tags with their content
    # Using re.DOTALL to match newlines within tags
    hebrew_pattern = r'<he>(.*?)</he>'
    hebrew_matches = re.finditer(hebrew_pattern, text, re.DOTALL)
    
    # Find all Arabic tags with their content
    arabic_pattern = r'<ar>(.*?)</ar>'
    arabic_matches = re.finditer(arabic_pattern, text, re.DOTALL)
    
    # Collect all matches with their positions to preserve order
    all_matches = []
    
    # Add Hebrew matches
    for match in hebrew_matches:
        content = match.group(1).strip()
        if content:  # Only add non-empty content
            all_matches.append((match.start(), content, "Hebrew"))
    
    # Add Arabic matches
    for match in arabic_matches:
        content = match.group(1).strip()
        if content:  # Only add non-empty content
            all_matches.append((match.start(), content, "Arabic"))
    
    # Sort by position to preserve original order
    all_matches.sort(key=lambda x: x[0])
    
    # Extract just the content and language, discarding position
    result = [(content, language) for _, content, language in all_matches]
    
    return result


def extract_hebrew_text(text: str) -> List[str]:
    """
    Extract only Hebrew text from tagged content.
    
    Args:
        text (str): Input string containing Hebrew text with <he> tags
        
    Returns:
        List[str]: List of Hebrew text segments
    """
    tagged_content = extract_tagged_text(text)
    return [content for content, language in tagged_content if language == "Hebrew"]


def extract_arabic_text(text: str) -> List[str]:
    """
    Extract only Arabic text from tagged content.
    
    Args:
        text (str): Input string containing Arabic text with <ar> tags
        
    Returns:
        List[str]: List of Arabic text segments
    """
    tagged_content = extract_tagged_text(text)
    return [content for content, language in tagged_content if language == "Arabic"]


def count_language_segments(text: str) -> Tuple[int, int]:
    """
    Count the number of Hebrew and Arabic segments in tagged text.
    
    Args:
        text (str): Input string containing tagged content
        
    Returns:
        Tuple[int, int]: (hebrew_count, arabic_count)
    """
    tagged_content = extract_tagged_text(text)
    hebrew_count = sum(1 for _, language in tagged_content if language == "Hebrew")
    arabic_count = sum(1 for _, language in tagged_content if language == "Arabic")
    return (hebrew_count, arabic_count)


def validate_bilingual_content(text: str, min_segments: int = 2) -> bool:
    """
    Validate that the text contains both Hebrew and Arabic segments.
    
    Args:
        text (str): Input string containing tagged content
        min_segments (int): Minimum number of segments required for each language
        
    Returns:
        bool: True if content contains both languages with minimum segments
    """
    hebrew_count, arabic_count = count_language_segments(text)
    return hebrew_count >= min_segments and arabic_count >= min_segments


def clean_tagged_text(text: str) -> str:
    """
    Remove all tags from the text, leaving only the content.
    
    Args:
        text (str): Input string containing tagged content
        
    Returns:
        str: Clean text without any tags
    """
    if not text or not isinstance(text, str):
        return ""
    
    # Remove Hebrew tags
    text = re.sub(r'<he>(.*?)</he>', r'\1', text, flags=re.DOTALL)
    
    # Remove Arabic tags
    text = re.sub(r'<ar>(.*?)</ar>', r'\1', text, flags=re.DOTALL)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text


def format_tagged_text(segments: List[Tuple[str, str]]) -> str:
    """
    Format a list of text segments back into tagged format.
    
    Args:
        segments: List of tuples (text, language) where language is "Hebrew" or "Arabic"
        
    Returns:
        str: Formatted text with appropriate tags
    """
    result = []
    
    for text, language in segments:
        if language == "Hebrew":
            result.append(f"<he>{text}</he>")
        elif language == "Arabic":
            result.append(f"<ar>{text}</ar>")
        else:
            # Skip unknown languages
            continue
    
    return " ".join(result)


# Test function to demonstrate usage
def test_extract_tagged_text():
    """
    Test function to demonstrate the extract_tagged_text function.
    """
    print("🧪 Testing extract_tagged_text function")
    print("=" * 50)
    
    test_cases = [
        # Normal case with both languages
        "<he>שלום עולם</he> <ar>مرحبا بالعالم</ar> <he>איך שלומך?</he>",
        
        # Missing closing tags
        "<he>שלום incomplete and <ar>مرحبا</ar> normal <he>עברית</he>",
        
        # Empty tags
        "<he></he> <ar>مرحبا</ar> <he>שלום</he> <ar></ar>",
        
        # Mixed with untagged text
        "Some English text <he>עברית</he> more English <ar>عربي</ar> end",
        
        # Only Hebrew
        "<he>רק עברית</he> <he>עוד עברית</he>",
        
        # Only Arabic
        "<ar>عربي فقط</ar> <ar>المزيد من العربية</ar>",
        
        # Malformed tags
        "<he>Hebrew without closing <ar>عربي</ar> <he>עברית</he>",
        
        # Empty string
        "",
        
        # No tags
        "Just regular text without any tags",
        
        # Nested or complex content
        "<he>התעוררתי מוקדם בבוקר,</he> <ar>وذهبت إلى المقهى القريب من منزلي.</ar>"
    ]
    
    for i, test_text in enumerate(test_cases, 1):
        print(f"\nTest {i}:")
        print(f"Input: {test_text[:60]}{'...' if len(test_text) > 60 else ''}")
        
        try:
            result = extract_tagged_text(test_text)
            print(f"Output: {result}")
            
            # Additional analysis
            hebrew_count, arabic_count = count_language_segments(test_text)
            print(f"Hebrew segments: {hebrew_count}, Arabic segments: {arabic_count}")
            
            is_valid = validate_bilingual_content(test_text, min_segments=1)
            print(f"Is bilingual: {'✅' if is_valid else '❌'}")
            
        except Exception as e:
            print(f"Error: {e}")
    
    print("\n" + "=" * 50)
    print("✅ Testing completed!")


# if __name__ == "__main__":
#     # Run tests if script is executed directly
#     test_extract_tagged_text()
