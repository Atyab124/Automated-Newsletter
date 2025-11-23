"""
Newsletter Generator using Ollama
"""
import requests
import json
from typing import Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import OLLAMA_BASE_URL, OLLAMA_MODEL, NEWSLETTER_TITLE_TEMPLATE, NEWSLETTER_DATE_FORMAT
from datetime import datetime


class NewsletterGenerator:
    """Generates newsletters from fact sheets using Ollama"""
    
    def __init__(self, model: str = OLLAMA_MODEL, base_url: str = OLLAMA_BASE_URL):
        self.model = model
        self.base_url = base_url
    
    def generate(self, fact_sheet_markdown: str, style_profile: Dict, topic: str) -> str:
        """
        Generate newsletter from fact sheet
        
        Args:
            fact_sheet_markdown: Markdown fact sheet
            style_profile: Writing style profile from StyleExtractor
            topic: Topic name
        
        Returns:
            Generated newsletter in Markdown format
        """
        # Format style profile for prompt
        style_text = f"""
Tone: {style_profile.get('tone', 'professional')}
Structure: {style_profile.get('structure', 'clear paragraphs')}
Voice: {style_profile.get('voice', 'third person')}
Common Phrases: {', '.join(style_profile.get('common_phrases', []))}
"""
        
        # Create prompt
        prompt = f"""Write a newsletter using ONLY information from the FACT SHEET below.

CRITICAL RULES:
1. Use ONLY information from the fact sheet - NO hallucinations or made-up facts
2. Every claim must be traceable to a source in the fact sheet
3. If information is not in the fact sheet, do not include it
4. Always cite sources using the URLs provided in the fact sheet

Writing Style to Follow:
{style_text}

FACT SHEET:
{fact_sheet_markdown}

Generate a well-structured newsletter that:
- Has a clear title related to "{topic}"
- Organizes information logically
- Includes proper source citations
- Follows the specified writing style
- Is engaging and informative
- Uses ONLY facts from the fact sheet

Format the newsletter in Markdown with appropriate headings, paragraphs, and links."""
        
        try:
            response = self._call_ollama(prompt)
            
            # Add header with date
            date_str = datetime.now().strftime(NEWSLETTER_DATE_FORMAT)
            title = NEWSLETTER_TITLE_TEMPLATE.format(topic=topic)
            
            newsletter = f"# {title}\n\n*Generated on {date_str}*\n\n---\n\n{response}"
            
            return newsletter
        
        except Exception as e:
            print(f"Error generating newsletter: {e}")
            return f"# Newsletter Generation Error\n\nError: {str(e)}"
    
    def _call_ollama(self, prompt: str) -> str:
        """Call Ollama API"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9
            }
        }
        
        response = requests.post(url, json=payload, timeout=300)  # Longer timeout for generation
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")

