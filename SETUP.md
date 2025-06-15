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
   # YouTube Data API v3 Key
   YOUTUBE_API_KEY=your_youtube_api_key_here
   
   # OpenAI API Key
   OPENAI_API_KEY=your_openai_api_key_here
   ```

3. **Get API Keys**

   **YouTube Data API v3:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Create a new project or select existing one
   - Enable YouTube Data API v3
   - Create credentials (API Key)
   - Copy the API key to your `.env` file

   **OpenAI API:**
   - Go to [OpenAI Platform](https://platform.openai.com/)
   - Sign up or log in
   - Go to API Keys section
   - Create a new API key
   - Copy the API key to your `.env` file

4. **Run the Application**
   ```bash
   streamlit run main.py
   ```

5. **Open in Browser**
   The application will open at `http://localhost:8501`

## Usage

1. Enter your API keys in the sidebar
2. Choose input method (single URL, multiple URLs, or CSV upload)
3. Select analysis options (transcripts, AI evaluation)
4. Click "Start Analysis"
5. View results and download reports

## Features

- **Video Metadata Extraction**: Channel, views, likes, comments, duration
- **Transcript Analysis**: Automatic transcript extraction and analysis
- **Quality Scoring**: DISCERN, Global Quality Score, JAMA Criteria
- **Multiple Input Methods**: Single URL, multiple URLs, CSV upload
- **Export Options**: Excel and CSV download
- **Real-time Progress**: Progress bars and status updates

## Troubleshooting

- **API Key Errors**: Make sure your API keys are correct and have proper permissions
- **Transcript Issues**: Some videos may not have available transcripts
- **Rate Limits**: YouTube API has daily quotas, OpenAI has rate limits
- **Network Issues**: Ensure stable internet connection for API calls 