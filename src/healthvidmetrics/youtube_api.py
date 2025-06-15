import re
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
import pandas as pd

def convert_duration_to_seconds(duration):
    match = re.match(r'PT(\d+H)?(\d+M)?(\d+S)?', duration)
    hours = int(match.group(1)[:-1]) if match.group(1) else 0
    minutes = int(match.group(2)[:-1]) if match.group(2) else 0
    seconds = int(match.group(3)[:-1]) if match.group(3) else 0
    return hours * 3600 + minutes * 60 + seconds

def extract_video_id(url):
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/)([^&\n?#]+)',
        r'youtube\.com/watch\?.*v=([^&\n?#]+)'
    ]
    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None

def get_video_transcript(video_id):
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        transcript_text = " ".join([entry['text'] for entry in transcript])
        return transcript_text
    except Exception:
        return None

def get_video_details(youtube, video_ids, include_transcript=True):
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
            transcript = get_video_transcript(video_id) if include_transcript else None
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