#!/usr/bin/env python3
"""
HealthVidMetrics Command Line Interface
A simple CLI version of the healthcare video analysis tool
"""

import pandas as pd
import os
import re
import argparse
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def convert_duration_to_seconds(duration):
    """Convert YouTube ISO 8601 duration to seconds"""
    match = re.match('PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def get_video_transcript(video_id):
    """Get video transcript from YouTube"""
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception as e:
        print(f"Warning: Transcript not available for video {video_id}: {e}")
        return None

def get_video_details(youtube, video_ids):
    """Get detailed information about YouTube videos"""
    video_details = []
    
    for i in range(0, len(video_ids), 50):
        batch_ids = video_ids[i:i+50]
        
        request = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=','.join(batch_ids)
        )
        response = request.execute()

        for item in response['items']:
            video_id = item['id']
            channel_name = item['snippet']['channelTitle']
            video_title = item['snippet']['title']
            country = item['snippet'].get('defaultAudioLanguage', 'Unknown')
            video_length = convert_duration_to_seconds(item['contentDetails']['duration'])
            views = int(item['statistics'].get('viewCount', 0))
            likes = int(item['statistics'].get('likeCount', 0))
            comments = int(item['statistics'].get('commentCount', 0))
            upload_year = item['snippet']['publishedAt'][:4]
            subtitles = 'Yes' if 'caption' in item['contentDetails'] and item['contentDetails']['caption'] == 'true' else 'No'

            # Get transcript
            transcript = get_video_transcript(video_id)

            video_details.append({
                'Video ID': video_id,
                'Video Title': video_title,
                'Channel Name': channel_name,
                'Country': country,
                'Video Length (Seconds)': video_length,
                'Views': views,
                'Likes': likes,
                'Comments': comments,
                'Upload Year': upload_year,
                'Subtitles/CC Available': subtitles,
                'Transcript': transcript
            })

    return video_details

def evaluate_healthcare_video(transcript, video_id):
    """Evaluate healthcare video quality using OpenAI"""
    if transcript is None:
        return {
            "DISCERN Score": None, 
            "Global Quality Score": None, 
            "JAMA Criteria Score": None,
            "Evaluation Notes": "No transcript available for evaluation"
        }

    prompt = f"""
    You are a healthcare content quality evaluator. Analyze the following YouTube video transcript and provide scores based on established healthcare quality metrics.

    TRANSCRIPT:
    {transcript[:4000]}

    Please evaluate this healthcare video content and provide the following scores:

    1. DISCERN Score (1-5): Rate the reliability and quality of health information
    2. Global Quality Score (1-5): Overall educational and informational quality
    3. JAMA Criteria Score (0-4): Based on JAMA benchmark criteria (Authorship, Attribution, Currency, Disclosure)

    Provide your response in this exact format:
    DISCERN Score: [number]
    Global Quality Score: [number]
    JAMA Criteria Score: [number]
    Evaluation Notes: [brief explanation of scores]
    """

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a healthcare content quality evaluator with expertise in medical information assessment."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=300,
            temperature=0.3
        )

        evaluation = response.choices[0].message.content.strip()
        
        # Parse scores from response
        discern_match = re.search(r"DISCERN Score:\s*(\d)", evaluation)
        global_quality_match = re.search(r"Global Quality Score:\s*(\d)", evaluation)
        jama_match = re.search(r"JAMA Criteria Score:\s*(\d)", evaluation)
        notes_match = re.search(r"Evaluation Notes:\s*(.+)", evaluation, re.DOTALL)

        return {
            "DISCERN Score": int(discern_match.group(1)) if discern_match else None,
            "Global Quality Score": int(global_quality_match.group(1)) if global_quality_match else None,
            "JAMA Criteria Score": int(jama_match.group(1)) if jama_match else None,
            "Evaluation Notes": notes_match.group(1).strip() if notes_match else "Evaluation completed"
        }
    except Exception as e:
        print(f"Error evaluating video {video_id}: {e}")
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": f"Evaluation failed: {str(e)}"
        }

def extract_video_id(url):
    """Extract video ID from various YouTube URL formats"""
    patterns = [
        r'(?:youtube\.com\/watch\?v=|youtu\.be\/|youtube\.com\/embed\/)([^&\n?#]+)',
        r'youtube\.com\/watch\?.*v=([^&\n?#]+)'
    ]
    
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def save_to_excel(data, filename='healthcare_video_analysis.xlsx'):
    """Save analysis results to Excel file"""
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

def main():
    parser = argparse.ArgumentParser(description='HealthVidMetrics - Healthcare Video Quality Analysis')
    parser.add_argument('--urls', nargs='+', help='YouTube video URLs to analyze')
    parser.add_argument('--file', help='CSV file containing video URLs')
    parser.add_argument('--output', default='healthcare_video_analysis.xlsx', help='Output filename')
    parser.add_argument('--no-ai', action='store_true', help='Skip AI evaluation')
    parser.add_argument('--no-transcript', action='store_true', help='Skip transcript extraction')
    
    args = parser.parse_args()
    
    # Get API keys
    youtube_api_key = os.getenv('YOUTUBE_API_KEY')
    openai_api_key = os.getenv('OPENAI_API_KEY')
    
    if not youtube_api_key:
        print("Error: YOUTUBE_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return
    
    if not args.no_ai and not openai_api_key:
        print("Error: OPENAI_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment, or use --no-ai flag")
        return
    
    # Get video URLs
    video_urls = []
    if args.urls:
        video_urls = args.urls
    elif args.file:
        try:
            df = pd.read_csv(args.file)
            if 'url' in df.columns:
                video_urls = df['url'].tolist()
            else:
                print("Error: CSV file must contain a 'url' column")
                return
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return
    else:
        print("Error: Please provide either --urls or --file argument")
        return
    
    # Extract video IDs
    video_ids = []
    invalid_urls = []
    
    for url in video_urls:
        video_id = extract_video_id(url)
        if video_id:
            video_ids.append(video_id)
        else:
            invalid_urls.append(url)
    
    if invalid_urls:
        print(f"Warning: Invalid URLs found: {invalid_urls}")
    
    if not video_ids:
        print("Error: No valid video IDs found")
        return
    
    print(f"Analyzing {len(video_ids)} videos...")
    
    try:
        # Initialize YouTube API
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
        print("Fetching video details...")
        video_details = get_video_details(youtube, video_ids)
        
        if not args.no_ai:
            print("Evaluating video quality with AI...")
            for i, detail in enumerate(video_details):
                print(f"Evaluating video {i+1}/{len(video_details)}: {detail['Video Title'][:50]}...")
                scores = evaluate_healthcare_video(detail['Transcript'], detail['Video ID'])
                detail.update(scores)
        
        # Remove transcript if not requested
        if args.no_transcript:
            for detail in video_details:
                detail.pop('Transcript', None)
        
        # Save results
        filename = save_to_excel(video_details, args.output)
        print(f"Analysis complete! Results saved to {filename}")
        
        # Print summary
        df = pd.DataFrame(video_details)
        print(f"\nSummary:")
        print(f"Total videos analyzed: {len(df)}")
        if 'Views' in df.columns:
            print(f"Average views: {df['Views'].mean():,.0f}")
        if 'DISCERN Score' in df.columns:
            avg_discern = df['DISCERN Score'].mean()
            if avg_discern:
                print(f"Average DISCERN Score: {avg_discern:.1f}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your API keys and try again.")

if __name__ == "__main__":
    main() 