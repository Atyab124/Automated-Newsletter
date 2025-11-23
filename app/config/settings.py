"""
Configuration settings for the Newsletter Generator
"""
import os

# Ollama Configuration
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # Default model, can be changed

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

