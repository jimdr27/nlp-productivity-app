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

    #  ADD TASK
    if set(lemmas) & {"add", "remind", "create"}:
        extracted_data["intent"] = "add_task"

        date_words = set()

        for ent in doc.ents:
            if ent.label_ in ("DATE", "TIME"):
                parsed_date = dateparser.parse(
                    ent.text,
                    settings={
                        "PREFER_DATES_FROM": "future",
                        "RELATIVE_BASE": datetime.now()
                    }
                )

                if parsed_date and not extracted_data["due_date"]:
                    extracted_data["due_date"] = parsed_date.strftime("%Y-%m-%d %H:%M")

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

    #  TODAY
    elif "today" in lemmas and set(lemmas) & {"show", "list"}:
        extracted_data["intent"] = "tasks_today"

    #  SHOW TASKS
    elif set(lemmas) & {"show", "list"}:
        extracted_data["intent"] = "show_tasks"

    #  COMPLETE TASK
    elif set(lemmas) & {"complete", "finish", "done"}:
        extracted_data["intent"] = "complete_task"

        for token in doc:
            if token.like_num:
                extracted_data["task_id"] = int(token.text)
                break

    #  DELETE TASK
    elif set(lemmas) & {"delete", "remove", "cancel"}:
        extracted_data["intent"] = "delete_task"

        for token in doc:
            if token.like_num:
                extracted_data["task_id"] = int(token.text)
                break

    return extracted_data
