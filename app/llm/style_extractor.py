"""
Writing Style Extractor using Ollama or OpenAI
"""
import json
from typing import List, Dict, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from llm.llm_provider import LLMProvider


class StyleExtractor:
    """Extracts writing style from user samples using Ollama or OpenAI"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize style extractor
        
        Args:
            provider: "ollama" or "openai" (defaults to config)
            model: Model name (defaults to provider's default)
        """
        self.llm = LLMProvider(provider=provider, model=model)
    
    def extract_style(self, writing_samples: List[str]) -> Dict:
        """
        Extract writing style from user samples
        
        Args:
            writing_samples: List of text samples from the user
        
        Returns:
            Dict with style profile: tone, structure, voice, common_phrases
        """
        if not writing_samples:
            return self._default_style()
        
        # Combine all samples
        combined_text = "\n\n---\n\n".join(writing_samples)
        
        # Create prompt
        system_prompt = "You are an expert at analyzing writing styles. Extract the key characteristics and return ONLY valid JSON."
        
        user_prompt = f"""Analyze the following writing samples and extract the writing style characteristics.

Writing Samples:
{combined_text}

Please provide a JSON object with the following structure:
{{
    "tone": "description of the tone (e.g., professional, casual, academic, friendly)",
    "structure": "description of the structure (e.g., formal paragraphs, bullet points, narrative style)",
    "voice": "description of the voice (e.g., first person, third person, authoritative, conversational)",
    "common_phrases": ["list", "of", "common", "phrases", "or", "expressions", "used"]
}}

Respond ONLY with valid JSON, no additional text."""
        
        try:
            response = self.llm.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.3  # Lower temperature for more consistent style extraction
            )
            
            # Try to parse JSON from response
            json_str = self._extract_json(response)
            style_profile = json.loads(json_str)
            
            return style_profile
        
        except Exception as e:
            print(f"Error extracting style: {e}")
            import traceback
            traceback.print_exc()
            return self._default_style()
    
    def _extract_json(self, text: str) -> str:
        """Extract JSON from text response"""
        import re
        
        # Look for JSON object
        json_match = re.search(r'\{[^{}]*(?:\{[^{}]*\}[^{}]*)*\}', text, re.DOTALL)
        if json_match:
            return json_match.group(0)
        
        # If no match, try to parse the whole text
        return text.strip()
    
    def _default_style(self) -> Dict:
        """Return default style profile"""
        return {
            "tone": "professional",
            "structure": "clear paragraphs with headings",
            "voice": "third person, informative",
            "common_phrases": []
        }
