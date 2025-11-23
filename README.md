# Automated Newsletter Generator

A Python-based automated newsletter system that scrapes content from multiple sources, builds fact sheets, and generates newsletters using your writing style.

## Features

- **Multi-Source Scraping**: Scrapes research papers (arXiv, Semantic Scholar), news headlines (NewsAPI/RSS), LinkedIn posts (LinkedIn API), and web articles (RSS feeds)
- **Open Source APIs**: Uses only open-source APIs - no closed-source dependencies
- **Fact Sheet Generation**: Creates structured fact sheets with verified sources
- **Writing Style Learning**: Extracts your writing style from uploaded samples
- **AI-Powered Generation**: Uses Ollama to generate newsletters strictly from fact sheets (no hallucinations)
- **Automated Scheduling**: Runs on configurable schedules (daily, weekly, monthly, etc.)
- **Streamlit UI**: Beautiful web interface for managing topics, samples, and newsletters

## Requirements

- Python 3.8+
- Ollama installed and running (default: http://localhost:11434)
- Optional: NewsAPI key for news scraping (free tier available, or uses RSS feeds)
- Optional: LinkedIn API credentials for LinkedIn scraping

## Installation

1. Clone or navigate to this directory

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Install and start Ollama:
   - Download from https://ollama.ai
   - Install and start the Ollama service
   - Pull a model (e.g., `ollama pull qwen2.5`)

4. (Optional) Set up API keys:
   - NewsAPI: Get free key from https://newsapi.org/ (or use RSS feeds - no key needed)
   - LinkedIn: Requires OAuth setup (see API_SETUP.md)
   - See `API_SETUP.md` for detailed instructions

## Configuration

Edit `app/config/settings.py` to configure:

- `OLLAMA_BASE_URL`: Ollama API endpoint (default: http://localhost:11434)
- `OLLAMA_MODEL`: Model to use (default: llama3.2)
- `DATABASE_PATH`: SQLite database path (default: newsletter.db)
- `FREQUENCY_OPTIONS`: Available scheduling frequencies

## Usage

### Starting the Application

Run the Streamlit app:

```bash
streamlit run app/ui/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

### Workflow

1. **Add Topics** (Topics Manager page):
   - Enter a topic name
   - Select frequency (daily, weekly, biweekly, monthly)
   - Click "Add Topic"

2. **Upload Writing Samples** (Writing Samples page):
   - Select a topic
   - Upload a text file or paste writing samples
   - The system will learn your writing style from these samples

3. **Generate Fact Sheets** (Fact Sheets page):
   - Select a topic
   - Click "Generate New Fact Sheet"
   - View the generated fact sheet with all sources

4. **Generate Newsletter** (Generate Newsletter page):
   - Select a topic
   - Click "Generate Newsletter"
   - Preview and download the generated newsletter

### Automated Scheduling

The scheduler runs automatically in the background:

- Checks every hour for topics that are due
- Runs the full pipeline (scraping → fact sheet → newsletter) for due topics
- Updates last run time after completion

Start/stop the scheduler from the sidebar in the Streamlit app.

## Project Structure

```
app/
├── ui/
│   └── streamlit_app.py          # Streamlit UI
├── scrapers/
│   ├── base_scraper.py           # Base scraper class
│   ├── news_scraper.py           # News scraper (Playwright MCP)
│   ├── linkedin_scraper.py       # LinkedIn scraper (Playwright MCP)
│   ├── research_scraper.py       # Research papers (APIs)
│   └── web_scraper.py            # Web articles (Playwright MCP)
├── pipeline/
│   ├── fact_sheet_builder.py     # Builds fact sheets
│   └── scheduler.py              # Automated scheduling
├── llm/
│   ├── style_extractor.py        # Extracts writing style (Ollama)
│   └── newsletter_generator.py   # Generates newsletters (Ollama)
├── db/
│   └── database.py               # SQLite database management
├── config/
│   └── settings.py               # Configuration
└── mcp_wrapper.py                # Playwright MCP wrapper
```

## Data Storage

All data is stored in SQLite (`newsletter.db` by default):

- **topics**: Topic names, frequencies, last run times
- **writing_samples**: User-uploaded writing samples
- **fact_sheets**: Generated fact sheets (Markdown + JSON)
- **newsletters**: Generated newsletters (Markdown)

## Scraping Sources

### Research Papers
- **arXiv**: Uses arXiv API (no authentication required)
- **Semantic Scholar**: Uses Semantic Scholar API (no authentication required)

### News
- **NewsAPI**: Uses NewsAPI (optional API key, free tier: 100 requests/day)
- **RSS Feeds**: Falls back to Google News RSS feeds if no API key (no limits)

### LinkedIn
- **LinkedIn API**: Uses LinkedIn API with OAuth 2.0 (requires authentication setup)
- See `API_SETUP.md` for setup instructions

### Web Articles
- **RSS Feeds**: Scrapes from Medium, Dev.to, Hacker News RSS feeds
- No API keys required - works immediately!

## Important Notes

### API Setup

Most scrapers work immediately without setup:
- ✅ Research papers: No setup needed
- ✅ News: Works with RSS feeds (no setup), or use NewsAPI key for more results
- ✅ Web articles: Works with RSS feeds (no setup)
- ⚠️ LinkedIn: Requires OAuth setup (optional - see API_SETUP.md)

See `API_SETUP.md` for detailed API setup instructions.

### No Hallucinations

The newsletter generator is explicitly instructed to:
- Use ONLY information from the fact sheet
- Cite all sources
- Never make up facts or information

### Local & Open Source

- All processing runs locally
- Uses only open-source tools (Ollama, SQLite, Streamlit)
- No external API keys required (except for public APIs like arXiv)

## Troubleshooting

### Ollama Connection Error
- Ensure Ollama is running: `ollama serve`
- Check the URL in `app/config/settings.py`
- Verify the model is installed: `ollama list`

### Scraping Issues
- Playwright MCP scrapers require MCP to be available in Cursor
- Some sites may have rate limiting or require authentication
- Research paper APIs (arXiv, Semantic Scholar) should work without issues

### Database Errors
- Ensure write permissions in the directory
- Check that SQLite is available (comes with Python)

## License

This project is open source and available for use.

## Contributing

Feel free to extend the scrapers, add new sources, or improve the newsletter generation prompts!

