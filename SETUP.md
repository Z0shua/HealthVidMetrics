# HealthVidMetrics Setup Guide

**Note:** Core logic is now in `src/healthvidmetrics/` for maintainability. Use `main.py` (Streamlit UI) or `cli.py` (CLI) as entry points.

## Quick Start

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   # or, for faster install:
   uv pip install -r requirements.txt
   ```

2. **Set up API Keys**
   
   Create a `.env` file in the project root with your API keys:
   ```bash
   # YouTube Data API v3 Key (Required)
   YOUTUBE_API_KEY=your_youtube_api_key_here
   
   # AI Provider API Keys (Choose one or more)
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   GEMINI_API_KEY=your_gemini_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   HUGGINGFACE_API_KEY=your_huggingface_api_key_here
   ```

3. **Get API Keys**

   **YouTube Data API v3:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API Key)
   - Copy the API key to your `.env` file

   **AI Providers (Choose one or more):**
   
   **OpenAI:**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Go to API Keys section
   - Create a new API key
   
   **Anthropic (Claude):**
   - Go to [Anthropic Console](https://console.anthropic.com/)
   - Sign up or log in
   - Create an API key
   
   **Google Gemini:**
   - Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Create an API key
   
   **DeepSeek:**
   - Go to [DeepSeek Platform](https://platform.deepseek.com/)
   - Sign up or log in
   - Create an API key
   
   **Hugging Face:**
   - Go to [Hugging Face](https://huggingface.co/settings/tokens)
   - Sign up or log in
   - Create an access token

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

5. **Open in Browser**
   The application will open at `http://localhost:8501`

## Usage

### Web Interface
1. Enter your YouTube API key
2. Select your preferred AI provider from the sidebar
3. Enter the corresponding API key
4. Choose input method (single URL, multiple URLs, or CSV upload)
5. Select analysis options (transcripts, AI evaluation)
6. Click "Start Analysis"
7. View results and download reports

### Command Line Interface
```bash
# Basic usage with OpenAI (default)
python cli.py --urls "https://www.youtube.com/watch?v=example"

# Use specific AI provider
python cli.py --urls "https://www.youtube.com/watch?v=example" --provider anthropic

# Use specific model
python cli.py --urls "https://www.youtube.com/watch?v=example" --provider gemini --model gemini-1.5-pro

# Export as CSV
python cli.py --urls "https://www.youtube.com/watch?v=example" --csv

# Skip AI evaluation (metadata only)
python cli.py --urls "https://www.youtube.com/watch?v=example" --no-ai
```

## Features

- **Video Metadata Extraction**: Channel, views, likes, comments, duration
- **Transcript Analysis**: Automatic transcript extraction and analysis
- **Quality Scoring**: DISCERN, Global Quality Score, JAMA Criteria
- **Multiple AI Providers**: OpenAI, Anthropic, Google Gemini, DeepSeek, Hugging Face
- **Multiple Input Methods**: Single URL, multiple URLs, CSV upload
- **Export Options**: Excel and CSV download
- **Real-time Progress**: Progress bars and status updates

## Troubleshooting

- **API Key Errors**: Make sure your API keys are correct and have proper permissions
- **Transcript Issues**: Some videos may not have available transcripts
- **Rate Limits**: All AI providers have rate limits, YouTube API has daily quotas
- **Network Issues**: Ensure stable internet connection for API calls
- **Provider-specific Issues**: Check the provider's documentation for specific error codes

## Supported AI Providers

| Provider | Models | Cost | Notes |
|----------|--------|------|-------|
| OpenAI | GPT-3.5, GPT-4 | Pay-per-token | Most widely used |
| Anthropic | Claude 3 Haiku/Sonnet/Opus | Pay-per-token | Strong reasoning |
| Google Gemini | Gemini 1.5 Flash/Pro | Pay-per-token | Good performance |
| DeepSeek | DeepSeek Chat/Coder | Pay-per-token | Cost-effective |
| Hugging Face | Various open models | Free/Paid | Self-hosted options | 