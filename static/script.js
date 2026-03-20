function updateDashboard(memory) {
    document.getElementById("lastTopic").textContent = memory.last_topic || "-";
    document.getElementById("recommendedNext").textContent = memory.recommended_next || "-";
    document.getElementById("weakTopics").textContent = memory.weak_topics.length ? memory.weak_topics.join(", ") : "-";
    document.getElementById("strongTopics").textContent = memory.strong_topics.length ? memory.strong_topics.join(", ") : "-";
    document.getElementById("memory").textContent = JSON.stringify(memory, null, 4);
}

async function sendMessage(mode) {
    const input = document.getElementById("message");
    const replyBox = document.getElementById("reply");
    const message = input.value.trim();

    if (!message) {
        replyBox.textContent = "Please enter something.";
        return;
    }

    replyBox.textContent = "Thinking...";

    try {
        const res = await fetch("/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message, mode })
        });

        const data = await res.json();

        if (!res.ok) {
            replyBox.textContent = data.reply || "Something went wrong.";
            return;
        }

        replyBox.textContent = data.reply;
        updateDashboard(data.memory);
    } catch (e) {
        replyBox.textContent = "Server error. Please try again.";
    }
}

async function resetMemory() {
    const replyBox = document.getElementById("reply");

    try {
        const res = await fetch("/reset", { method: "POST" });
        const data = await res.json();
        replyBox.textContent = data.message || "Memory reset.";
        updateDashboard(data.memory);
    } catch (e) {
        replyBox.textContent = "Could not reset memory.";
    }
}
