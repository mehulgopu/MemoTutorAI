from utils.memory import detect_topic


TOPIC_KB = {
    "trigonometry": {
        "definition": "Trigonometry is the branch of mathematics that studies the relationship between angles and sides of triangles, especially right-angled triangles.",
        "steps": [
            "First, understand that trigonometry mainly deals with right triangles.",
            "Second, learn the three basic ratios: sine, cosine, and tangent.",
            "Third, connect each ratio to sides of a triangle using SOH-CAH-TOA.",
            "Finally, use the ratios to find missing sides or angles."
        ],
        "example": "If a right triangle has an opposite side of 3 and hypotenuse of 5, then sin(theta) = 3/5.",
        "quiz": [
            "What is trigonometry in one or two lines?",
            "What does SOH-CAH-TOA help us remember?",
            "If opposite = 4 and hypotenuse = 5, what is sin(theta)?"
        ],
        "keywords": ["triangle", "angle", "sine", "cosine", "tangent", "soh", "cah", "toa", "hypotenuse", "opposite", "adjacent"]
    },
    "chemical bonding": {
        "definition": "Chemical bonding is the force of attraction that holds atoms together to form molecules or compounds.",
        "steps": [
            "First, remember that atoms bond to become more stable.",
            "Second, atoms often try to complete their outer electron shell.",
            "Third, learn the main types of bonds: ionic, covalent, and metallic.",
            "Finally, understand bonding by checking whether electrons are transferred or shared."
        ],
        "example": "In sodium chloride, sodium gives one electron to chlorine, so an ionic bond forms.",
        "quiz": [
            "What is chemical bonding?",
            "What is the difference between ionic and covalent bonding?",
            "Give one real example of a compound and mention its bond type."
        ],
        "keywords": ["atom", "atoms", "electron", "electrons", "ionic", "covalent", "metallic", "bond", "compound", "molecule", "stable"]
    },
    "algebra": {
        "definition": "Algebra is the branch of mathematics that uses symbols and variables to represent numbers and relationships.",
        "steps": [
            "First, understand that a variable is a symbol like x that stands for an unknown value.",
            "Second, equations show relationships between numbers and variables.",
            "Third, solve equations by isolating the variable step by step.",
            "Finally, verify the answer by substituting it back."
        ],
        "example": "In x + 5 = 9, subtract 5 from both sides to get x = 4.",
        "quiz": [
            "What is a variable?",
            "Solve: x + 7 = 12.",
            "Why do we check answers after solving an equation?"
        ],
        "keywords": ["variable", "equation", "x", "unknown", "solve", "expression", "value"]
    },
    "physics": {
        "definition": "Physics is the study of matter, energy, force, and motion, and how they interact in the universe.",
        "steps": [
            "First, identify what is happening physically, like motion, force, or energy transfer.",
            "Second, connect the event to a basic law or formula.",
            "Third, define the quantities involved such as mass, velocity, or acceleration.",
            "Finally, solve step by step using logic and formulas."
        ],
        "example": "If a ball falls down due to gravity, physics explains that the Earth pulls it downward.",
        "quiz": [
            "What does physics study?",
            "What is force?",
            "Give one daily life example of physics."
        ],
        "keywords": ["force", "motion", "energy", "mass", "gravity", "velocity", "acceleration"]
    },
    "programming": {
        "definition": "Programming is the process of writing instructions that tell a computer what to do.",
        "steps": [
            "First, define the problem clearly.",
            "Second, break the problem into smaller steps.",
            "Third, write instructions in the correct order using code.",
            "Finally, test the program and fix mistakes."
        ],
        "example": "A calculator program adds two numbers because the programmer wrote instructions for input, processing, and output.",
        "quiz": [
            "What is programming?",
            "Why do we break a problem into smaller steps?",
            "What is the purpose of testing a program?"
        ],
        "keywords": ["code", "computer", "program", "logic", "instructions", "bug", "function"]
    },
    "general studies": {
        "definition": "A topic becomes easier when you understand its meaning, break it into parts, and practice with examples.",
        "steps": [
            "First, learn the basic definition.",
            "Second, identify the main rules or ideas.",
            "Third, study one simple example.",
            "Finally, test yourself with a small question."
        ],
        "example": "If you do not know a topic, start by asking what it means in plain language.",
        "quiz": [
            "What is the main idea of the topic?",
            "What is one important rule or fact?",
            "Give one simple example."
        ],
        "keywords": ["definition", "idea", "example", "concept", "meaning"]
    }
}


def get_topic_data(topic: str):
    return TOPIC_KB.get(topic, TOPIC_KB["general studies"])


def personalized_intro(memory, topic):
    pace = memory["user_profile"].get("preferred_pace", "medium")
    style = memory["user_profile"].get("preferred_style", "simple")
    confidence = memory.get("topic_confidence", {}).get(topic, 50)
    weak_topics = memory.get("weak_topics", [])
    strong_topics = memory.get("strong_topics", [])

    lines = [
        f"I remember that you prefer {style} explanations at a {pace} pace."
    ]

    if topic in weak_topics:
        lines.append(f"You seem to struggle with {topic}, so I will explain it more carefully.")
        lines.append(f"{topic.title()} is currently marked as a weak topic, so I will simplify the explanation and focus on fundamentals.")
    elif topic in strong_topics:
        lines.append(f"You seem fairly comfortable with {topic}, so I can keep it tighter.")

    lines.append(f"Your current confidence in this topic is {confidence}/100.")
    return " ".join(lines)
def generate_tutor_response(message, memory):
    topic = detect_topic(message)
    data = get_topic_data(topic)

    reply = f"""
{personalized_intro(memory, topic)}

Topic: {topic.title()}

Definition:
{data['definition']}

Step-by-step explanation:
1. {data['steps'][0]}
2. {data['steps'][1]}
3. {data['steps'][2]}
4. {data['steps'][3]}

Example:
{data['example']}

Quick recap:
{data['definition']}

Next practice step:
Write this topic in your own words, then try one simple question on it.
""".strip()

    return reply, topic


def generate_quiz_question(topic_input, memory):
    topic = detect_topic(topic_input)
    data = get_topic_data(topic)
    confidence = memory.get("topic_confidence", {}).get(topic, 50)

    if confidence < 40:
        difficulty = "easy"
    elif confidence < 75:
        difficulty = "medium"
    else:
        difficulty = "challenging"

    reply = f"""
Quiz on {topic.title()} ({difficulty})

1. {data['quiz'][0]}
2. {data['quiz'][1]}
3. {data['quiz'][2]}

Answer all three together, and I will evaluate them.
""".strip()

    return reply, topic


def evaluate_quiz_reply(topic, answer, memory):
    data = get_topic_data(topic)
    text = answer.lower()
    keywords = data["keywords"]

    keyword_hits = sum(1 for kw in keywords if kw in text)
    word_count = len(text.split())

    if "don't know" in text or "dont know" in text or "not sure" in text:
        verdict = "incorrect"
    elif keyword_hits >= 4 and word_count >= 12:
        verdict = "correct"
    elif keyword_hits >= 2 and word_count >= 6:
        verdict = "partly correct"
    else:
        verdict = "incorrect"

    if verdict == "correct":
        return f"""
Verdict: Correct

Why:
Your answer includes the main concepts of {topic} and shows that you understand the topic reasonably well.

Correction:
No major correction needed. You can improve by making your explanation more precise.

Next step:
Try a harder question or solve one numerical/example-based problem on {topic}.
""".strip()

    if verdict == "partly correct":
        return f"""
Verdict: Partly correct

Why:
Your answer shows some understanding of {topic}, but it is incomplete or missing important terms.

Correction:
Review the core definition and one solid example before answering again.

Next step:
Read the explanation once more and retry the quiz in clearer sentences.
""".strip()

    return f"""
Verdict: Incorrect

Why:
Your answer does not yet show a stable understanding of {topic}.

Correction:
Start again from the basic definition and one example.

Next step:
Ask for a simpler explanation of {topic}, then attempt the quiz again.
""".strip()
