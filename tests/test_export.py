import os
from src.healthvidmetrics.export import save_to_excel, save_to_csv

def test_save_to_excel_and_csv(tmp_path):
    data = [
        {"Video ID": "abc123", "Views": 100, "Transcript": "hello"},
        {"Video ID": "def456", "Views": 200, "Transcript": "world"}
    ]
    excel_path = tmp_path / "test.xlsx"
    csv_path = tmp_path / "test.csv"
    save_to_excel(data, str(excel_path))
    save_to_csv(data, str(csv_path))
    assert os.path.exists(excel_path)
    assert os.path.exists(csv_path) 