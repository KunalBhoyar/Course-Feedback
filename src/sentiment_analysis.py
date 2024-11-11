import openai
from config import OPENAI_API_KEY

# Set up the API key
openai.api_key = OPENAI_API_KEY
client = openai  # Alias the openai module as client for consistency

def perform_sentiment_analysis(data):
    print("Performing sentiment analysis...")

    def get_sentiment(text):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Classify the sentiment of this feedback: {text}"}],
                max_tokens=10
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in get_sentiment: {e}")
            return "Error in sentiment analysis"

    # Apply the get_sentiment function to the 'Comments/Feedback' column
    data['Sentiment'] = data['Comments/Feedback'].apply(get_sentiment)
    print("Sentiment analysis completed.")
    return data
