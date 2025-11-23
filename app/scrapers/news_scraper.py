"""
News scraper using NewsAPI and other open APIs
"""
import requests
import os
from typing import List, Dict
from .base_scraper import BaseScraper
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import MAX_RESULTS_PER_SOURCE


class NewsScraper(BaseScraper):
    """Scrapes news headlines using NewsAPI and other open APIs"""
    
    def __init__(self):
        super().__init__()
        # Get API key from environment or config
        self.newsapi_key = os.getenv("NEWSAPI_KEY", "")
        # Alternative: use free RSS feeds if API key not available
        self.use_rss_fallback = not self.newsapi_key
    
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape news headlines for a topic
        
        Tries NewsAPI first, falls back to RSS feeds if no API key
        """
        results = []
        
        # Try NewsAPI if key is available
        if self.newsapi_key:
            results = self._scrape_newsapi(topic)
        
        # If NewsAPI didn't work or no key, try RSS feeds
        if not results and self.use_rss_fallback:
            results = self._scrape_rss_feeds(topic)
        
        return results[:self.max_results]
    
    def _scrape_newsapi(self, topic: str) -> List[Dict]:
        """Scrape using NewsAPI"""
        results = []
        
        try:
            # NewsAPI endpoint
            url = "https://newsapi.org/v2/everything"
            params = {
                "q": topic,
                "language": "en",
                "sortBy": "relevancy",
                "pageSize": self.max_results,
                "apiKey": self.newsapi_key
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get("status") == "ok" and "articles" in data:
                for article in data["articles"]:
                    title = article.get("title", "")
                    url = article.get("url", "")
                    source = article.get("source", {}).get("name", "Unknown")
                    description = article.get("description", "")
                    
                    if title and url:
                        results.append(self.format_result(
                            source=source,
                            headline=title,
                            url=url,
                            abstract=description
                        ))
        
        except requests.exceptions.RequestException as e:
            print(f"NewsAPI error: {e}")
        except Exception as e:
            print(f"Error scraping NewsAPI: {e}")
        
        return results
    
    def _scrape_rss_feeds(self, topic: str) -> List[Dict]:
        """Scrape using RSS feeds from news sites"""
        results = []
        
        try:
            import feedparser
            
            # RSS feeds that support search or topic-based feeds
            # Note: Many RSS feeds don't support search, so we'll use topic-specific feeds
            rss_feeds = [
                # Google News RSS (topic-based)
                f"https://news.google.com/rss/search?q={topic.replace(' ', '+')}&hl=en-US&gl=US&ceid=US:en",
            ]
            
            for feed_url in rss_feeds:
                try:
                    feed = feedparser.parse(feed_url)
                    
                    for entry in feed.entries[:self.max_results]:
                        title = entry.get("title", "")
                        link = entry.get("link", "")
                        summary = entry.get("summary", "")
                        source = entry.get("source", {}).get("title", "RSS Feed") if hasattr(entry, "source") else "RSS Feed"
                        
                        if title and link:
                            results.append(self.format_result(
                                source=source,
                                headline=title,
                                url=link,
                                abstract=summary
                            ))
                    
                    if len(results) >= self.max_results:
                        break
                
                except Exception as e:
                    print(f"Error parsing RSS feed {feed_url}: {e}")
                    continue
        
        except ImportError:
            print("feedparser not installed. Install with: pip install feedparser")
        except Exception as e:
            print(f"Error scraping RSS feeds: {e}")
        
        return results
