import pandas as pd
import re
from pathlib import Path



ROOT_DIR = Path(__file__).resolve().parent.parent

def load_and_preprocess_data(input_path=ROOT_DIR / 'data/raw/student_feedback_data.xlsx', 
                             output_path=ROOT_DIR / 'data/processed/cleaned_feedback_data.csv'):
    try:
        print(f"Loading data from {input_path}")
        # Load data
        data = pd.read_excel(input_path)
        print("Data loaded successfully")

        # Drop missing feedback comments
        data.dropna(subset=['Comments/Feedback'], inplace=True)
        print("Dropped rows with missing feedback comments")
        
        # Ensure ratings are within a standard range (1-5)
        data = data[(data['Overall Course Rating'].between(1, 5)) & 
                    (data['Instructor Rating'].between(1, 5))]
        print("Filtered ratings to standard range")

        # Clean and preprocess feedback text
        def clean_text(text):
            text = re.sub(r'[^\w\s]', '', text)  # Remove punctuation
            text = re.sub(r'\s+', ' ', text)     # Remove extra whitespace
            return text.strip().lower()          # Convert to lowercase and strip

        data['Comments/Feedback'] = data['Comments/Feedback'].apply(clean_text)
        print("Cleaned feedback text")

        # Save cleaned data
        data.to_csv(output_path, index=False)
        print(f"Data saved to {output_path}")

        return data
    except Exception as e:
        print(f"Error occurred: {e}")

# Run the function if this file is executed directly
if __name__ == "__main__":
    load_and_preprocess_data()
