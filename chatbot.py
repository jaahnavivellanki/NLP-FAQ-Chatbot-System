import json
import numpy as np
import random
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from preprocess import preprocess

# Configuration
FAQ_FILE_PATH = 'data/faqs.json'
SIMILARITY_THRESHOLD = 0.2  

def load_faqs(filepath):
    """
    Loads FAQs from a JSON file.
    Expects a list of dictionaries, each with 'question' and 'answer' keys.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Warning: The file {filepath} was not found.")
        return []
    except json.JSONDecodeError:
        print(f"Warning: The file {filepath} contains invalid JSON.")
        return []


# Initialization 
faqs = load_faqs(FAQ_FILE_PATH)

questions = [item.get('question', '') for item in faqs]
answers = [item.get('answer', '') for item in faqs]

preprocessed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))

if preprocessed_questions:
    tfidf_matrix = vectorizer.fit_transform(preprocessed_questions)
else:
    tfidf_matrix = None


def get_response(user_question):
    """
    Finds the most similar FAQ question to the user's input and returns the corresponding answer.
    
    Args:
        user_question (str): The question asked by the user.
        
    Returns:
        tuple: The matched answer and the confidence score (float).
    """
    if tfidf_matrix is None or not faqs:
        return "Sorry, I cannot answer questions right now. FAQ data is missing.", 0.0
        
    cleaned_user_question = preprocess(user_question)
    

    user_vector = vectorizer.transform([cleaned_user_question])
    
    similarities = cosine_similarity(user_vector, tfidf_matrix)
    

    similarity_scores = similarities.flatten()
    
    best_match_index = np.argmax(similarity_scores)
    best_score = similarity_scores[best_match_index]
    
    if best_score >= SIMILARITY_THRESHOLD:
        # Match found! Return the corresponding answer
        return answers[best_match_index], float(best_score)
    else:
        # Score is too low, meaning the question wasn't a close enough match
        fallback_responses = [
            "I’m not fully sure about that. Could you provide a bit more context?",
            "I couldn't find a matching FAQ. Could you rephrase your question?",
            "I don't have a confident answer for that at the moment. Would you mind asking in a different way?",
            "I'm sorry, I couldn't find an exact match for your inquiry in our policies."
        ]
        return random.choice(fallback_responses), float(best_score)

# Testing block
if __name__ == "__main__":
    print("Chatbot is ready! Type 'quit' or 'exit' to stop.")
    while True:
        user_input = input("\nYou: ")
        if user_input.lower() in ['quit', 'exit']:
            print("Chatbot: Goodbye!")
            break
            
        response, score = get_response(user_input)
        print(f"Chatbot: {response} (Confidence: {score*100:.1f}%)")
