# Quick Start Guide

Get your Newsletter Generator up and running in minutes!

## Prerequisites Check

Before starting, ensure you have:

- ✅ Python 3.8 or higher
- ✅ Ollama installed and running
- ✅ Internet connection (for scraping)

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

## Step 2: Start Ollama

Make sure Ollama is running:

```bash
# Check if Ollama is running
ollama list

# If not running, start it:
ollama serve

# Pull a model (if you haven't already):
ollama pull llama3.2
```

## Step 3: Run the Application

```bash
# Option 1: Use the run script
python run.py

# Option 2: Direct Streamlit command
streamlit run app/ui/streamlit_app.py
```

The app will open in your browser at `http://localhost:8501`

## Step 4: Create Your First Newsletter

### 4.1 Add a Topic

1. Go to **Topics Manager** page
2. Enter a topic (e.g., "Machine Learning")
3. Select frequency (e.g., "weekly")
4. Click "Add Topic"

### 4.2 (Optional) Upload Writing Samples

1. Go to **Writing Samples** page
2. Select your topic
3. Upload a text file or paste writing samples
4. Click "Save Writing Sample"

This helps the AI learn your writing style!

### 4.3 Generate Fact Sheet

1. Go to **Fact Sheets** page
2. Select your topic
3. Click "Generate New Fact Sheet"

**Note**: Currently, research papers (arXiv, Semantic Scholar) will work immediately. News, LinkedIn, and web scraping require Playwright MCP integration (see MCP_INTEGRATION.md).

### 4.4 Generate Newsletter

1. Go to **Generate Newsletter** page
2. Select your topic
3. Click "Generate Newsletter"
4. Preview and download your newsletter!

## What Works Immediately

✅ **Research Papers**: arXiv and Semantic Scholar scraping works out of the box  
✅ **Fact Sheet Generation**: Creates structured fact sheets from available data  
✅ **Style Extraction**: Learns from your writing samples  
✅ **Newsletter Generation**: Uses Ollama to generate newsletters  
✅ **Scheduling**: Automated pipeline runs on schedule  

## What Requires Setup

⚠️ **News/LinkedIn/Web Scraping**: Requires Playwright MCP integration (see MCP_INTEGRATION.md)

The system works with just research papers, so you can start using it immediately!

## Troubleshooting

### "Ollama connection error"
- Make sure Ollama is running: `ollama serve`
- Check the model is installed: `ollama list`
- Verify the URL in `app/config/settings.py`

### "No fact sheet generated"
- Check your internet connection
- Research paper APIs should work without issues
- For other sources, see MCP_INTEGRATION.md

### "Database error"
- Ensure you have write permissions in the directory
- SQLite comes with Python, so this should work automatically

## Next Steps

- Read the full [README.md](README.md) for detailed documentation
- Check [MCP_INTEGRATION.md](MCP_INTEGRATION.md) for Playwright MCP setup
- Customize settings in `app/config/settings.py`
- Add more topics and experiment with different frequencies

Happy newsletter generating! 📰

