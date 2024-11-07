import pandas as pd
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

def generate_recommendations(input_path=ROOT_DIR / 'data/processed/summarized_feedback_data.csv', 
                             output_path=ROOT_DIR / 'data/processed/recommendations_feedback_data.csv'):
    print(f"Loading data from {input_path}")
    data = pd.read_csv(input_path)
    print("Data loaded successfully")

    # Ensure required columns are present
    if 'Sentiment' not in data.columns or 'Topic' not in data.columns:
        print("Error: Required columns 'Sentiment' or 'Topic' not found in the input data.")
        return None

    def improvement_suggestion(row):
        # Convert 'Topic' to lowercase for case-insensitive matching
        topic = row['Topic'].lower() if isinstance(row['Topic'], str) else ''
        
        # Generate recommendations based on conditions
        if row['Sentiment'] == 'Negative' and 'workload' in topic:
            return "Consider reducing the workload for better engagement."
        elif row['Sentiment'] == 'Negative' and 'pace' in topic:
            return "Consider adjusting the course pace."
        else:
            return "No specific recommendation."
    
    print("Generating recommendations...")
    data['Recommendation'] = data.apply(improvement_suggestion, axis=1)
    print("Recommendation generation complete")

    # Save the data with recommendations
    data.to_csv(output_path, index=False)
    print(f"Recommendations saved to {output_path}")
    return data

# Run the function if this file is executed directly
if __name__ == "__main__":
    generate_recommendations()
