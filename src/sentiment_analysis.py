import openai
import pandas as pd
from config import OPENAI_API_KEY
from pathlib import Path

# Set up API key and root directory
openai.api_key = OPENAI_API_KEY
ROOT_DIR = Path(__file__).resolve().parent.parent

def get_sentiment(text):
    """
    Call OpenAI API to determine the sentiment of a given text.
    Returns 'Positive', 'Neutral', or 'Negative'.
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant who classifies the sentiment of feedback."},
                {"role": "user", "content": f"Classify the sentiment of this feedback as Positive, Neutral, or Negative:\n\n{text}"}
            ]
        )
        # Extract the sentiment from the response
        sentiment = response.choices[0].message['content'].strip()
        return sentiment
    except Exception as e:
        print(f"Error analyzing sentiment for text: '{text[:50]}...': {e}")
        return "Error"

def perform_sentiment_analysis(input_path=ROOT_DIR / 'data/processed/cleaned_feedback_data.csv', 
                   output_path=ROOT_DIR / 'data/processed/sentiment_feedback_data.csv'):
    """
    Load feedback data, perform sentiment analysis on each comment, 
    and save the results to a new file with added sentiment column.
    """
    try:
        print(f"Loading data from {input_path}")
        data = pd.read_csv(input_path)
        print(f"Data loaded successfully. Total rows: {len(data)}")

        # Apply the get_sentiment function to each comment
        print("Starting sentiment analysis on each feedback comment...")
        data['Sentiment'] = data['Comments/Feedback'].apply(get_sentiment)

        # Save the results
        data.to_csv(output_path, index=False)
        print(f"Sentiment analysis complete. Data with sentiments saved to {output_path}")

        return data
    except FileNotFoundError:
        print(f"Error: The input file '{input_path}' does not exist.")
    except pd.errors.EmptyDataError:
        print("Error: The input file is empty.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

# Run the function if this file is executed directly
if __name__ == "__main__":
    perform_sentiment_analysis()
