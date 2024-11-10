from src.data_ingestion import load_and_preprocess_data
from src.sentiment_analysis import perform_sentiment_analysis
from src.topic_modeling import extract_topics
from src.summarization import summarize_feedback
from src.recommendation import generate_recommendations
from pathlib import Path

def main():
    print("Stage 1: Data Ingestion and Preprocessing")
    data = load_and_preprocess_data()
    print("Stage 1 completed.\n")

    print("Stage 2: Sentiment Analysis")
    data = perform_sentiment_analysis(data)
    print("Stage 2 completed.\n")

    print("Stage 3: Topic Extraction")
    data = extract_topics(data)
    print("Stage 3 completed.\n")

    print("Stage 4: Feedback Summarization")
    data = summarize_feedback(data)
    print("Stage 4 completed.\n")

    print("Stage 5: Recommendation Generation")
    final_data = generate_recommendations(data)
    print("Stage 5 completed.\n")

    # Save final data
    output_path = Path('data/processed/final_feedback_data.csv')
    final_data.to_csv(output_path, index=False)
    print(f"Final data saved to {output_path}")

if __name__ == "__main__":
    main()
