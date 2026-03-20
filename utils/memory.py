import json
import os
from datetime import datetime

MEMORY_FILE = "memory_store.json"


def default_memory():
    return {
        "user_profile": {
            "name": "Student",
            "preferred_style": "simple",
            "preferred_pace": "medium"
        },
        "weak_topics": [],
        "strong_topics": [],
        "mistakes": [],
        "recent_sessions": [],
        "topic_confidence": {},
        "quiz_history": [],
        "last_topic": "",
        "recommended_next": "",
        "last_updated": ""
    }


def load_memory():
    if not os.path.exists(MEMORY_FILE):
        return default_memory()

    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)
            base = default_memory()
            base.update(data)
            if "user_profile" in data:
                base["user_profile"].update(data["user_profile"])
            return base
    except (json.JSONDecodeError, FileNotFoundError):
        return default_memory()


def save_memory(memory):
    memory["last_updated"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(MEMORY_FILE, "w", encoding="utf-8") as file:
        json.dump(memory, file, indent=4)


def reset_memory():
    save_memory(default_memory())


def add_unique_item(lst, item):
    item = item.strip()
    if item and item not in lst:
        lst.append(item)


def detect_topic(message):
    text = message.lower()
    topic_keywords = [
        "chemical bonding", "chemistry", "trigonometry", "algebra", "geometry",
        "calculus", "physics", "biology", "programming", "c language", "python",
        "loops", "functions", "arrays", "pointers", "recursion", "integrals"
    ]

    for topic in topic_keywords:
        if topic in text:
            return topic
    return "general studies"


def update_confidence(memory, topic, delta):
    if "topic_confidence" not in memory:
        memory["topic_confidence"] = {}

    current = memory["topic_confidence"].get(topic, 50)
    new_score = max(0, min(100, current + delta))
    memory["topic_confidence"][topic] = new_score

    if "weak_topics" not in memory:
        memory["weak_topics"] = []
    if "strong_topics" not in memory:
        memory["strong_topics"] = []

    if new_score < 65:
        if topic not in memory["weak_topics"]:
            memory["weak_topics"].append(topic)
        if topic in memory["strong_topics"]:
            memory["strong_topics"].remove(topic)

    elif new_score >= 80:
        if topic not in memory["strong_topics"]:
            memory["strong_topics"].append(topic)
        if topic in memory["weak_topics"]:
            memory["weak_topics"].remove(topic)

    else:
        if topic in memory["weak_topics"]:
            memory["weak_topics"].remove(topic)
        if topic in memory["strong_topics"]:
            memory["strong_topics"].remove(topic)


def update_memory_from_message(message, memory):
    text = message.lower()
    topic = detect_topic(message)
    memory["last_topic"] = topic

    add_unique_item(memory["recent_sessions"], message)

    if "step by step" in text:
        memory["user_profile"]["preferred_style"] = "step-by-step"
    elif "simple" in text or "easy" in text:
        memory["user_profile"]["preferred_style"] = "simple"

    if "slow" in text:
        memory["user_profile"]["preferred_pace"] = "slow"
    elif "fast" in text:
        memory["user_profile"]["preferred_pace"] = "fast"

    confused_signals = [
        "confused", "don't understand", "did not understand",
        "wrong", "hard", "difficult", "not sure"
    ]

    if any(signal in text for signal in confused_signals):
        add_unique_item(memory["mistakes"], message)
        update_confidence(memory, topic, -12)
    else:
        update_confidence(memory, topic, 4)

    memory["recent_sessions"] = memory["recent_sessions"][-8:]
    memory["mistakes"] = memory["mistakes"][-8:]

    if memory["weak_topics"]:
        memory["recommended_next"] = memory["weak_topics"][0]
    else:
        memory["recommended_next"] = memory["last_topic"]
