import pandas as pd
import re
from pathlib import Path



def validate_data(data: pd.DataFrame) -> pd.DataFrame:
    # Check if essential columns are present
    required_columns = ['Comments/Feedback', 'Overall Course Rating', 'Instructor Rating']
    missing_columns = [col for col in required_columns if col not in data.columns]
    if missing_columns:
        raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")

    # Ensure 'Comments/Feedback' is of type string
    data['Comments/Feedback'] = data['Comments/Feedback'].astype(str)

    # Check that ratings are within acceptable ranges
    for column in ['Overall Course Rating', 'Instructor Rating']:
        if not pd.api.types.is_numeric_dtype(data[column]):
            raise ValueError(f"{column} must be numeric")
        if not data[column].between(1, 5).all():
            raise ValueError(f"{column} must be between 1 and 5")

    return data


def load_and_preprocess_data(input_path=Path('data/raw/student_feedback_data.xlsx')):
    print("Loading and preprocessing data...")
    data = pd.read_excel(input_path)
    data = validate_data(data)
    data.dropna(subset=['Comments/Feedback'], inplace=True)
    data = data[(data['Overall Course Rating'].between(1, 5)) & 
                (data['Instructor Rating'].between(1, 5))]

    data['Comments/Feedback'] = data['Comments/Feedback'].apply(
        lambda x: re.sub(r'[^\w\s]', '', x).strip().lower()
    )
    print("Data ingestion and preprocessing completed.")
    return data
