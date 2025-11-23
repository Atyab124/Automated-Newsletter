"""
Configuration settings for the Newsletter Generator
"""
import os

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen2.5")  # Default model, can be changed

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

