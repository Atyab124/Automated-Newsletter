# API Setup Guide

This guide explains how to set up API keys for the Newsletter Generator scrapers and LLM providers.

## News Scraper

### Option 1: NewsAPI (Recommended)

1. **Get a free API key**:
   - Visit https://newsapi.org/
   - Sign up for a free account
   - Get your API key from the dashboard

2. **Set the API key**:
   ```bash
   # Windows PowerShell
   $env:NEWSAPI_KEY="your_api_key_here"
   
   # Linux/Mac
   export NEWSAPI_KEY="your_api_key_here"
   ```

3. **Or add to your environment permanently**:
   - Windows: Add to System Environment Variables
   - Linux/Mac: Add to `~/.bashrc` or `~/.zshrc`

### Option 2: RSS Feeds (No API Key Required)

If you don't set `NEWSAPI_KEY`, the scraper will automatically fall back to RSS feeds from Google News. This works without any setup!

**Free tier limits**:
- NewsAPI free tier: 100 requests/day
- RSS feeds: No limits

## LinkedIn Scraper

LinkedIn API requires OAuth 2.0 authentication.

### Setup Steps

1. **Create a LinkedIn App**:
   - Go to https://www.linkedin.com/developers/apps
   - Create a new app
   - Note your Client ID and Client Secret

2. **Get OAuth Access Token**:
   - Follow LinkedIn's OAuth guide: https://learn.microsoft.com/en-us/linkedin/shared/authentication/authentication
   - You'll need to:
     - Set up redirect URI
     - Get authorization code
     - Exchange for access token

3. **Set Environment Variables**:
   ```bash
   export LINKEDIN_ACCESS_TOKEN="your_access_token"
   export LINKEDIN_CLIENT_ID="your_client_id"
   export LINKEDIN_CLIENT_SECRET="your_client_secret"
   ```

**Note**: LinkedIn API access requires approval for most endpoints. For basic use, you may want to skip LinkedIn scraping or use it only if you have approved API access.

### Alternative: Skip LinkedIn

If LinkedIn setup is too complex, the scraper will simply return empty results. The system works fine without LinkedIn data.

## Web Scraper

**No setup required!** The web scraper uses RSS feeds from:
- Medium (tag-based feeds)
- Dev.to (tag-based feeds)
- Hacker News (search-based feeds)

These work immediately without any API keys.

## Research Scraper

**No setup required!** Uses public APIs:
- arXiv: No authentication needed
- Semantic Scholar: No authentication needed

## Quick Start (Minimal Setup)

For the quickest start, you don't need any API keys:

1. **Research Papers**: ✅ Works immediately
2. **News**: ✅ Works with RSS feeds (no key needed)
3. **Web Articles**: ✅ Works with RSS feeds (no key needed)
4. **LinkedIn**: ⚠️ Requires API setup (optional)

## Testing Your Setup

To test if your API keys are working:

```python
from app.scrapers.news_scraper import NewsScraper
from app.scrapers.linkedin_scraper import LinkedInScraper

# Test news scraper
news = NewsScraper()
results = news.scrape("artificial intelligence")
print(f"Found {len(results)} news items")

# Test LinkedIn scraper
linkedin = LinkedInScraper()
results = linkedin.scrape("artificial intelligence")
print(f"Found {len(results)} LinkedIn posts")
```

## LLM Provider Setup

### Option 1: Ollama (Default, Free, Local)

Ollama runs locally on your machine - no API keys needed!

1. **Install Ollama**: https://ollama.ai
2. **Pull a model**: `ollama pull qwen2.5` (or llama3.2, mistral, etc.)
3. **Start Ollama**: `ollama serve`
4. **Set environment variable** (optional):
   ```bash
   export LLM_PROVIDER="ollama"
   export OLLAMA_MODEL="qwen2.5"
   ```

### Option 2: OpenAI (Cloud, Paid)

1. **Get API Key**:
   - Go to https://platform.openai.com/api-keys
   - Sign up or log in
   - Create a new API key

2. **Set Environment Variables**:
   ```bash
   export OPENAI_API_KEY="sk-..."
   export OPENAI_MODEL="gpt-4o-mini"  # or gpt-4o, gpt-4-turbo, gpt-3.5-turbo
   export LLM_PROVIDER="openai"
   ```

3. **Install OpenAI Package**:
   ```bash
   pip install openai
   ```

**Note**: OpenAI API usage is paid. Check pricing at https://openai.com/pricing

### Switching Between Providers

You can switch between Ollama and OpenAI:
- **In UI**: Use the "LLM Settings" page or sidebar dropdown
- **Via Environment**: Set `LLM_PROVIDER=ollama` or `LLM_PROVIDER=openai`

## Environment Variables Summary

```bash
# LLM Provider (default: ollama)
LLM_PROVIDER="ollama"  # or "openai"

# Ollama Configuration (if using Ollama)
OLLAMA_MODEL="qwen2.5"
OLLAMA_BASE_URL="http://localhost:11434"

# OpenAI Configuration (if using OpenAI)
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4o-mini"
OPENAI_BASE_URL="https://api.openai.com/v1"  # Optional, for custom endpoints

# Optional - for NewsAPI (falls back to RSS if not set)
NEWSAPI_KEY="your_key_here"

# Optional - for LinkedIn API (returns empty if not set)
LINKEDIN_ACCESS_TOKEN="your_token_here"
LINKEDIN_CLIENT_ID="your_client_id"
LINKEDIN_CLIENT_SECRET="your_client_secret"
```

## Troubleshooting

### NewsAPI Errors

- **"Invalid API key"**: Check your API key is correct
- **"Rate limit exceeded"**: Free tier is 100 requests/day. Wait or upgrade.
- **Falling back to RSS**: This is normal if no API key is set. RSS feeds work fine!

### LinkedIn API Errors

- **"Invalid access token"**: Token may have expired. Get a new one.
- **"Insufficient permissions"**: Your app may not have the required scopes.
- **Empty results**: This is normal if LinkedIn API isn't set up. The system works without it.

### RSS Feed Errors

- **"feedparser not installed"**: Run `pip install feedparser`
- **No results**: Some RSS feeds may not have content for your topic. Try a different topic.

## Recommended Setup

For best results with minimal setup:

1. ✅ Use RSS feeds for news (no setup needed)
2. ✅ Use RSS feeds for web articles (no setup needed)
3. ✅ Use public APIs for research papers (no setup needed)
4. ⚠️ Skip LinkedIn unless you need it (requires complex OAuth setup)

This gives you 3 out of 4 sources working immediately!

