import re
import openai

def evaluate_healthcare_video(transcript, video_id, openai_api_key=None):
    if transcript is None:
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": "No transcript available for evaluation"
        }
    if openai_api_key:
        openai.api_key = openai_api_key
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
        return {
            "DISCERN Score": None,
            "Global Quality Score": None,
            "JAMA Criteria Score": None,
            "Evaluation Notes": f"Evaluation failed: {str(e)}"
        } 