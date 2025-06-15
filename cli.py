#!/usr/bin/env python3
"""
HealthVidMetrics Command Line Interface
A simple CLI version of the healthcare video analysis tool
"""

import os
import argparse
import pandas as pd
from src.healthvidmetrics.config import load_api_keys, get_ai_provider_config
from src.healthvidmetrics.youtube_api import extract_video_id, get_video_details
from src.healthvidmetrics.scoring import evaluate_healthcare_video
from src.healthvidmetrics.export import save_to_excel, save_to_csv

def main():
    parser = argparse.ArgumentParser(description='HealthVidMetrics - Healthcare Video Quality Analysis')
    parser.add_argument('--urls', nargs='+', help='YouTube video URLs to analyze')
    parser.add_argument('--file', help='CSV file containing video URLs')
    parser.add_argument('--output', default='healthcare_video_analysis.xlsx', help='Output filename')
    parser.add_argument('--csv', action='store_true', help='Export as CSV instead of Excel')
    parser.add_argument('--no-ai', action='store_true', help='Skip AI evaluation')
    parser.add_argument('--no-transcript', action='store_true', help='Skip transcript extraction')
    parser.add_argument('--provider', choices=['openai', 'anthropic', 'gemini', 'deepseek', 'huggingface'], 
                       default='openai', help='AI provider to use for evaluation')
    parser.add_argument('--model', help='Specific model to use (optional)')
    
    args = parser.parse_args()

    api_keys = load_api_keys()
    youtube_api_key = api_keys.get('youtube')
    
    if not youtube_api_key:
        print("Error: YOUTUBE_API_KEY not found in environment variables")
        print("Please set it in your .env file or environment")
        return
    
    if not args.no_ai:
        provider_config = get_ai_provider_config(args.provider)
        if not provider_config or not provider_config['api_key']:
            print(f"Error: {args.provider.upper()}_API_KEY not found in environment variables")
            print("Please set it in your .env file or environment, or use --no-ai flag")
            return
        ai_api_key = provider_config['api_key']
    else:
        ai_api_key = None
    
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
    
    print(f"Analyzing {len(video_ids)} videos using {args.provider}...")
    
    try:
        from googleapiclient.discovery import build
        youtube = build('youtube', 'v3', developerKey=youtube_api_key)
        
        print("Fetching video details...")
        video_details = get_video_details(youtube, video_ids, include_transcript=not args.no_transcript)
        
        if not args.no_ai:
            print(f"Evaluating video quality with {args.provider}...")
            for i, detail in enumerate(video_details):
                print(f"Evaluating video {i+1}/{len(video_details)}: {detail['Video Title'][:50]}...")
                scores = evaluate_healthcare_video(
                    detail['Transcript'], 
                    detail['Video ID'], 
                    provider_name=args.provider,
                    api_key=ai_api_key,
                    model=args.model
                )
                detail.update(scores)
        
        if args.no_transcript:
            for detail in video_details:
                detail.pop('Transcript', None)
        
        if args.csv or args.output.endswith('.csv'):
            filename = save_to_csv(video_details, args.output if args.output.endswith('.csv') else 'healthcare_video_analysis.csv')
        else:
            filename = save_to_excel(video_details, args.output)
        
        print(f"Analysis complete! Results saved to {filename}")
        
        # Print summary
        df = pd.DataFrame(video_details)
        print(f"\nSummary:")
        print(f"Total videos analyzed: {len(df)}")
        if 'Views' in df.columns:
            print(f"Average views: {df['Views'].mean():,.0f}")
        if 'DISCERN Score' in df.columns and not args.no_ai:
            avg_discern = df['DISCERN Score'].mean()
            if avg_discern:
                print(f"Average DISCERN Score: {avg_discern:.1f}")
        
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("Please check your API keys and try again.")

if __name__ == "__main__":
    main() 