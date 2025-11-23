"""
News scraper using Playwright MCP
"""
import time
from typing import List, Dict, Any, Optional
from .base_scraper import BaseScraper
from .snapshot_parser import extract_headlines_from_snapshot


class NewsScraper(BaseScraper):
    """Scrapes news headlines using Playwright MCP"""
    
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape news headlines for a topic using Google News search
        
        Note: This uses Playwright MCP tools which are called externally.
        The actual MCP calls should be made by the caller or through a wrapper.
        """
        results = []
        return results
    
    def scrape_with_mcp(self, mcp_client) -> List[Dict]:
        """
        Scrape using Playwright MCP client
        
        This method should be called with an MCP client that has Playwright tools.
        In Cursor, mcp_client should have navigate() and snapshot() methods.
        """
        results = []
        topic = getattr(self, '_current_topic', '')
        
        if not topic:
            return results
        
        try:
            # Navigate to Google News
            search_url = f"https://news.google.com/search?q={topic.replace(' ', '+')}"
            
            # Use MCP navigate if available
            if hasattr(mcp_client, 'navigate'):
                mcp_client.navigate(url=search_url)
            elif callable(mcp_client):
                # If mcp_client is a function that can call MCP tools
                mcp_client('navigate', url=search_url)
            else:
                print("MCP client does not support navigation")
                return results
            
            # Wait for page to load
            time.sleep(3)
            
            # Get page snapshot
            snapshot = None
            if hasattr(mcp_client, 'snapshot'):
                snapshot = mcp_client.snapshot()
            elif callable(mcp_client):
                snapshot = mcp_client('snapshot')
            
            if snapshot:
                # Extract headlines from snapshot
                headlines = extract_headlines_from_snapshot(snapshot, max_results=self.max_results)
                
                # Format results
                for item in headlines:
                    results.append(self.format_result(
                        source="Google News",
                        headline=item['text'],
                        url=item['url']
                    ))
            
        except Exception as e:
            print(f"Error scraping news: {e}")
            import traceback
            traceback.print_exc()
        
        return results

