from gensim import corpora
from gensim.models import LdaModel
from nltk.corpus import stopwords
import nltk

nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

def extract_topics(data, num_topics=3):
    print("Starting topic extraction...")

    data['Processed_Feedback'] = data['Comments/Feedback'].apply(
        lambda text: [word for word in text.lower().split() if word.isalpha() and word not in stop_words]
    )

    dictionary = corpora.Dictionary(data['Processed_Feedback'])
    corpus = [dictionary.doc2bow(text) for text in data['Processed_Feedback']]

    lda_model = LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=5)
    data['Topic'] = data['Processed_Feedback'].apply(
        lambda text: sorted(lda_model.get_document_topics(dictionary.doc2bow(text)), key=lambda x: x[1], reverse=True)[0][0]
    )

    print("Topic extraction completed.")
    return data
