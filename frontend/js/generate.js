const form = document.getElementById("generate-form");
const submitBtn = document.getElementById("submit-btn");
const statusArea = document.getElementById("status-area");
const resultsEl = document.getElementById("results");
const themesContainer = document.getElementById("themes-container");
const startersContainer = document.getElementById("starters-container");

function showStatus(message, type = "info") {
  statusArea.innerHTML = `<div class="status-banner status-${type}">${escapeHtml(message)}</div>`;
}

function clearStatus() {
  statusArea.innerHTML = "";
}

form.addEventListener("submit", async (e) => {
  e.preventDefault();
  clearStatus();

  const name = document.getElementById("name").value.trim();
  const bio = document.getElementById("bio").value.trim();
  const event_description = document.getElementById("event").value.trim();
  const interests = document.getElementById("interests").value.trim();

  if (!bio || !event_description) {
    showStatus("Please fill in both your bio and the event description.", "error");
    return;
  }

  submitBtn.disabled = true;
  submitBtn.textContent = "Generating…";
  resultsEl.style.display = "none";

  try {
    const data = await apiPost("/api/v1/generate", {
      name: name || null,
      bio,
      event_description,
      interests: interests || null,
    });

    renderResults(data);
    resultsEl.style.display = "block";
    resultsEl.scrollIntoView({ behavior: "smooth", block: "start" });
  } catch (err) {
    showStatus(`Couldn't generate starters: ${err.message}`, "error");
  } finally {
    submitBtn.disabled = false;
    submitBtn.textContent = "Generate starters →";
  }
});

function renderResults(data) {
  themesContainer.innerHTML = data.themes
    .map((t) => `<span class="theme-pill">${escapeHtml(t)}</span>`)
    .join("");

  startersContainer.innerHTML = data.starters
    .map(
      (s, idx) => `
      <div class="starter-item">
        <div class="starter-badge">${idx + 1}</div>
        <div style="flex:1;">
          <div class="starter-text">${escapeHtml(s)}</div>
          <div class="feedback-row">
            <button class="icon-btn" data-useful="true" data-interaction="${data.interaction_id}">👍 Useful</button>
            <button class="icon-btn" data-useful="false" data-interaction="${data.interaction_id}">👎 Not for me</button>
          </div>
        </div>
      </div>`
    )
    .join("");

  startersContainer.querySelectorAll(".icon-btn").forEach((btn) => {
    btn.addEventListener("click", async () => {
      const interactionId = Number(btn.dataset.interaction);
      const useful = btn.dataset.useful === "true";
      const row = btn.parentElement;

      try {
        await apiPost("/api/v1/feedback", { interaction_id: interactionId, useful });
        row.querySelectorAll(".icon-btn").forEach((b) => b.classList.remove("active"));
        btn.classList.add("active");
      } catch (err) {
        showStatus(`Couldn't save feedback: ${err.message}`, "error");
      }
    });
  });
}
