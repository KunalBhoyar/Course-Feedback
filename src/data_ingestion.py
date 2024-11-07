import pandas as pd
import re
from pathlib import Path

def load_and_preprocess_data(input_path=Path('data/raw/student_feedback_data.xlsx')):
    print("Loading and preprocessing data...")
    data = pd.read_excel(input_path)
    data.dropna(subset=['Comments/Feedback'], inplace=True)
    data = data[(data['Overall Course Rating'].between(1, 5)) & 
                (data['Instructor Rating'].between(1, 5))]

    data['Comments/Feedback'] = data['Comments/Feedback'].apply(
        lambda x: re.sub(r'[^\w\s]', '', x).strip().lower()
    )
    print("Data ingestion and preprocessing completed.")
    return data
