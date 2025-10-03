from difflib import SequenceMatcher

def similarity_score(user_answer, correct_answer):
    """
    Compares the user’s answer with the correct answer and returns a similarity percentage.
    If similarity is 50% or more, the answer is considered correct.
    """
    user_answer = user_answer.lower().strip()  # Normalize user input
    correct_answer = correct_answer.lower().strip()  # Normalize correct answer

    similarity = SequenceMatcher(None, user_answer, correct_answer).ratio() * 100  # Convert to percentage
    return similarity  # Returns a value between 0 and 100