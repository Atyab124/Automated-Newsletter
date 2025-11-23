"""
Web scraper using Playwright MCP for general web articles
"""
import time
from typing import List, Dict
from .base_scraper import BaseScraper
from .snapshot_parser import extract_headlines_from_snapshot


class WebScraper(BaseScraper):
    """Scrapes web articles using Playwright MCP"""
    
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape web articles for a topic
        
        Note: This uses Playwright MCP tools which are called externally.
        """
        results = []
        return results
    
    def scrape_with_mcp(self, mcp_client) -> List[Dict]:
        """
        Scrape using Playwright MCP client
        
        Searches for articles on various public sites related to the topic.
        """
        results = []
        topic = getattr(self, '_current_topic', '')
        
        if not topic:
            return results
        
        # List of sites to search (public, non-news sites)
        search_sites = [
            ("Medium", f"https://www.google.com/search?q={topic.replace(' ', '+')}+site:medium.com"),
            ("Dev.to", f"https://www.google.com/search?q={topic.replace(' ', '+')}+site:dev.to"),
        ]
        
        for site_name, search_url in search_sites:
            try:
                # Navigate to search
                if hasattr(mcp_client, 'navigate'):
                    mcp_client.navigate(url=search_url)
                elif callable(mcp_client):
                    mcp_client('navigate', url=search_url)
                else:
                    continue
                
                time.sleep(2)
                
                # Get snapshot
                snapshot = None
                if hasattr(mcp_client, 'snapshot'):
                    snapshot = mcp_client.snapshot()
                elif callable(mcp_client):
                    snapshot = mcp_client('snapshot')
                
                if snapshot:
                    # Extract article titles and links
                    articles = extract_headlines_from_snapshot(snapshot, max_results=5)
                    
                    for item in articles:
                        results.append(self.format_result(
                            source=site_name,
                            headline=item['text'],
                            url=item['url']
                        ))
                
                # Limit total results
                if len(results) >= self.max_results:
                    break
                    
            except Exception as e:
                print(f"Error scraping {site_name}: {e}")
                continue
        
        return results[:self.max_results]

