"""
Web scraper using RSS feeds and open APIs
"""
from typing import List, Dict
from .base_scraper import BaseScraper
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from config.settings import MAX_RESULTS_PER_SOURCE


class WebScraper(BaseScraper):
    """Scrapes web articles using RSS feeds from popular sites"""
    
    def __init__(self):
        super().__init__()
        # Popular tech/content sites with RSS feeds
        self.rss_feeds = {
            "Medium": "https://medium.com/feed/tag/{topic}",
            "Dev.to": "https://dev.to/feed/tag/{topic}",
            "Hacker News": "https://hnrss.org/newest?q={topic}",
        }
    
    def scrape(self, topic: str) -> List[Dict]:
        """
        Scrape web articles for a topic using RSS feeds
        """
        results = []
        
        try:
            import feedparser
        except ImportError:
            print("feedparser not installed. Install with: pip install feedparser")
            return results
        
        # Try each RSS feed
        for site_name, feed_template in self.rss_feeds.items():
            try:
                feed_url = feed_template.format(topic=topic.lower().replace(' ', '-'))
                feed_results = self._scrape_rss_feed(feed_url, site_name, topic)
                results.extend(feed_results)
                
                if len(results) >= self.max_results:
                    break
            
            except Exception as e:
                print(f"Error scraping {site_name}: {e}")
                continue
        
        return results[:self.max_results]
    
    def _scrape_rss_feed(self, feed_url: str, source_name: str, topic: str) -> List[Dict]:
        """Scrape a single RSS feed"""
        results = []
        
        try:
            import feedparser
            
            feed = feedparser.parse(feed_url)
            
            # Filter entries that match the topic
            for entry in feed.entries:
                title = entry.get("title", "")
                link = entry.get("link", "")
                summary = entry.get("summary", "")
                
                # Basic topic matching (check if topic appears in title or summary)
                title_lower = title.lower()
                summary_lower = summary.lower()
                topic_lower = topic.lower()
                
                if topic_lower in title_lower or topic_lower in summary_lower:
                    if title and link:
                        results.append(self.format_result(
                            source=source_name,
                            headline=title,
                            url=link,
                            abstract=summary[:200] if summary else ""  # Truncate summary
                        ))
                
                if len(results) >= 5:  # Limit per feed
                    break
        
        except Exception as e:
            print(f"Error parsing RSS feed {feed_url}: {e}")
        
        return results
    
    def add_custom_rss_feed(self, name: str, url_template: str):
        """Add a custom RSS feed"""
        self.rss_feeds[name] = url_template
