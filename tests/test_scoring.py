from src.healthvidmetrics.scoring import evaluate_healthcare_video

def test_evaluate_healthcare_video_no_transcript():
    result = evaluate_healthcare_video(None, "dummy_id")
    assert result["DISCERN Score"] is None
    assert result["Global Quality Score"] is None
    assert result["JAMA Criteria Score"] is None
    assert "No transcript" in result["Evaluation Notes"] 