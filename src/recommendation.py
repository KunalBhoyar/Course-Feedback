import openai
import pandas as pd
from config import OPENAI_API_KEY

# Initialize OpenAI client and set API key
openai.api_key = OPENAI_API_KEY
client = openai

def generate_dynamic_recommendation(feedback_text, sentiment, topic):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Provide a recommendation based on feedback: {feedback_text}"}],
            max_tokens=50
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error in generate_dynamic_recommendation: {e}")
        return "Error generating recommendation."

def generate_recommendations(data: pd.DataFrame) -> pd.DataFrame:
    def improvement_suggestion(row):
        if row['Sentiment'] == 'Negative' and isinstance(row['Topic'], str):
            if 'workload' in row['Topic'].lower():
                return "Consider reducing the workload for better engagement."
            elif 'pace' in row['Topic'].lower():
                return "Consider adjusting the course pace."
        return "No specific recommendation."


    # Ensure 'Recommendation' column is added to the DataFrame
    data['Recommendation'] = data.apply(improvement_suggestion, axis=1)

    # Return the updated DataFrame with recommendations
    return data
