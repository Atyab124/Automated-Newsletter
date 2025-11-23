"""
Scrapers module for Newsletter Generator
"""
from .news_scraper import NewsScraper
from .linkedin_scraper import LinkedInScraper
from .research_scraper import ResearchScraper
from .web_scraper import WebScraper

__all__ = ['NewsScraper', 'LinkedInScraper', 'ResearchScraper', 'WebScraper']

