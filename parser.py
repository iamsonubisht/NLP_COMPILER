import spacy

def extract_info(text):
    """Extracts numbers and operation from the input text."""
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text.lower())

    numbers = [int(token.text) for token in doc if token.like_num]
    operations = {
        "add": "+", "plus": "+", "sum": "+", 
        "subtract": "-", "minus": "-", "difference": "-",
        "multiply": "", "times": "", "product": "*",
        "divide": "/", "over": "/", "quotient": "/"
    }

    operation = None
    for token in doc:
        if token.text in operations:
            operation = operations[token.text]
            break

    # 🛠 Ensure function never returns None
    if len(numbers) < 2 or operation is None:
        return [], None  # Fix: Return empty list & None instead of NoneType

    return numbers, operation
