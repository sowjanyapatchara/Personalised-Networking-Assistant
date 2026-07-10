const verifyForm = document.getElementById("verify-form");
const verifyBtn = document.getElementById("verify-btn");
const statusArea = document.getElementById("status-area");
const resultEl = document.getElementById("result");
const resultTitle = document.getElementById("result-title");
const resultSummary = document.getElementById("result-summary");
const resultLink = document.getElementById("result-link");

function showStatus(message, type = "info") {
  statusArea.innerHTML = `<div class="status-banner status-${type}">${escapeHtml(message)}</div>`;
}

verifyForm.addEventListener("submit", async (e) => {
  e.preventDefault();
  statusArea.innerHTML = "";
  resultEl.style.display = "none";

  const query = document.getElementById("query").value.trim();
  if (!query) return;

  verifyBtn.disabled = true;
  verifyBtn.textContent = "Checking…";

  try {
    const data = await apiGet(`/api/v1/verify?query=${encodeURIComponent(query)}`);

    if (!data.found) {
      showStatus(`No reliable Wikipedia reference found for "${query}". Try rephrasing.`, "error");
      return;
    }

    resultTitle.textContent = data.query;
    resultSummary.textContent = data.summary || "No summary available.";
    resultLink.href = data.source_url || "#";
    resultEl.style.display = "block";
  } catch (err) {
    showStatus(`Fact check failed: ${err.message}`, "error");
  } finally {
    verifyBtn.disabled = false;
    verifyBtn.textContent = "Check →";
  }
});
