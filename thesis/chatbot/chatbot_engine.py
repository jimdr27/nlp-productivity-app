import spacy


print("Loading AI Model (this takes a second)...")
nlp = spacy.load("en_core_web_sm")
print("Model loaded successfully!")

def parse_message(user_input):
    """
    Takes raw user text, processes it with spaCy, and returns a dictionary 
    containing the user's intent and any extracted data (like task titles or IDs).
    """
    
    doc = nlp(user_input.lower())
    
    
    extracted_data = {
        "intent": "unknown",
        "task_title": None,
        "task_id": None
    }
    
    
    lemmas = [token.lemma_ for token in doc]
    
    
    if "add" in lemmas or "remind" in lemmas or "create" in lemmas:
        extracted_data["intent"] = "add_task"
        
        
        filler_words = ["add", "remind", "me", "to", "create", "a", "task", "please", "could", "you"]
        
        
        task_words = [token.text for token in doc if token.text not in filler_words]
        
        if task_words:
            
            extracted_data["task_title"] = " ".join(task_words).capitalize()

    
    elif "show" in lemmas or "list" in lemmas or "what" in lemmas:
        extracted_data["intent"] = "show_tasks"
        
    
    elif "complete" in lemmas or "finish" in lemmas or "done" in lemmas:
        extracted_data["intent"] = "complete_task"
        
       
        for token in doc:
            if token.pos_ == "NUM" or token.like_num:
                extracted_data["task_id"] = token.text
                break 

    return extracted_data


if __name__ == "__main__":
    test_sentences = [
        "Please add buy milk to my list",
        "Could you remind me to call mom?",
        "Show me my tasks",
        "I just finished task 2"
    ]
    
    print("\n--- Testing the NLP Engine ---")
    for sentence in test_sentences:
        print(f"\nUser: '{sentence}'")
        result = parse_message(sentence)
        print(f"Bot understood: {result}")