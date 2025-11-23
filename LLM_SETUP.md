# LLM Provider Setup Guide

The Newsletter Generator supports two LLM providers: **Ollama** (local, free) and **OpenAI** (cloud, paid).

## Quick Comparison

| Feature | Ollama | OpenAI |
|---------|--------|--------|
| **Cost** | Free | Paid (per token) |
| **Location** | Local (your machine) | Cloud |
| **Setup** | Install + pull model | API key only |
| **Privacy** | 100% local | Data sent to OpenAI |
| **Speed** | Depends on hardware | Fast (cloud) |
| **Models** | Many open-source models | GPT-4, GPT-3.5, etc. |

## Option 1: Ollama (Recommended for Local Use)

### Installation

1. **Download and Install Ollama**:
   - Visit https://ollama.ai
   - Download for your OS (Windows, Mac, Linux)
   - Install the application

2. **Start Ollama**:
   ```bash
   ollama serve
   ```
   (On Windows/Mac, Ollama usually starts automatically)

3. **Pull a Model**:
   ```bash
   # Recommended models:
   ollama pull qwen2.5        # Good balance of quality and speed
   ollama pull llama3.2       # Popular, well-tested
   ollama pull mistral        # Fast and efficient
   ollama pull gemma2         # Google's model
   ```

4. **Configure** (optional):
   ```bash
   export LLM_PROVIDER="ollama"
   export OLLAMA_MODEL="qwen2.5"
   export OLLAMA_BASE_URL="http://localhost:11434"
   ```

### Testing Ollama

```bash
# Test if Ollama is working
ollama run qwen2.5 "Say hello"
```

### Available Models

- `qwen2.5` - Recommended, good balance
- `llama3.2` - Popular, well-tested
- `mistral` - Fast and efficient
- `gemma2` - Google's model
- `phi3` - Microsoft's small model
- `neural-chat` - Conversational model

See all models: https://ollama.com/library

## Option 2: OpenAI (Cloud-Based)

### Setup

1. **Get API Key**:
   - Go to https://platform.openai.com/api-keys
   - Sign up or log in
   - Click "Create new secret key"
   - Copy the key (starts with `sk-`)

2. **Set Environment Variable**:
   ```bash
   # Windows PowerShell
   $env:OPENAI_API_KEY="sk-your-key-here"
   
   # Linux/Mac
   export OPENAI_API_KEY="sk-your-key-here"
   ```

3. **Install OpenAI Package**:
   ```bash
   pip install openai
   ```

4. **Configure**:
   ```bash
   export LLM_PROVIDER="openai"
   export OPENAI_MODEL="gpt-4o-mini"  # or gpt-4o, gpt-4-turbo, gpt-3.5-turbo
   ```

### Available Models

- `gpt-4o-mini` - Recommended, fast and cheap
- `gpt-4o` - Most capable
- `gpt-4-turbo` - Previous generation
- `gpt-3.5-turbo` - Cheapest option

**Pricing** (as of 2024):
- GPT-4o-mini: ~$0.15 per 1M input tokens
- GPT-4o: ~$2.50 per 1M input tokens
- GPT-3.5-turbo: ~$0.50 per 1M input tokens

Check current pricing: https://openai.com/pricing

## Switching Between Providers

### In the UI

1. Go to **LLM Settings** page in the Streamlit app
2. Select your provider (Ollama or OpenAI)
3. Configure settings
4. Test the connection

### Via Environment Variables

```bash
# Use Ollama
export LLM_PROVIDER="ollama"

# Use OpenAI
export LLM_PROVIDER="openai"
```

Then restart the Streamlit app.

## Configuration in Code

You can also specify the provider when creating extractors/generators:

```python
from llm.style_extractor import StyleExtractor
from llm.newsletter_generator import NewsletterGenerator

# Use Ollama
extractor = StyleExtractor(provider="ollama", model="qwen2.5")
generator = NewsletterGenerator(provider="ollama", model="qwen2.5")

# Use OpenAI
extractor = StyleExtractor(provider="openai", model="gpt-4o-mini")
generator = NewsletterGenerator(provider="openai", model="gpt-4o-mini")
```

## Troubleshooting

### Ollama Issues

**"Connection refused"**:
- Make sure Ollama is running: `ollama serve`
- Check the URL: `http://localhost:11434`

**"Model not found"**:
- Pull the model: `ollama pull qwen2.5`
- Check available models: `ollama list`

**Slow generation**:
- Use a smaller model (e.g., `qwen2.5:1b` instead of `qwen2.5:7b`)
- Check your system resources (CPU/RAM)

### OpenAI Issues

**"Invalid API key"**:
- Check your API key is correct
- Make sure it starts with `sk-`
- Verify it's set: `echo $OPENAI_API_KEY`

**"Rate limit exceeded"**:
- You've hit OpenAI's rate limits
- Wait a bit or upgrade your plan
- Check usage: https://platform.openai.com/usage

**"Module not found: openai"**:
- Install: `pip install openai`

## Recommendations

- **For privacy/offline use**: Use Ollama
- **For best quality**: Use OpenAI GPT-4o
- **For cost efficiency**: Use Ollama or OpenAI GPT-4o-mini
- **For speed**: Use OpenAI (cloud is faster than local)

## Testing Your Setup

Use the **LLM Settings** page in the Streamlit UI to test your configuration. It will:
- Test the connection
- Show current settings
- Provide setup instructions

