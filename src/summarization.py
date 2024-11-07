import openai
import pandas as pd
from config import OPENAI_API_KEY
from pathlib import Path

openai.api_key = OPENAI_API_KEY

ROOT_DIR = Path(__file__).resolve().parent.parent

def summarize_feedback(input_path=ROOT_DIR / 'data/processed/topic_feedback_data.csv', 
                       output_path=ROOT_DIR / 'data/processed/summarized_feedback_data.csv'):
    print(f"Loading data from {input_path}")
    data = pd.read_csv(input_path)
    print("Data loaded successfully")

    def generate_summary(text):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant that summarizes feedback text."},
                    {"role": "user", "content": f"Summarize the key points in this feedback:\n\n{text}"}
                ],
                max_tokens=50,
                temperature=0.5
            )
            summary = response.choices[0].message['content'].strip()
            return summary
        except Exception as e:
            print(f"Error generating summary for text: {text[:50]}... Error: {e}")
            return "Error in summary generation"

    print("Generating summaries for feedback comments...")
    data['Summary'] = data['Comments/Feedback'].apply(generate_summary)
    print("Summary generation complete")

    data.to_csv(output_path, index=False)
    print(f"Summarized data saved to {output_path}")
    return data

# Run the function if this file is executed directly
if __name__ == "__main__":
    summarize_feedback()
