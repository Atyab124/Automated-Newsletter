# Changelog

## Latest Update: Replaced Playwright MCP with Open Source APIs

### What Changed

All scrapers now use open-source APIs instead of Playwright MCP:

1. **News Scraper** (`app/scrapers/news_scraper.py`)
   - ✅ Now uses NewsAPI (optional API key)
   - ✅ Falls back to RSS feeds if no API key
   - ✅ Works immediately without setup

2. **LinkedIn Scraper** (`app/scrapers/linkedin_scraper.py`)
   - ✅ Now uses LinkedIn API (requires OAuth setup)
   - ✅ Returns empty results if not configured (system works fine without it)

3. **Web Scraper** (`app/scrapers/web_scraper.py`)
   - ✅ Now uses RSS feeds from Medium, Dev.to, Hacker News
   - ✅ Works immediately without any setup

4. **Research Scraper** (unchanged)
   - ✅ Still uses arXiv and Semantic Scholar APIs
   - ✅ Works immediately without setup

### Benefits

- ✅ **No MCP dependency**: Works anywhere Python runs
- ✅ **Open source only**: All APIs are open source
- ✅ **Works immediately**: Most scrapers work without API keys
- ✅ **Better reliability**: API-based scraping is more reliable than web scraping

### Migration Notes

- The `use_mcp_client` parameter in `FactSheetBuilder.build_fact_sheet()` is now deprecated but still accepted for backward compatibility
- All scrapers now have a `scrape()` method that works without MCP
- Old MCP-related methods (`scrape_with_mcp()`) are kept for backward compatibility but not used

### New Dependencies

- `feedparser>=6.0.10` - For RSS feed parsing

### Configuration

See `API_SETUP.md` for:
- NewsAPI key setup (optional)
- LinkedIn API OAuth setup (optional)
- RSS feed configuration (no setup needed)

### Files Modified

- `app/scrapers/news_scraper.py` - Complete rewrite
- `app/scrapers/linkedin_scraper.py` - Complete rewrite
- `app/scrapers/web_scraper.py` - Complete rewrite
- `app/pipeline/fact_sheet_builder.py` - Updated to use new scrapers
- `app/config/settings.py` - Added API key configuration
- `requirements.txt` - Added feedparser
- `README.md` - Updated documentation
- `QUICKSTART.md` - Updated quick start guide
- `API_SETUP.md` - New file with API setup instructions

### Deprecated Files

These files are no longer used but kept for reference:
- `app/scrapers/snapshot_parser.py` - Was for MCP snapshot parsing
- `app/scrapers/mcp_integration.py` - Was for MCP integration
- `app/scrapers/direct_mcp_scraper.py` - Was for direct MCP usage
- `MCP_INTEGRATION.md` - Old MCP integration guide
- `USING_MCP.md` - Old MCP usage guide

