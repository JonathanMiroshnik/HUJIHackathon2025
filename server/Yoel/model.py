"""
Model module for generating bilingual Hebrew-Arabic content using Gemini AI.
"""

import re
import sys
import os
import google.generativeai as genai
import google.auth
from server.Yoel.parser import extract_tagged_text

# Custom Gemini class with correct service account path
class FixedGemini:
    """
    Custom Gemini class that points to the correct service account file location.
    """
    
    # Available models with descriptions
    AVAILABLE_MODELS = {
        "gemini-1.5-flash": "Fast and versatile (recommended for beginners)",
        "gemini-1.5-pro": "Complex reasoning tasks (more powerful)",
        "gemini-2.0-flash": "Newest multimodal, fastest",
        "gemini-2.0-flash-lite": "Most cost-efficient",
        "gemini-2.5-flash-preview-05-20": "Best price-performance with thinking capabilities",
        "gemini-2.5-pro-preview-05-06": "Most powerful thinking model (advanced reasoning)"
    }

    def __init__(self):
        self.model = None
        self.chat = None
        self.model_name = None
        self._initialized = False
        
        # Correct path to the service account file
        self._SERVICE_ACCOUNT_FILE_PATH = os.path.join(
            os.path.dirname(__file__), 
            '..', 
            'services', 
            'LLM', 
            'hackathon-team-22_gen-lang-client-0325865525_iam_gserviceaccount_com_1747758084.json'
        )

    def init_model(self, model_name=None):
        """
        Initialize Gemini model.
        
        Args:
            model_name (str, optional): Model to use. Defaults to gemini-1.5-flash.
            
        Returns:
            FixedGemini: Ready-to-use Gemini instance
            
        Raises:
            Exception: If initialization fails
        """
        try:
            if model_name is None:
                model_name = "gemini-1.5-flash" #"gemini-1.5-flash"
            
            # Validate model
            if model_name not in self.AVAILABLE_MODELS:
                raise ValueError(f"Invalid model. Available: {list(self.AVAILABLE_MODELS.keys())}")

            print(f"🚀 Initializing model: {model_name}...")

            # Configure Google AI API with correct service account path
            service_account_path = os.path.abspath(self._SERVICE_ACCOUNT_FILE_PATH)
            
            if not os.path.exists(service_account_path):
                raise FileNotFoundError(f"Service account file not found at: {service_account_path}")

            try:
                credentials, _ = google.auth.load_credentials_from_file(service_account_path)
            except Exception as e:
                raise Exception(f"Failed to load credentials from {service_account_path}: {e}")

            genai.configure(credentials=credentials)

            # Create model and chat session
            self.model = genai.GenerativeModel(model_name)
            self.chat = self.model.start_chat()
            self.model_name = model_name
            self._initialized = True

            print(f"✅ Gemini {model_name} is ready!")
            return self

        except Exception as e:
            raise Exception(f"Failed to initialize Gemini: {e}")

    def ask(self, question, short_answer=True):
        """
        Ask Gemini a question and get a response
        
        Args:
            question (str): The question to ask
            short_answer (bool): Whether to request a concise answer
            
        Returns:
            str: Gemini's response
            
        Raises:
            Exception: If not initialized or API error occurs
        """
        if not self._initialized:
            raise Exception("Model not initialized. Call init_model() first!")

        if not question or not question.strip():
            raise ValueError("Question cannot be empty")

        try:
            # Prepare prompt
            if short_answer:
                prompt = f"{question}\n\nPlease provide a short, concise answer with minimal explanation."
            else:
                prompt = question

            # Get response
            response = self.chat.send_message(prompt)
            return response.text

        except Exception as e:
            raise Exception(f"Error getting response: {e}")


class BilingualContentGenerator:
    """
    A class to generate bilingual Hebrew-Arabic content using the Gemini AI API.
    """
    
    def __init__(self, model_name="gemini-1.5-flash"):
        """
        Initialize the bilingual content generator.
        
        Args:
            model_name (str): The Gemini model to use for content generation
        """
        self.gemini = FixedGemini()
        self.model_name = model_name
        self._initialized = False
        self.history = []
    
    def initialize(self):
        """
        Initialize the Gemini model.
        
        Raises:
            Exception: If initialization fails
        """
        try:
            self.gemini.init_model(self.model_name)
            self._initialized = True
            print(f"✅ BilingualContentGenerator initialized with {self.model_name}")
        except Exception as e:
            raise Exception(f"Failed to initialize BilingualContentGenerator: {e}")
    
    def generate_bilingual_content(self, prompt, max_retries=3):
        """
        Generate content with alternating Hebrew and Arabic segments.
        
        Args:
            prompt (str): The prompt to send to Gemini AI
            max_retries (int): Maximum number of attempts to get properly formatted content
            
        Returns:
            str: Generated content with proper <he>...</he> and <ar>...</ar> tags
            
        Raises:
            Exception: If not initialized, API error occurs, or proper formatting cannot be achieved
        """
        if not self._initialized:
            raise Exception("Generator not initialized. Call initialize() first!")
        
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty")
        
        # Adding human input to history
        self.history.append(prompt)

        # Enhanced prompt to ensure proper bilingual formatting
        enhanced_prompt = f"""
        {prompt}
        
        IMPORTANT FORMATTING REQUIREMENTS:
        - Generate content that contains both Hebrew and Arabic text, but never generate in English.
        - Hebrew text must be enclosed in <he>...</he> tags
        - Arabic text must be enclosed in <ar>...</ar> tags
        - Alternate between Hebrew and Arabic segments
        - Write up to 3 segments in total in the response.
        - The first Hebrew sentence should be long and useful in terms of study.
        - Ensure both languages are present in the response
        - Create a natural flowing narrative that switches between the two languages
        - Example format: <he>Hebrew text here</he> <ar>Arabic text here</ar> <he>More Hebrew</he> <ar>More Arabic</ar>
        """
        
        for attempt in range(max_retries):
            try:
                # Get response from Gemini
                response = self.gemini.ask(enhanced_prompt, short_answer=False)
                
                # Validate and format the response
                formatted_response = self._validate_and_format_response(response)
                
                if formatted_response:
                    # Adding human output to history
                    self.history.append(formatted_response)                    
                    return formatted_response
                else:
                    print(f"⚠️ Attempt {attempt + 1} failed: Response doesn't contain proper bilingual content")
                    
            except Exception as e:
                print(f"⚠️ Attempt {attempt + 1} failed with error: {e}")
                
                if attempt == max_retries - 1:
                    raise Exception(f"Failed to generate proper bilingual content after {max_retries} attempts: {e}")
        
        raise Exception(f"Failed to generate properly formatted bilingual content after {max_retries} attempts")
    
    def _validate_and_format_response(self, response):
        """
        Validate and format the response to ensure proper Hebrew/Arabic tagging.
        
        Args:
            response (str): Raw response from Gemini
            
        Returns:
            str: Properly formatted response or None if validation fails
        """
        if not response:
            return None
        
        # Check if response already has proper tags
        he_tags = re.findall(r'<he>.*?</he>', response, re.DOTALL)
        ar_tags = re.findall(r'<ar>.*?</ar>', response, re.DOTALL)
        
        # If we have both Hebrew and Arabic tags, consider it valid
        if he_tags and ar_tags:
            # Clean up any extra whitespace and ensure proper formatting
            cleaned_response = re.sub(r'\s+', ' ', response).strip()
            return cleaned_response
        
        # Try to detect Hebrew and Arabic text and add tags
        return self._attempt_auto_tagging(response)
    
    def _attempt_auto_tagging(self, text):
        """
        Attempt to automatically detect and tag Hebrew and Arabic text.
        
        Args:
            text (str): Text to analyze and tag
            
        Returns:
            str: Tagged text or None if proper detection fails
        """
        # Hebrew Unicode range: \u0590-\u05FF
        # Arabic Unicode range: \u0600-\u06FF, \u0750-\u077F, \u08A0-\u08FF
        
        hebrew_pattern = r'[\u0590-\u05FF]+'
        arabic_pattern = r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF]+'
        
        has_hebrew = bool(re.search(hebrew_pattern, text))
        has_arabic = bool(re.search(arabic_pattern, text))
        
        # Only proceed if we have both languages
        if not (has_hebrew and has_arabic):
            return None
        
        # Split text into segments and try to tag them
        # This is a simplified approach - in a production system, 
        # you might want more sophisticated language detection
        segments = re.split(r'([.!?]\s+)', text)
        tagged_segments = []
        
        for segment in segments:
            segment = segment.strip()
            if not segment:
                continue
                
            if re.search(hebrew_pattern, segment):
                tagged_segments.append(f"<he>{segment}</he>")
            elif re.search(arabic_pattern, segment):
                tagged_segments.append(f"<ar>{segment}</ar>")
            else:
                # For punctuation or other text, append to previous segment if exists
                if tagged_segments:
                    # Remove the closing tag, add the segment, and re-add closing tag
                    last_segment = tagged_segments[-1]
                    if last_segment.endswith('</he>'):
                        tagged_segments[-1] = last_segment[:-5] + segment + '</he>'
                    elif last_segment.endswith('</ar>'):
                        tagged_segments[-1] = last_segment[:-5] + segment + '</ar>'
                    else:
                        tagged_segments.append(segment)
                else:
                    tagged_segments.append(segment)
        
        result = ' '.join(tagged_segments)
        
        # Final validation
        if '<he>' in result and '<ar>' in result:
            return result
        
        return None


def generate_bilingual_content(prompt, model_name="gemini-1.5-flash", max_retries=3):
    """
    Convenience function to generate bilingual Hebrew-Arabic content.
    
    Args:
        prompt (str): The prompt to send to Gemini AI
        model_name (str): The Gemini model to use
        max_retries (int): Maximum number of attempts to get properly formatted content
        
    Returns:
        str: Generated content with proper <he>...</he> and <ar>...</ar> tags
        
    Raises:
        Exception: If initialization fails, API error occurs, or proper formatting cannot be achieved
    """
    generator = BilingualContentGenerator(model_name)
    generator.initialize()
    return generator.generate_bilingual_content(prompt, max_retries)


# Example usage and testing function
def test_bilingual_generation():
    """
    Test function to demonstrate the bilingual content generation.
    """
    try:
        print("🧪 Testing bilingual content generation...")
        
        # Test prompt
        prompt = "Write a short story about a person going to the market and meeting people from different cultures. Include dialogue and descriptions in both Hebrew and Arabic."
        
        # Generate content
        result = generate_bilingual_content(prompt)
        
        print("✅ Generated bilingual content:")
        print("-" * 50)
        print(result)
        print("-" * 50)
        
        # Validate the result
        he_count = result.count('<he>')
        ar_count = result.count('<ar>')
        
        print(f"📊 Hebrew segments: {he_count}")
        print(f"📊 Arabic segments: {ar_count}")
        
        if he_count > 0 and ar_count > 0:
            print("✅ Test passed: Content contains both Hebrew and Arabic segments!")
        else:
            print("❌ Test failed: Content missing Hebrew or Arabic segments")
            
    except Exception as e:
        print(f"❌ Test failed with error: {e}")


if __name__ == "__main__":
    # Run test if script is executed directly
    test_bilingual_generation()
