import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def generate_dynamic_recommendation(feedback_text, sentiment, topic):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": f"Provide a recommendation based on feedback: {feedback_text}"}],
        max_tokens=50
    )
    return response.choices[0].message['content'].strip()

def generate_recommendations(data):
    print("Generating recommendations...")

    def improvement_suggestion(row):
        if row['Sentiment'] == 'Negative' and 'workload' in row['Topic'].lower():
            return "Consider reducing workload."
        elif row['Sentiment'] == 'Negative':
            return generate_dynamic_recommendation(row['Comments/Feedback'], row['Sentiment'], row['Topic'])
        return "No specific recommendation."

    data['Recommendation'] = data.apply(improvement_suggestion, axis=1)
    print("Recommendation generation completed.")
    return data
