from pathlib import Path
from fastapi import UploadFile
import pandas as pd
from src.data_ingestion import load_and_preprocess_data
from src.sentiment_analysis import perform_sentiment_analysis
from src.topic_modeling import extract_topics
from src.summarization import summarize_feedback
from src.recommendation import generate_recommendations

# Directory for storing processed files
DATA_DIR = Path("data/processed")
DATA_DIR.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist

# 1. Save Uploaded File
def save_file(file: UploadFile) -> Path:
    """Save the uploaded file to the data directory."""
    filepath = DATA_DIR / file.filename
    with open(filepath, "wb") as f:
        f.write(file.file.read())
    return filepath

# 2. Run Analysis Pipeline
def run_analysis_pipeline(filepath: Path) -> Path:
    """Run the feedback analysis pipeline on the uploaded file."""
    # Step 1: Data ingestion and preprocessing
    data = load_and_preprocess_data(filepath)
    print("After data ingestion:", type(data))
    if data is None:
        raise ValueError("Data preprocessing returned None")

    # Step 2: Perform sentiment analysis
    data = perform_sentiment_analysis(data)
    print("After sentiment analysis:", type(data))
    if data is None:
        raise ValueError("Sentiment analysis returned None")

    # Step 3: Extract topics
    data = extract_topics(data)
    print("After topic extraction:", type(data))
    if data is None:
        raise ValueError("Topic extraction returned None")

    # Step 4: Summarize feedback
    data = summarize_feedback(data)
    print("After summarization:", type(data))
    if data is None:
        raise ValueError("Summarization returned None")

    # Step 5: Generate recommendations
    final_data = generate_recommendations(data)
    print("After recommendations:", type(final_data))
    if final_data is None:
        raise ValueError("Recommendation generation returned None")


    # Save the processed file
    result_filepath = DATA_DIR / f"processed_{filepath.stem}.csv"
    final_data.to_csv(result_filepath, index=False)
    return result_filepath

# 3. Get Processed File Path
def get_processed_file_path(filename: str) -> Path:
    """Get the path for a processed file by filename."""
    return DATA_DIR / filename






