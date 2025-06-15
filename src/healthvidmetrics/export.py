import pandas as pd

def save_to_excel(data, filename='healthcare_video_analysis.xlsx'):
    df = pd.DataFrame(data)
    df.to_excel(filename, index=False)
    return filename

def save_to_csv(data, filename='healthcare_video_analysis.csv'):
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)
    return filename 