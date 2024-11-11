import openai
from config import OPENAI_API_KEY

# Set up the API key
openai.api_key = OPENAI_API_KEY
client = openai  # Alias the openai module as client for consistency

def summarize_feedback(data):
    print("Generating feedback summaries...")

    def generate_summary(text):
        try:
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": f"Summarize the key points in this feedback: {text}"}],
                max_tokens=50,
                temperature=0.5
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            print(f"Error in generate_summary: {e}")
            return "Error generating summary"

    # Apply the generate_summary function to the 'Comments/Feedback' column
    data['Summary'] = data['Comments/Feedback'].apply(generate_summary)
    print("Feedback summarization completed.")
    return data
