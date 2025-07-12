def get_semantic_response(query: str, intent: str):
    if intent == "general_summary":
        return "This dataset captures correlations between personality traits and social behaviors..."
    if intent == "error_invalid_query":
        return "Sorry, I couldn't understand your question."
    return "Processing..."
