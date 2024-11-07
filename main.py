from src.data_ingestion import load_and_preprocess_data
from src.sentiment_analysis import perform_sentiment_analysis
from src.topic_modeling import extract_topics
from src.summarization import summarize_feedback
from src.recommendation import generate_recommendations


def main():
    # Step 1: Load and preprocess data
    data = load_and_preprocess_data()
    
    # Step 2: Perform sentiment analysis
    data_with_sentiment = perform_sentiment_analysis()
    
    # Step 3: Extract topics
    data_with_topics = extract_topics()
    
    # Step 4: Summarize feedback
    summarized_data = summarize_feedback()
    
    # Step 5: Generate recommendations
    final_data = generate_recommendations()

if __name__ == "__main__":
    main()
