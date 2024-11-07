import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def perform_sentiment_analysis(data):
    print("Performing sentiment analysis...")

    def get_sentiment(text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Classify the sentiment of this feedback: {text}"}]
        )
        return response.choices[0].message['content'].strip()

    data['Sentiment'] = data['Comments/Feedback'].apply(get_sentiment)
    print("Sentiment analysis completed.")
    return data
