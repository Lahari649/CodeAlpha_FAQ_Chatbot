import json
import re
import nltk

from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class FAQChatbot:

    def __init__(self, faq_file="faqs.json"):

        self.download_nltk_data()

        with open(faq_file, "r", encoding="utf-8") as file:
            self.faqs = json.load(file)

        self.stop_words = set(stopwords.words("english"))
        self.lemmatizer = WordNetLemmatizer()

        self.questions = [
            faq["question"]
            for faq in self.faqs
        ]

        self.vectorizer = TfidfVectorizer(
            tokenizer=self.tokenize,
            token_pattern=None,
            ngram_range=(1, 2)
        )

        self.question_vectors = self.vectorizer.fit_transform(
            self.questions
        )

    def download_nltk_data(self):

        resources = {
            "corpora/stopwords": "stopwords",
            "corpora/wordnet": "wordnet",
            "corpora/omw-1.4": "omw-1.4"
        }

        for path, package in resources.items():

            try:
                nltk.data.find(path)

            except LookupError:
                nltk.download(package, quiet=True)

    def tokenize(self, text):

        text = text.lower()

        words = re.findall(
            r"\b[a-zA-Z]+\b",
            text
        )

        words = [
            self.lemmatizer.lemmatize(word)
            for word in words
            if word not in self.stop_words
        ]

        return words

    def get_response(self, user_question):

        if not user_question.strip():

            return {
                "answer": "Please enter a question.",
                "confidence": 0.0,
                "category": "General"
            }

        user_vector = self.vectorizer.transform(
            [user_question]
        )

        similarity_scores = cosine_similarity(
            user_vector,
            self.question_vectors
        )[0]

        best_index = similarity_scores.argmax()

        confidence = float(
            similarity_scores[best_index]
        )

        threshold = 0.25

        if confidence < threshold:

            return {
                "answer": (
                    "I'm sorry, I couldn't find a suitable "
                    "answer to your question. Please try "
                    "asking your question in a different way "
                    "or contact customer support."
                ),
                "confidence": confidence,
                "category": "Unknown"
            }

        best_faq = self.faqs[best_index]

        return {
            "answer": best_faq["answer"],
            "confidence": confidence,
            "category": best_faq["category"]
        }