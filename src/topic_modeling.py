import pandas as pd
from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
import nltk
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def preprocess(text):
    tokens = [word for word in text.lower().split() if word.isalpha() and word not in stop_words]
    return tokens

def extract_topics(input_path=ROOT_DIR / 'data/processed/sentiment_feedback_data.csv', 
                   output_path=ROOT_DIR / 'data/processed/topic_feedback_data.csv', num_topics=3):
    print(f"Loading data from {input_path}")
    data = pd.read_csv(input_path)
    print("Data loaded successfully")

    print("Preprocessing feedback text...")
    data['Processed_Feedback'] = data['Comments/Feedback'].apply(preprocess)
    print("Preprocessing complete")

    print("Creating dictionary and corpus for LDA model...")
    dictionary = corpora.Dictionary(data['Processed_Feedback'])
    corpus = [dictionary.doc2bow(text) for text in data['Processed_Feedback']]
    print("Dictionary and corpus created")

    print("Training LDA model...")
    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=5)  # Reduce passes for quicker testing
    print("LDA model training complete")

    def get_topic(text):
        bow = dictionary.doc2bow(text)
        topics = lda_model.get_document_topics(bow)
        main_topic = sorted(topics, key=lambda x: x[1], reverse=True)[0]
        return main_topic[0]

    print("Extracting main topics for each feedback comment...")
    data['Topic'] = data['Processed_Feedback'].apply(get_topic)
    print("Topic extraction complete")

    print(f"Saving data to {output_path}")
    data.to_csv(output_path, index=False)
    print(f"Topic data saved to {output_path}")
    return data

# Run extract_topics if this file is executed directly
if __name__ == "__main__":
    extract_topics()
