"""
Configuration settings for the Newsletter Generator
"""
import os

# LLM Provider Configuration
# Options: "ollama" or "openai"
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "ollama")  # Default to Ollama

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")  # Default model, can be changed

# OpenAI Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")  # Default model, can be changed to gpt-4, gpt-3.5-turbo, etc.
OPENAI_BASE_URL = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")  # For custom endpoints

# Database Configuration
DATABASE_PATH = os.getenv("DATABASE_PATH", "newsletter.db")

# Scraping Configuration
SCRAPING_TIMEOUT = 30  # seconds
MAX_RESULTS_PER_SOURCE = 10  # Maximum results to fetch per source

# Newsletter Configuration
NEWSLETTER_TITLE_TEMPLATE = "Weekly Newsletter: {topic}"
NEWSLETTER_DATE_FORMAT = "%B %d, %Y"

# Frequency Options
FREQUENCY_OPTIONS = {
    "daily": 1,  # days
    "weekly": 7,
    "biweekly": 14,
    "monthly": 30
}

# Research API Configuration
ARXIV_MAX_RESULTS = 10
SEMANTIC_SCHOLAR_MAX_RESULTS = 10

# News API Configuration
# Get free API key from https://newsapi.org/
NEWSAPI_KEY = os.getenv("NEWSAPI_KEY", "")

# LinkedIn API Configuration
# Requires OAuth setup - see https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication
LINKEDIN_ACCESS_TOKEN = os.getenv("LINKEDIN_ACCESS_TOKEN", "")
LINKEDIN_CLIENT_ID = os.getenv("LINKEDIN_CLIENT_ID", "")
LINKEDIN_CLIENT_SECRET = os.getenv("LINKEDIN_CLIENT_SECRET", "")

