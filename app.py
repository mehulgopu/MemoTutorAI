from flask import Flask, render_template, request, jsonify
from utils.memory import (
    load_memory,
    save_memory,
    reset_memory,
    update_memory_from_message,
    update_confidence
)
from utils.tutor import (
    generate_tutor_response,
    generate_quiz_question,
    evaluate_quiz_reply
)

app = Flask(__name__)
LAST_QUIZ_TOPIC = {"value": ""}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    message = data.get("message", "").strip()
    mode = data.get("mode", "explain")

    if not message:
        return jsonify({"reply": "Please enter something."}), 400

    memory = load_memory()

    try:
        if mode == "quiz":
            update_memory_from_message(message, memory)
            reply, topic = generate_quiz_question(message, memory)
            LAST_QUIZ_TOPIC["value"] = topic
            memory["last_topic"] = topic

        elif mode == "quiz_answer":
            topic = LAST_QUIZ_TOPIC["value"] or memory.get("last_topic", "general studies")
            reply = evaluate_quiz_reply(topic, message, memory)

            lower = reply.lower()
            if "incorrect" in lower:
                update_confidence(memory, topic, -10)
                memory["mistakes"].append(f"Weak quiz answer in {topic}: {message}")
            elif "partly correct" in lower:
                update_confidence(memory, topic, 3)
            elif "correct" in lower:
                update_confidence(memory, topic, 10)

        else:
            update_memory_from_message(message, memory)
            reply, topic = generate_tutor_response(message, memory)
            memory["last_topic"] = topic

        if memory["weak_topics"]:
            memory["recommended_next"] = memory["weak_topics"][0]
        else:
            memory["recommended_next"] = memory.get("last_topic", "")

        save_memory(memory)

        return jsonify({
            "reply": reply,
            "memory": memory,
            "last_topic": memory.get("last_topic", "")
        })

    except Exception as e:
        return jsonify({
            "reply": f"Something went wrong in the backend: {str(e)}"
        }), 500


@app.route("/reset", methods=["POST"])
def clear_memory():
    reset_memory()
    LAST_QUIZ_TOPIC["value"] = ""
    memory = load_memory()
    return jsonify({
        "message": "Memory reset complete.",
        "memory": memory,
        "last_topic": ""
    })

import os

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
