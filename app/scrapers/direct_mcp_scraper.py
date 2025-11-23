"""
Direct MCP Scraper - Uses Playwright MCP tools directly when available

This module can be used to scrape content using Playwright MCP tools.
It's designed to work when MCP tools are available (e.g., in Cursor).
"""
from typing import List, Dict, Optional, Callable
from .news_scraper import NewsScraper
from .linkedin_scraper import LinkedInScraper
from .web_scraper import WebScraper


class DirectMCPScraper:
    """
    Scraper that uses Playwright MCP tools directly
    
    This class wraps the individual scrapers and provides MCP tool integration.
    """
    
    def __init__(self, mcp_navigate: Optional[Callable] = None, 
                 mcp_snapshot: Optional[Callable] = None,
                 mcp_wait: Optional[Callable] = None):
        """
        Initialize with MCP tool functions
        
        Args:
            mcp_navigate: Function to navigate (should accept url parameter)
            mcp_snapshot: Function to get snapshot (should return snapshot dict)
            mcp_wait: Optional function to wait (should accept time parameter)
        """
        self.mcp_navigate = mcp_navigate
        self.mcp_snapshot = mcp_snapshot
        self.mcp_wait = mcp_wait
        
        # Create scrapers
        self.news_scraper = NewsScraper()
        self.linkedin_scraper = LinkedInScraper()
        self.web_scraper = WebScraper()
    
    def _create_mcp_client(self):
        """Create a mock MCP client that uses the provided functions"""
        class MCPClient:
            def __init__(self, navigate_fn, snapshot_fn, wait_fn):
                self.navigate_fn = navigate_fn
                self.snapshot_fn = snapshot_fn
                self.wait_fn = wait_fn
            
            def navigate(self, url: str):
                if self.navigate_fn:
                    self.navigate_fn(url=url)
            
            def snapshot(self):
                if self.snapshot_fn:
                    return self.snapshot_fn()
                return None
        
        return MCPClient(self.mcp_navigate, self.mcp_snapshot, self.mcp_wait)
    
    def scrape_all(self, topic: str) -> Dict[str, List[Dict]]:
        """
        Scrape from all sources for a topic
        
        Returns:
            Dict with keys: news, linkedin, web, each containing list of results
        """
        results = {
            'news': [],
            'linkedin': [],
            'web': []
        }
        
        if not (self.mcp_navigate and self.mcp_snapshot):
            print("MCP tools not available - skipping Playwright-based scraping")
            return results
        
        mcp_client = self._create_mcp_client()
        
        # Scrape news
        try:
            self.news_scraper._current_topic = topic
            results['news'] = self.news_scraper.scrape_with_mcp(mcp_client)
        except Exception as e:
            print(f"Error scraping news: {e}")
        
        # Scrape LinkedIn
        try:
            self.linkedin_scraper._current_topic = topic
            results['linkedin'] = self.linkedin_scraper.scrape_with_mcp(mcp_client)
        except Exception as e:
            print(f"Error scraping LinkedIn: {e}")
        
        # Scrape web
        try:
            self.web_scraper._current_topic = topic
            results['web'] = self.web_scraper.scrape_with_mcp(mcp_client)
        except Exception as e:
            print(f"Error scraping web: {e}")
        
        return results

