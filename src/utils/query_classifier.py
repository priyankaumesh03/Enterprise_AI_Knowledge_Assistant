import re


def classify_query(user_query):

    # Convert input to lowercase and remove extra spaces
    query = user_query.lower().strip()

    # Remove punctuation for easier matching
    query = re.sub(r"[^\w\s]", "", query)
    query = re.sub(r"\s+", " ", query)

    # 1. Greeting detection
    greetings = [
    "hi",
    "hello",
    "hey",
    "good morning",
    "good afternoon",
    "good evening",
    "good night",
    "hi there",
    "hello there",
    "hi good morning",
    "hi good afternoon",
    "hi good evening",
    "hello good morning",
    "hello good afternoon",
    "hello good evening",
    "hey good morning",
    "hey good afternoon",
    "hey good evening"
]
    if query in greetings:
        return "greeting"

    # 2. Appreciation detection
    appreciation = [
        "thanks",
        "thank you",
        "thanks a lot",
        "thank you so much",
        "much appreciated",
        "appreciate it"
    ]

    if query in appreciation:
        return "appreciation"

    # 3. General conversation detection
    general_conversation = [
        "how are you",
        "how are you doing",
        "whats up",
        "what is up",
        "who are you",
        "what can you do",
        "how is your day"
    ]

    if query in general_conversation:
        return "general_conversation"

    # 4. Default: Treat as a knowledge-related question
    return "knowledge"
if __name__ == "__main__":

    test_queries = [
        "Hi",
        "Good afternoon",
        "Thank you",
        "How are you?",
        "Who are you?",
        "How many annual leaves do employees get?",
        "How do I reset my password?"
    ]

    for query in test_queries:
        intent = classify_query(query)
        print(f"Query: {query} | Intent: {intent}")