# Using Playwright MCP with Newsletter Generator

## Current Status

✅ **Research Papers**: Work immediately (arXiv, Semantic Scholar APIs)  
⚠️ **News/LinkedIn/Web**: Require Playwright MCP integration

## Why Only Research Papers Work

The research paper scrapers use public APIs that don't require MCP:
- **arXiv**: Public API endpoint
- **Semantic Scholar**: Public API endpoint

The other scrapers (news, LinkedIn, web) need Playwright MCP to:
- Navigate to websites
- Extract content from pages
- Handle JavaScript-rendered content

## Options for MCP Integration

### Option 1: Use Research Papers Only (Current)

The system works great with just research papers! You can:
1. Generate fact sheets (will have research papers)
2. Generate newsletters from those fact sheets
3. All features work except news/LinkedIn/web scraping

### Option 2: Manual MCP Integration

If you want to use Playwright MCP tools, you need to:

1. **Set up MCP client** in your code
2. **Pass MCP functions** to the fact sheet builder
3. **Update the Streamlit app** to use MCP

Example:

```python
from app.pipeline.fact_sheet_builder import FactSheetBuilder

# Create MCP client (you need to implement this based on your MCP setup)
def mcp_navigate(url):
    # Call your MCP navigate function
    pass

def mcp_snapshot():
    # Call your MCP snapshot function
    pass

# Use in fact sheet builder
builder = FactSheetBuilder()
fact_sheet = builder.build_fact_sheet(
    "your topic",
    use_mcp_client=your_mcp_client
)
```

### Option 3: Use Alternative Scrapers

You could replace the Playwright-based scrapers with:
- **News**: Use news APIs (NewsAPI, etc.)
- **LinkedIn**: Use LinkedIn API (requires authentication)
- **Web**: Use RSS feeds or other APIs

## Testing Your Setup

To test if MCP is working:

```python
from app.scrapers.news_scraper import NewsScraper

scraper = NewsScraper()
scraper._current_topic = "test topic"

# If you have MCP client:
results = scraper.scrape_with_mcp(your_mcp_client)
print(f"Found {len(results)} news items")
```

## Current Workaround

For now, the system gracefully handles missing MCP:
- Research papers are scraped successfully
- News/LinkedIn/Web return empty lists
- Fact sheets are generated with available data
- Newsletters are generated from available fact sheet data

This means you can use the system right now with research papers, and add MCP integration later when ready!

## Need Help?

- Check `MCP_INTEGRATION.md` for detailed integration guide
- The scrapers are in `app/scrapers/` and are designed to work with MCP
- All scrapers have `scrape_with_mcp()` methods that accept an MCP client

