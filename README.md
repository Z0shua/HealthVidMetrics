# HealthVidMetrics

_A Tool for Rating Educational YouTube Videos Using Healthcare Quality Metrics_

---

**Project Structure (v2 Modularized)**

- `src/healthvidmetrics/` — Core logic (YouTube API, scoring, utils, export)
- `main.py` — Streamlit app (UI only)
- `cli.py` — Command-line interface (CLI only)
- `tests/` — Unit and integration tests
- `requirements.txt`, `.gitignore`, `README.md`, `SETUP.md`, `sample_videos.csv`

---

## Table of Contents
### 1. [Introduction](#introduction)
### 2. [Features](#features)
### 3. [Installation](#installation)
### 4. [Usage](#usage)
### 5. [API Setup](#api-setup)
### 6. [Rating Criteria](#rating-criteria)
### 7. [Contributing](#contributing)
### 8. [License](#license)

## Introduction

**HealthVidMetrics** is an open-source Python tool designed to extract data from educational YouTube videos, particularly healthcare-related content, and rate them based on well-known healthcare scoring frameworks such as the DISCERN score, Global Quality Score (GQS), and JAMA benchmark criteria.

This project pulls video metadata like the channel name, views, likes, comments, and transcripts, and leverages a Large Language Model (LLM) to automatically rate healthcare videos based on their content quality.

This tool is designed for researchers, educators, and healthcare professionals looking to evaluate YouTube videos based on educational and informational quality.

## Features

- **Multiple Interfaces**: Web-based Streamlit app and command-line interface
- **Video Metadata Extraction**: Channel name, country, views, likes, comments, duration, and subtitles availability
- **Transcript Analysis**: Automatic transcript extraction and analysis
- **AI-Powered Quality Assessment**: Automatically rate healthcare content using:
  - **DISCERN Score**: Quality of health information (1-5)
  - **Global Quality Score (GQS)**: Overall quality (1-5)
  - **JAMA Benchmark Criteria**: Authorship, Attribution, Currency, and Disclosure (0-4)
- **Multiple Input Methods**: Single URL, multiple URLs, or CSV file upload
- **Export Options**: Excel and CSV file downloads
- **Real-time Progress**: Progress bars and status updates
- **Easy-to-use Interface**: Modern, responsive web UI

## Installation

```bash
git clone https://github.com/Z0shua/HealthVidMetrics.git
cd HealthVidMetrics
pip install -r requirements.txt
```

### Prerequisites

* Python 3.7+
* YouTube Data API Key: Create a project in Google Cloud and enable the YouTube Data API
* OpenAI API Key: For LLM-based automatic video ratings

## Usage

### Web Interface (Recommended)

1. **Set up API Keys**:
   Create a `.env` file in the project root:
   ```bash
   YOUTUBE_API_KEY=your_youtube_api_key
   OPENAI_API_KEY=your_openai_api_key
   ```

2. **Run the Streamlit App**:
   ```bash
   streamlit run main.py
   ```

3. **Open in Browser**:
   The application will open at `http://localhost:8501`

### Command Line Interface

```bash
# Analyze single video
python cli.py --urls "https://www.youtube.com/watch?v=example"

# Analyze multiple videos
python cli.py --urls "https://www.youtube.com/watch?v=example1" "https://www.youtube.com/watch?v=example2"

# Analyze videos from CSV file
python cli.py --file sample_videos.csv

# Skip AI evaluation (metadata only)
python cli.py --urls "https://www.youtube.com/watch?v=example" --no-ai

# Custom output filename
python cli.py --urls "https://www.youtube.com/watch?v=example" --output my_analysis.xlsx
```

### Input Methods

1. **Single Video URL**: Enter one YouTube URL
2. **Multiple Video URLs**: Enter multiple URLs (one per line)
3. **CSV Upload**: Upload a CSV file with a 'url' column

### Analysis Options

- **Include Transcripts**: Extract and include video transcripts
- **AI Evaluation**: Use OpenAI to assess video quality
- **Export Formats**: Excel (.xlsx) or CSV files

## API Setup

To use HealthVidMetrics, you need API keys from the following services:

### YouTube Data API v3
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable YouTube Data API v3
4. Create credentials (API Key)
5. Add the API key to your `.env` file

### OpenAI API
1. Go to [OpenAI Platform](https://platform.openai.com/)
2. Sign up or log in
3. Go to API Keys section
4. Create a new API key
5. Add the API key to your `.env` file

## Rating Criteria

The tool uses healthcare-specific quality benchmarks to evaluate YouTube content:

### DISCERN Score (1-5)
- **1**: Very poor quality, potentially harmful
- **2**: Poor quality, unreliable information
- **3**: Moderate quality, some concerns
- **4**: Good quality, generally reliable
- **5**: Excellent quality, highly reliable

### Global Quality Score (1-5)
- **1**: Very poor overall quality
- **2**: Poor overall quality
- **3**: Moderate overall quality
- **4**: Good overall quality
- **5**: Excellent overall quality

### JAMA Benchmark Criteria (0-4)
- **0**: Meets none of the criteria
- **1**: Meets 1 criterion
- **2**: Meets 2 criteria
- **3**: Meets 3 criteria
- **4**: Meets all 4 criteria

**JAMA Criteria**: Authorship, Attribution, Currency, and Disclosure

## Output

The tool generates comprehensive reports including:

- **Video Metadata**: ID, title, channel, views, likes, comments, duration
- **Transcript Data**: Full video transcript (if available)
- **Quality Scores**: DISCERN, Global Quality, and JAMA scores
- **Evaluation Notes**: AI-generated explanations of scores
- **Summary Statistics**: Average scores and metrics

## Contributing

We welcome contributions to HealthVidMetrics! Here's how you can help:

* Fork the repository
* Create a new branch for your feature or fix
* Submit a pull request
* All contributions should follow the project style guide and pass any tests

## Issues

If you encounter bugs or have suggestions, please open an issue on GitHub.

## License

This project is open source and available under the MIT License.
