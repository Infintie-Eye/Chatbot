"""
Gemini API client for handling text, image, and file processing.
Updated for Gemini 2.0 Flash model with enhanced capabilities.
"""
import logging
import base64
import io
from typing import Dict, List, Any, Optional, Union
from PIL import Image
import google.generativeai as genai
from tenacity import retry, stop_after_attempt, wait_exponential
from config.settings import settings

# Configure logging
logger = logging.getLogger(__name__)

class GeminiClient:
    """Client for interacting with Google's Gemini 2.0 Flash API."""

    def __init__(self):
        """Initialize the Gemini client with 2.0 Flash model."""
        if not settings.gemini_api_key:
            raise ValueError("Gemini API key is required")

        genai.configure(api_key=settings.gemini_api_key)

        # Use the same model for both text and vision (Gemini 2.0 Flash supports both)
        self.model = genai.GenerativeModel(settings.text_model)

        # Enhanced generation config for Gemini 2.0 Flash
        self.generation_config = genai.types.GenerationConfig(
            temperature=settings.temperature,
            max_output_tokens=settings.max_tokens,
            top_p=0.95,  # Increased for better creativity
            top_k=64,  # Optimized for Gemini 2.0 Flash
            candidate_count=1,
            stop_sequences=None,
        )

        # Updated safety settings for Gemini 2.0
        self.safety_settings = [
            {
                "category": "HARM_CATEGORY_HARASSMENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_HATE_SPEECH",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_SEXUALLY_EXPLICIT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            },
            {
                "category": "HARM_CATEGORY_DANGEROUS_CONTENT",
                "threshold": "BLOCK_MEDIUM_AND_ABOVE"
            }
        ]

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def generate_text_response(
            self,
            prompt: str,
            context: Optional[str] = None,
            system_instruction: Optional[str] = None
    ) -> str:
        """
        Generate text response using Gemini 2.0 Flash.
        
        Args:
            prompt: User prompt
            context: Additional context
            system_instruction: System instruction for the model
            
        Returns:
            Generated response text
        """
        try:
            # Create model with system instruction if provided
            if system_instruction:
                model_with_system = genai.GenerativeModel(
                    settings.text_model,
                    system_instruction=system_instruction
                )
            else:
                model_with_system = self.model

            # Prepare the full prompt
            full_prompt = []

            if context:
                full_prompt.append(f"Context: {context}")

            full_prompt.append(f"User: {prompt}")

            final_prompt = "\n\n".join(full_prompt)

            response = model_with_system.generate_content(
                final_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "I'm sorry, I couldn't generate a response. Please try rephrasing your question."

        except Exception as e:
            logger.error(f"Text generation error: {str(e)}")
            return f"Error generating response: {str(e)}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def analyze_image(
            self,
            image: Image.Image,
            prompt: str,
            system_instruction: Optional[str] = None
    ) -> str:
        """
        Analyze image using Gemini 2.0 Flash (unified model for vision).
        
        Args:
            image: PIL Image object
            prompt: Analysis prompt
            system_instruction: System instruction for the model
            
        Returns:
            Analysis result
        """
        try:
            # Create model with system instruction if provided
            if system_instruction:
                model_with_system = genai.GenerativeModel(
                    settings.vision_model,  # Same as text_model for Gemini 2.0 Flash
                    system_instruction=system_instruction
                )
            else:
                model_with_system = self.model

            # Create content with image and text
            content = [prompt, image]

            response = model_with_system.generate_content(
                content,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "I'm sorry, I couldn't analyze the image. Please try again."

        except Exception as e:
            logger.error(f"Image analysis error: {str(e)}")
            return f"Error analyzing image: {str(e)}"

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    def process_document(
            self,
            content: str,
            query: str,
            file_type: str,
            system_instruction: Optional[str] = None
    ) -> str:
        """
        Process document content using Gemini 2.0 Flash.
        
        Args:
            content: Document content
            query: User query about the document
            file_type: Type of file being processed
            system_instruction: System instruction for the model
            
        Returns:
            Analysis result
        """
        try:
            # Create model with system instruction if provided
            if system_instruction:
                model_with_system = genai.GenerativeModel(
                    settings.text_model,
                    system_instruction=system_instruction
                )
            else:
                model_with_system = self.model

            # Prepare the prompt with better structure for Gemini 2.0 Flash
            prompt_parts = [
                f"Document Type: {file_type.upper()}",
                f"Document Content:\n```\n{content}\n```",
                f"User Query: {query}",
                "\nPlease analyze the document and provide a comprehensive response to the user's query."
            ]

            final_prompt = "\n\n".join(prompt_parts)

            response = model_with_system.generate_content(
                final_prompt,
                generation_config=self.generation_config,
                safety_settings=self.safety_settings
            )

            if response.candidates and response.candidates[0].content.parts:
                return response.candidates[0].content.parts[0].text
            else:
                return "I'm sorry, I couldn't process the document. Please try again."

        except Exception as e:
            logger.error(f"Document processing error: {str(e)}")
            return f"Error processing document: {str(e)}"

    def get_model_info(self) -> Dict[str, Any]:
        """Get information about available models."""
        try:
            models = []
            for model in genai.list_models():
                if 'generateContent' in model.supported_generation_methods:
                    models.append({
                        'name': model.name,
                        'display_name': model.display_name,
                        'description': model.description,
                        'version': getattr(model, 'version', 'Unknown'),
                        'input_token_limit': getattr(model, 'input_token_limit', 'Unknown'),
                        'output_token_limit': getattr(model, 'output_token_limit', 'Unknown')
                    })

            # Add current configuration info
            current_config = {
                'current_text_model': settings.text_model,
                'current_vision_model': settings.vision_model,
                'max_tokens': settings.max_tokens,
                'temperature': settings.temperature,
                'model_version': '2.0-flash'
            }

            return {
                'available_models': models,
                'current_configuration': current_config
            }
        except Exception as e:
            logger.error(f"Error getting model info: {str(e)}")
            return {'models': [], 'error': str(e)}

    def test_connection(self) -> Dict[str, Any]:
        """Test the connection to Gemini API."""
        try:
            test_response = self.generate_text_response("Hello, this is a connection test.")
            return {
                'status': 'success',
                'model': settings.text_model,
                'response_preview': test_response[:100] + "..." if len(test_response) > 100 else test_response
            }
        except Exception as e:
            return {
                'status': 'error',
                'error': str(e)
            }

# Global client instance
gemini_client = GeminiClient()
