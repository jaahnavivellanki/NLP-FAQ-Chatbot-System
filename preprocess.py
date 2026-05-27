import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True) # Usually needed for newer versions of NLTK
nltk.download('stopwords', quiet=True)

def preprocess(text):
    """
    Preprocesses text for an NLP FAQ chatbot.
    
    This function takes a raw string of text and applies several cleaning steps:
    1. Converts text to lowercase.
    2. Removes punctuation.
    3. Tokenizes words (splits the sentence into individual words).
    4. Removes common English stopwords (like 'the', 'is', 'in').
    5. Joins the words back into a single string.
    
    Args:
        text (str): The input string to clean.
        
    Returns:
        str: The cleaned text.
    """
    
    # 1. Convert text to lowercase
    # This ensures that "Hello" and "hello" are treated as the same word
    text = text.lower()
    
    # 2. Remove punctuation
    # We use a regular expression (regex) here. 
    # [^\w\s] means "match anything that is NOT a word character or a space"
    # We replace those matches with an empty string (meaning we remove them)
    text = re.sub(r'[^\w\s]', '', text)
    
    # 3. Tokenize words
    # This splits the string into a list of individual words
    words = word_tokenize(text)
    
    # 4. Remove English stopwords
    # Stopwords are common words that usually don't carry much meaning for NLP tasks
    stop_words = set(stopwords.words('english'))
    
    # We create a new list containing only the words that are not in our stop_words set
    cleaned_words = []
    for word in words:
        if word not in stop_words:
            cleaned_words.append(word)
            
    # Alternatively, using a list comprehension (a more Pythonic way):
    # cleaned_words = [word for word in words if word not in stop_words]
    
    # 5. Return cleaned text as a string
    # We join the words in our list back together, separated by a single space
    cleaned_text = ' '.join(cleaned_words)
    
    return cleaned_text

# You can run this block to test the function directly
if __name__ == "__main__":
    sample = "Hello! Welcome to our FAQ chatbot. How can I help you today?"
    result = preprocess(sample)
    
    print("Original Text:", sample)
    print("Cleaned Text: ", result)
