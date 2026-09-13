const button = document.getElementById("ask-button");

button.addEventListener("click", askAdvisor);

async function askAdvisor() {
    const question = document.getElementById("question").value.trim();

    if (!question) {
        alert("Please enter a question.");
        return;
    }

    const loading = document.getElementById("loading");
    const answerContainer = document.getElementById("answer-container");
    const answer = document.getElementById("answer");
    const sources = document.getElementById("sources");

    loading.classList.remove("hidden");
    answerContainer.classList.add("hidden");

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({
                question: question
            })
        });

        if (!response.ok) {
            throw new Error("Request failed");
        }

        const data = await response.json();

        answer.textContent = data.answer;
        sources.innerHTML = "";

        data.sources.forEach(source => {
            const card = document.createElement("div");
            card.className = "source-card";

            const title = document.createElement("h4");
            title.textContent = source.course_name
                ? `${source.course_code} — ${source.course_name}`
                : source.course_code;

            const link = document.createElement("a");
            link.href = source.source_url;
            link.target = "_blank";
            link.rel = "noopener noreferrer";
            link.textContent = "View official UofT course →";

            card.appendChild(title);
            card.appendChild(link);
            sources.appendChild(card);
        });

        answerContainer.classList.remove("hidden");
    } catch (error) {
        answer.textContent =
            "Something went wrong. Please try again.";
        answerContainer.classList.remove("hidden");
        console.error(error);
    } finally {
        loading.classList.add("hidden");
    }
}