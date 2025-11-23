"""
LLM Provider abstraction - supports both Ollama and OpenAI
"""
import requests
import os
from typing import Optional, Dict, Any
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import (
    LLM_PROVIDER, 
    OLLAMA_BASE_URL, 
    OLLAMA_MODEL,
    OPENAI_API_KEY,
    OPENAI_MODEL,
    OPENAI_BASE_URL
)


class LLMProvider:
    """Unified interface for LLM providers (Ollama and OpenAI)"""
    
    def __init__(self, provider: Optional[str] = None, model: Optional[str] = None):
        """
        Initialize LLM provider
        
        Args:
            provider: "ollama" or "openai" (defaults to LLM_PROVIDER from config)
            model: Model name (defaults to provider's default model)
        """
        self.provider = provider or LLM_PROVIDER.lower()
        
        if self.provider == "openai":
            self.model = model or OPENAI_MODEL
            self.api_key = OPENAI_API_KEY
            self.base_url = OPENAI_BASE_URL
            
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. Set OPENAI_API_KEY environment variable. "
                    "Get your key from https://platform.openai.com/api-keys"
                )
        else:  # Default to Ollama
            self.provider = "ollama"
            self.model = model or OLLAMA_MODEL
            self.base_url = OLLAMA_BASE_URL
    
    def generate(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """
        Generate text using the configured provider
        
        Args:
            prompt: User prompt
            system_prompt: Optional system prompt
            **kwargs: Additional provider-specific parameters
        
        Returns:
            Generated text
        """
        if self.provider == "openai":
            return self._call_openai(prompt, system_prompt, **kwargs)
        else:
            return self._call_ollama(prompt, **kwargs)
    
    def _call_ollama(self, prompt: str, **kwargs) -> str:
        """Call Ollama API"""
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": kwargs.get("temperature", 0.7),
                "top_p": kwargs.get("top_p", 0.9)
            }
        }
        
        response = requests.post(url, json=payload, timeout=kwargs.get("timeout", 300))
        response.raise_for_status()
        
        result = response.json()
        return result.get("response", "")
    
    def _call_openai(self, prompt: str, system_prompt: Optional[str] = None, **kwargs) -> str:
        """Call OpenAI API"""
        try:
            import openai
        except ImportError:
            raise ImportError(
                "OpenAI package not installed. Install with: pip install openai"
            )
        
        # Initialize OpenAI client
        client = openai.OpenAI(
            api_key=self.api_key,
            base_url=self.base_url if self.base_url != "https://api.openai.com/v1" else None
        )
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        response = client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=kwargs.get("temperature", 0.7),
            max_tokens=kwargs.get("max_tokens", 4000),
            timeout=kwargs.get("timeout", 60)
        )
        
        return response.choices[0].message.content

