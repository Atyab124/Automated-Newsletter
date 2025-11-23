"""
Fact Sheet Builder - Creates structured fact sheets from scraped content
"""
from typing import List, Dict
from datetime import datetime
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))

from scrapers.news_scraper import NewsScraper
from scrapers.linkedin_scraper import LinkedInScraper
from scrapers.research_scraper import ResearchScraper
from scrapers.web_scraper import WebScraper


class FactSheetBuilder:
    """Builds fact sheets from scraped content"""
    
    def __init__(self):
        self.news_scraper = NewsScraper()
        self.linkedin_scraper = LinkedInScraper()
        self.research_scraper = ResearchScraper()
        self.web_scraper = WebScraper()
    
    def build_fact_sheet(self, topic: str, use_mcp_client=None) -> Dict:
        """
        Build a fact sheet for a topic
        
        Args:
            topic: The topic to build a fact sheet for
            use_mcp_client: Deprecated - kept for backward compatibility
        
        Returns:
            Dict with 'markdown' and 'json_data' keys
        """
        # Scrape from all sources using APIs
        print(f"Scraping research papers for: {topic}")
        research_papers = self.research_scraper.scrape(topic)
        
        print(f"Scraping news for: {topic}")
        news_items = self.news_scraper.scrape(topic)
        
        print(f"Scraping LinkedIn for: {topic}")
        linkedin_posts = self.linkedin_scraper.scrape(topic)
        
        print(f"Scraping web articles for: {topic}")
        web_articles = self.web_scraper.scrape(topic)
        
        # Build JSON structure
        json_data = {
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "research_papers": research_papers,
            "news_headlines": news_items,
            "linkedin_posts": linkedin_posts,
            "web_articles": web_articles
        }
        
        # Build Markdown
        markdown = self._build_markdown(topic, json_data)
        
        return {
            "markdown": markdown,
            "json_data": json_data
        }
    
    def _build_markdown(self, topic: str, data: Dict) -> str:
        """Build Markdown fact sheet"""
        lines = [f"# Fact Sheet: {topic}\n"]
        lines.append(f"*Generated on {datetime.now().strftime('%B %d, %Y at %H:%M')}*\n")
        
        # Research Papers
        if data.get("research_papers"):
            lines.append("\n## Research Papers\n")
            for idx, paper in enumerate(data["research_papers"], 1):
                lines.append(f"{idx}. **{paper['headline']}**")
                if paper.get('abstract'):
                    # Truncate abstract if too long
                    abstract = paper['abstract']
                    if len(abstract) > 500:
                        abstract = abstract[:500] + "..."
                    lines.append(f"   {abstract}")
                lines.append(f"   Source: [{paper['source']}]({paper['url']})\n")
        else:
            lines.append("\n## Research Papers\n*No research papers found.*\n")
        
        # News Headlines
        if data.get("news_headlines"):
            lines.append("\n## News Headlines\n")
            for item in data["news_headlines"]:
                lines.append(f"- {item['headline']} ([{item['source']}]({item['url']}))")
            lines.append("")
        else:
            lines.append("\n## News Headlines\n*No news headlines found.*\n")
        
        # LinkedIn Posts
        if data.get("linkedin_posts"):
            lines.append("\n## LinkedIn Posts\n")
            for item in data["linkedin_posts"]:
                lines.append(f"- {item['headline']} ([View Post]({item['url']}))")
            lines.append("")
        else:
            lines.append("\n## LinkedIn Posts\n*No LinkedIn posts found.*\n")
        
        # Web Articles
        if data.get("web_articles"):
            lines.append("\n## Web Articles\n")
            for item in data["web_articles"]:
                lines.append(f"- {item['headline']} ([{item['source']}]({item['url']}))")
            lines.append("")
        else:
            lines.append("\n## Web Articles\n*No web articles found.*\n")
        
        return "\n".join(lines)

