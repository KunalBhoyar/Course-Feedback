import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

def summarize_feedback(data):
    print("Generating feedback summaries...")

    def generate_summary(text):
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": f"Summarize the key points in this feedback: {text}"}],
            max_tokens=50
        )
        return response.choices[0].message['content'].strip()

    data['Summary'] = data['Comments/Feedback'].apply(generate_summary)
    print("Feedback summarization completed.")
    return data
