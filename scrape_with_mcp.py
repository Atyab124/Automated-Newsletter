"""
Script to scrape content using Playwright MCP tools directly

This script demonstrates how to use Playwright MCP tools to scrape content.
Run this in Cursor where MCP tools are available.

Usage:
    python scrape_with_mcp.py "your topic here"
"""
import sys
from pathlib import Path

# Add app to path
sys.path.insert(0, str(Path(__file__).parent))

from app.scrapers.direct_mcp_scraper import DirectMCPScraper
from app.scrapers.research_scraper import ResearchScraper


def main():
    """Main function to scrape with MCP"""
    if len(sys.argv) < 2:
        print("Usage: python scrape_with_mcp.py 'topic'")
        sys.exit(1)
    
    topic = sys.argv[1]
    print(f"Scraping content for topic: {topic}")
    
    # Note: In Cursor, you would pass the actual MCP tool functions here
    # For example:
    # scraper = DirectMCPScraper(
    #     mcp_navigate=lambda **kwargs: mcp_Playwright_browser_navigate(**kwargs),
    #     mcp_snapshot=lambda: mcp_Playwright_browser_snapshot()
    # )
    
    # For now, this is a template showing how it would work
    print("\nTo use MCP tools, you need to:")
    print("1. Import the MCP tool functions")
    print("2. Pass them to DirectMCPScraper")
    print("3. Call scrape_all()")
    
    # Research scraper works without MCP
    print("\nScraping research papers (works without MCP)...")
    research_scraper = ResearchScraper()
    research_papers = research_scraper.scrape(topic)
    
    print(f"\nFound {len(research_papers)} research papers:")
    for paper in research_papers[:5]:  # Show first 5
        print(f"  - {paper['headline']}")
        print(f"    Source: {paper['url']}")


if __name__ == "__main__":
    main()

