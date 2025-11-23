"""
Base scraper class with common functionality
"""
from abc import ABC, abstractmethod
from typing import List, Dict
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import MAX_RESULTS_PER_SOURCE


class BaseScraper(ABC):
    """Base class for all scrapers"""
    
    def __init__(self):
        self.max_results = MAX_RESULTS_PER_SOURCE
    
    @abstractmethod
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape content for a given topic
        
        Returns:
            List of dicts with keys: source, headline, abstract (optional), url
        """
        pass
    
    def format_result(self, source: str, headline: str, url: str, abstract: str = "") -> Dict:
        """Format a result dictionary"""
        return {
            "source": source,
            "headline": headline,
            "abstract": abstract,
            "url": url
        }

