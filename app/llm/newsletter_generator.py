"""
Newsletter Generator using Ollama or OpenAI
"""
from typing import Dict, Optional
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from llm.llm_provider import LLMProvider
from config.settings import NEWSLETTER_TITLE_TEMPLATE, NEWSLETTER_DATE_FORMAT
from datetime import datetime


class NewsletterGenerator:
    """Generates newsletters from fact sheets using Ollama or OpenAI"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize newsletter generator
        
        Args:
            provider: "ollama" or "openai" (defaults to config)
            model: Model name (defaults to provider's default)
        """
        self.llm = LLMProvider(provider=provider, model=model)
    
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
        
        # Create system prompt
        system_prompt = """You are an expert newsletter writer. You create engaging, informative newsletters that strictly adhere to the provided fact sheet. You never make up facts or information that isn't in the fact sheet."""
        
        # Create user prompt
        user_prompt = f"""Write a newsletter using ONLY information from the FACT SHEET below.

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
            response = self.llm.generate(
                prompt=user_prompt,
                system_prompt=system_prompt,
                temperature=0.7,
                max_tokens=4000
            )
            
            # Add header with date
            date_str = datetime.now().strftime(NEWSLETTER_DATE_FORMAT)
            title = NEWSLETTER_TITLE_TEMPLATE.format(topic=topic)
            
            newsletter = f"# {title}\n\n*Generated on {date_str}*\n\n---\n\n{response}"
            
            return newsletter
        
        except Exception as e:
            print(f"Error generating newsletter: {e}")
            import traceback
            traceback.print_exc()
            return f"# Newsletter Generation Error\n\nError: {str(e)}"
