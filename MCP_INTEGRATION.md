# Playwright MCP Integration Guide

This guide explains how to integrate Playwright MCP tools with the Newsletter Generator scrapers.

## Overview

The Newsletter Generator uses Playwright MCP for scraping news, LinkedIn posts, and web articles. The research paper scrapers (arXiv, Semantic Scholar) work immediately using their public APIs.

## MCP Tools Available in Cursor

When running in Cursor, the following Playwright MCP tools are available:

- `mcp_Playwright_browser_navigate(url)` - Navigate to a URL
- `mcp_Playwright_browser_snapshot()` - Get page accessibility snapshot
- `mcp_Playwright_browser_click(element, ref)` - Click an element
- `mcp_Playwright_browser_type(element, ref, text)` - Type text
- `mcp_Playwright_browser_evaluate(function)` - Run JavaScript

## Integration Options

### Option 1: Direct MCP Calls (In Cursor)

When you're in Cursor and want to use MCP tools directly, you can modify the scrapers to call MCP functions. However, since the scrapers are Python classes and MCP tools are function calls, you have a few options:

1. **Pass MCP tools as a dictionary** to the fact sheet builder
2. **Create a wrapper class** that bridges Python and MCP calls
3. **Use the scrapers in a context where MCP is available** (e.g., through Cursor's AI assistant)

### Option 2: Enhanced Scrapers with MCP Support

The scrapers are designed to work with an MCP client. Here's how to set it up:

```python
# Example: Creating an MCP client wrapper
class MCPClient:
    def __init__(self):
        # In Cursor, you would initialize with access to MCP tools
        pass
    
    def navigate(self, url):
        # Call: mcp_Playwright_browser_navigate(url=url)
        pass
    
    def snapshot(self):
        # Call: mcp_Playwright_browser_snapshot()
        return {}
```

### Option 3: Using Research Papers Only

The research paper scraper works immediately without MCP:

- **arXiv**: Public API, no authentication
- **Semantic Scholar**: Public API, no authentication

You can use the system with just research papers while setting up MCP integration for other sources.

## Current Implementation

The current scrapers are structured to:

1. **Work immediately**: Research papers (arXiv, Semantic Scholar) work out of the box
2. **Support MCP when available**: News, LinkedIn, and web scrapers accept an MCP client
3. **Gracefully degrade**: If MCP is not available, those scrapers return empty lists

## Example Usage

### With MCP (In Cursor)

```python
from app.pipeline.fact_sheet_builder import FactSheetBuilder

# Create MCP client (implementation depends on your setup)
mcp_client = create_mcp_client()  # Your MCP client implementation

builder = FactSheetBuilder()
fact_sheet = builder.build_fact_sheet("Artificial Intelligence", use_mcp_client=mcp_client)
```

### Without MCP (Research Papers Only)

```python
from app.pipeline.fact_sheet_builder import FactSheetBuilder

builder = FactSheetBuilder()
fact_sheet = builder.build_fact_sheet("Artificial Intelligence")  # Only research papers
```

## Future Enhancements

To fully integrate MCP:

1. Create a proper MCP client wrapper that can be instantiated in Python
2. Update scrapers to parse accessibility snapshots more effectively
3. Add error handling and retry logic for web scraping
4. Implement rate limiting and respectful scraping practices

## Notes

- The research paper scrapers work immediately and don't require MCP
- Playwright MCP scrapers will return empty results if MCP is not available
- The system is designed to work with partial data (e.g., just research papers)
- Newsletter generation works with whatever data is available in the fact sheet

