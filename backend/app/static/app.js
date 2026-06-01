const form = document.getElementById("screening-form");
const resumesInput = document.getElementById("resumes-input");
const summaryText = document.getElementById("summary-text");
const results = document.getElementById("results");

function parseResumes(raw) {
  return raw
    .split("=== CANDIDATE:")
    .map((block) => block.trim())
    .filter(Boolean)
    .map((block) => {
      const [idLine, ...rest] = block.split("===");
      return {
        candidate_id: idLine.trim(),
        resume_text: rest.join(" ").trim(),
      };
    });
}

function renderCandidate(candidate) {
  const traceHtml = candidate.traces
    .map(
      (trace) => `
        <div class="trace">
          <strong>${trace.agent_name}</strong>
          <p>${trace.summary}</p>
        </div>
      `,
    )
    .join("");

  return `
    <article class="candidate-card">
      <div class="candidate-head">
        <h3>${candidate.rank}. ${candidate.candidate_name}</h3>
        <span class="badge">${candidate.score}%</span>
      </div>
      <p><strong>Recommendation:</strong> ${candidate.recommendation}</p>
      <p><strong>Matched skills:</strong> ${candidate.matched_skills.join(", ") || "None"}</p>
      <p><strong>Missing skills:</strong> ${candidate.missing_skills.join(", ") || "None"}</p>
      <p><strong>Strengths:</strong> ${candidate.strengths.join(" | ")}</p>
      <p><strong>Concerns:</strong> ${candidate.concerns.join(" | ")}</p>
      <p><strong>Interview questions:</strong></p>
      <ul>${candidate.interview_questions.map((question) => `<li>${question}</li>`).join("")}</ul>
      <details>
        <summary>Agent traces</summary>
        ${traceHtml}
      </details>
    </article>
  `;
}

form.addEventListener("submit", async (event) => {
  event.preventDefault();
  const payload = {
    job_title: form.job_title.value,
    job_description: form.job_description.value,
    resumes: parseResumes(resumesInput.value),
  };

  summaryText.textContent = "Screening candidates...";
  results.innerHTML = "";

  const response = await fetch("/api/screen", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });

  const data = await response.json();
  summaryText.textContent = data.screening_summary;
  results.innerHTML = data.results.map(renderCandidate).join("");
});
