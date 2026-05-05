import spacy
import dateparser
from datetime import datetime

nlp = None

def get_nlp():
    global nlp
    if nlp is None:
        print("Loading AI Model...")
        nlp = spacy.load("en_core_web_sm")
    return nlp


def parse_message(user_input):
    doc = get_nlp()(user_input.lower())

    extracted_data = {
        "intent": "unknown",
        "task_title": None,
        "task_id": None,
        "due_date": None
    }

    lemmas = [token.lemma_ for token in doc]

    # First, determine the intent
    intent = "unknown"  # Define intent variable BEFORE using it
    
    # ADD TASK
    if set(lemmas) & {"add", "remind", "create"}:
        intent = "add_task"

        date_words = set()

        # First try full sentence (stronger)
        parsed_date = dateparser.parse(
            user_input,
            settings={
                "PREFER_DATES_FROM": "future",
                "RELATIVE_BASE": datetime.now()
            }
        )

        if parsed_date:
            extracted_data["due_date"] = parsed_date.strftime("%Y-%m-%d %H:%M")

        # Then use entities only for cleanup
        for ent in doc.ents:
            if ent.label_ in ("DATE", "TIME"):
                for word in ent.text.lower().split():
                    date_words.add(word)

        date_words.update([
            "today", "tomorrow", "tonight", "next",
            "this", "in", "am", "pm"
        ])

        filler_words = {
            "add", "remind", "me", "to", "create", "a", "task",
            "please", "could", "you", "for", "at", "by", "on", "my", "list"
        }

        task_words = [
            token.text for token in doc
            if token.text.lower() not in filler_words
            and token.text.lower() not in date_words
            and not token.is_punct
        ]

        if task_words:
            extracted_data["task_title"] = " ".join(task_words).strip().capitalize()

    # TODAY
    elif "today" in lemmas:
        intent = "tasks_today"

    # SHOW TASKS
    elif set(lemmas) & {"show", "list"}:
        intent = "show_tasks"

    # COMPLETE TASK
    elif set(lemmas) & {"complete", "finish", "done"}:
        intent = "complete_task"

        for token in doc:
            if token.like_num:
                extracted_data["task_id"] = int(token.text)
                break

    # DELETE TASK
    elif set(lemmas) & {"delete", "remove", "cancel"}:
        intent = "delete_task"

        for token in doc:
            if token.like_num:
                extracted_data["task_id"] = int(token.text)
                break
    
    # Set the intent in the extracted data
    extracted_data["intent"] = intent
    
    # NOW we can check if we need fallback title extraction
    if intent == "add_task" and not extracted_data["task_title"]:
        extracted_data["task_title"] = _extract_task_title_fallback(doc, user_input)

    return extracted_data


def _extract_task_title_fallback(doc, user_input):
    """Fallback method to extract task title from user input"""
    # Remove common prefixes
    prefixes = [
        "add", "create", "remind me to", "remind me", "please", "could you",
        "can you", "i need to", "i want to", "i have to"
    ]
    
    cleaned_input = user_input.lower().strip()
    for prefix in prefixes:
        if cleaned_input.startswith(prefix):
            cleaned_input = cleaned_input[len(prefix):].strip()
            break  # Only remove the first matching prefix
    
    # Remove common suffixes
    suffixes = [
        "to my list", "to my task", "to my tasks", "please", "thanks", "thank you"
    ]
    for suffix in suffixes:
        if cleaned_input.endswith(suffix):
            cleaned_input = cleaned_input[:-len(suffix)].strip()
            break  # Only remove the first matching suffix
    
    # If we have something meaningful left, use it as the title
    if cleaned_input and len(cleaned_input) > 1:
        return cleaned_input.capitalize()
    
    return None