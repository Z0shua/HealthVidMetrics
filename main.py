import streamlit as st
import os
import pandas as pd
from src.healthvidmetrics.config import load_api_keys
from src.healthvidmetrics.youtube_api import extract_video_id, get_video_details
from src.healthvidmetrics.scoring import evaluate_healthcare_video
from src.healthvidmetrics.export import save_to_excel

def main():
    st.set_page_config(
        page_title="HealthVidMetrics - Healthcare Video Quality Analyzer",
        page_icon="🏥",
        layout="wide"
    )
    st.title("🏥 HealthVidMetrics")
    st.subheader("Healthcare Video Quality Analysis Tool")
    st.markdown("---")
    st.sidebar.header("Configuration")
    # API Keys
    env_youtube_api_key, env_openai_api_key = load_api_keys()
    youtube_api_key = st.sidebar.text_input(
        "YouTube API Key",
        type="password",
        value=env_youtube_api_key or '',
        help="Enter your YouTube Data API v3 key"
    )
    openai_api_key = st.sidebar.text_input(
        "OpenAI API Key",
        type="password",
        value=env_openai_api_key or '',
        help="Enter your OpenAI API key"
    )
    st.header("Video Analysis")
    input_method = st.radio(
        "Choose input method:",
        ["Single Video URL", "Multiple Video URLs", "Upload CSV File"]
    )
    video_urls = []
    if input_method == "Single Video URL":
        url = st.text_input("Enter YouTube Video URL:")
        if url:
            video_urls = [url]
    elif input_method == "Multiple Video URLs":
        urls_text = st.text_area(
            "Enter YouTube Video URLs (one per line):",
            height=150,
            placeholder="https://www.youtube.com/watch?v=example1\nhttps://www.youtube.com/watch?v=example2"
        )
        if urls_text:
            video_urls = [url.strip() for url in urls_text.split('\n') if url.strip()]
    elif input_method == "Upload CSV File":
        uploaded_file = st.file_uploader("Upload CSV file with video URLs", type=['csv'])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            if 'url' in df.columns:
                video_urls = df['url'].tolist()
            else:
                st.error("CSV file must contain a 'url' column")
    st.subheader("Analysis Options")
    include_transcript = st.checkbox("Include video transcripts", value=True)
    include_ai_evaluation = st.checkbox("Include AI-powered quality evaluation", value=True)
    if st.button("🚀 Start Analysis", type="primary"):
        if not video_urls:
            st.error("Please provide at least one video URL")
            return
        if not youtube_api_key:
            st.error("Please provide a YouTube API key")
            return
        if include_ai_evaluation and not openai_api_key:
            st.error("Please provide an OpenAI API key for AI evaluation")
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
            st.warning(f"Invalid URLs found: {invalid_urls}")
        if not video_ids:
            st.error("No valid video IDs found")
            return
        progress_bar = st.progress(0)
        status_text = st.empty()
        try:
            from googleapiclient.discovery import build
            youtube = build('youtube', 'v3', developerKey=youtube_api_key)
            status_text.text("Fetching video details...")
            video_details = get_video_details(youtube, video_ids, include_transcript=include_transcript)
            progress_bar.progress(30)
            if include_ai_evaluation:
                status_text.text("Evaluating video quality with AI...")
                for i, detail in enumerate(video_details):
                    scores = evaluate_healthcare_video(detail['Transcript'], detail['Video ID'], openai_api_key=openai_api_key)
                    detail.update(scores)
                    progress_bar.progress(30 + (i + 1) * 60 / len(video_details))
            if not include_transcript:
                for detail in video_details:
                    detail.pop('Transcript', None)
            progress_bar.progress(100)
            status_text.text("Analysis complete!")
            st.subheader("📊 Analysis Results")
            df = pd.DataFrame(video_details)
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total Videos", len(df))
            with col2:
                avg_views = df['Views'].mean() if 'Views' in df.columns else 0
                st.metric("Average Views", f"{avg_views:,.0f}")
            with col3:
                if 'DISCERN Score' in df.columns:
                    avg_discern = df['DISCERN Score'].mean()
                    st.metric("Avg DISCERN Score", f"{avg_discern:.1f}" if avg_discern else "N/A")
            with col4:
                if 'Global Quality Score' in df.columns:
                    avg_quality = df['Global Quality Score'].mean()
                    st.metric("Avg Quality Score", f"{avg_quality:.1f}" if avg_quality else "N/A")
            st.dataframe(df, use_container_width=True)
            st.subheader("📥 Download Results")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("Download Excel File"):
                    filename = save_to_excel(video_details)
                    with open(filename, 'rb') as f:
                        st.download_button(
                            label="Click to download Excel file",
                            data=f.read(),
                            file_name=filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                        )
            with col2:
                csv = df.to_csv(index=False)
                st.download_button(
                    label="Download CSV File",
                    data=csv,
                    file_name="healthcare_video_analysis.csv",
                    mime="text/csv"
                )
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            st.error("Please check your API keys and try again.")
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
        <p>HealthVidMetrics - Healthcare Video Quality Analysis Tool</p>
        <p>Uses DISCERN, Global Quality Score, and JAMA Benchmark Criteria</p>
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main() 