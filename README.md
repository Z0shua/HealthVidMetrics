_A Tool for Rating Educational YouTube Videos Using Healthcare Quality Metrics_

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

**This project** is an open-source Python tool designed to extract data from educational YouTube videos, particularly healthcare-related content, and rate them based on well-known healthcare scoring frameworks such as the DISCERN score, Global Quality Score (GQS), and JAMA benchmark criteria.

This project pulls video metadata like the channel name, views, likes, comments, and transcripts, and leverages a Large Language Model (LLM) to automatically rate healthcare videos based on their content quality.

This tool is designed for researchers, educators, and healthcare professionals looking to evaluate YouTube videos based on educational and informational quality.

## Features

- Extract metadata from YouTube videos (channel name, country, views, likes, comments, and subtitles availability).
- Scrape video transcripts (if available) for further analysis.
- Automatically rate healthcare content using:
  - **DISCERN Score**: Quality of health information.
  - **Global Quality Score (GQS)**: Overall quality.
  - **JAMA Benchmark Criteria**: Authorship, Attribution, Currency, and Disclosure.
- Export results to an Excel or CSV file for further analysis.
- Easy-to-use, customizable, and scalable for large datasets.

## Installation

```bash
git clone https://github.com/Z0shua/HealthVidMetrics.git
cd HealthVidMetrics
pip install -r requirements.txt
```

Prerequisites:

* Python 3.7+
* YouTube Data API Key: Create a project in Google Cloud and enable the YouTube Data API.
* OpenAI API Key: For LLM-based automatic video ratings.

## Usage

Add Your API Keys:

Create a `.env` file in the project root and add your API keys:

```bash
YOUTUBE_API_KEY=your_youtube_api_key
OPENAI_API_KEY=your_openai_api_key
```

Prepare a list of YouTube video links:

In the main script (`main.py`), replace the placeholder `video_links` list with your own set of video links:

```python
video_links = [
    'https://www.youtube.com/watch?v=example1',
    'https://www.youtube.com/watch?v=example2'
]
```

Run the Script:

To analyze the YouTube videos and generate an Excel file:

```bash
python main.py
```

Outputs:

The tool will output an Excel file (`youtube_videos.xlsx`) that contains video details, including channel information, transcript, and quality scores (DISCERN, Global Quality, JAMA).

Each row corresponds to a video, with columns for all extracted data and computed scores.

## API Setup

To use HealthVidMetrics, you need API keys from the following services:

* YouTube Data API: Create a project in the Google Cloud Console. Enable the YouTube Data API v3. Generate an API Key and add it to your `.env` file.
* OpenAI API: Sign up for OpenAI API access. Generate an API Key. Add it to your `.env` file.

## Rating Criteria

The tool uses healthcare-specific quality benchmarks to evaluate YouTube content:

* **DISCERN Score**: Rates the reliability and quality of health information (1-5).
* **Global Quality Score (GQS)**: A general score for the overall quality of the video (1-5).
* **JAMA Benchmark Criteria**: Analyzes Authorship, Attribution, Currency, and Disclosure (scores from 0-4).

## Contributing

We welcome contributions to HealthVidMetrics! Here's how you can help:

* Fork the repository.
* Create a new branch for your feature or fix.
* Submit a pull request.
* All contributions should follow the project style guide and pass any tests. Before opening a PR, ensure your code passes basic checks.

## Issues

If you encounter bugs or have suggestions, please open an issue.
