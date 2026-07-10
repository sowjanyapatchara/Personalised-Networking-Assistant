const statusArea = document.getElementById("status-area");
const listEl = document.getElementById("history-list");

function showStatus(message, type = "info") {
  statusArea.innerHTML = `<div class="status-banner status-${type}">${escapeHtml(message)}</div>`;
}

async function loadHistory() {
  try {
    const items = await apiGet("/api/v1/history");

    if (!items.length) {
      listEl.innerHTML = `<div class="empty-state panel">No sessions yet. <a href="/generate.html" style="color:var(--accent);">Generate your first starters →</a></div>`;
      return;
    }

    listEl.innerHTML = `<div class="panel">${items.map(renderItem).join("")}</div>`;
  } catch (err) {
    showStatus(`Couldn't load history: ${err.message}`, "error");
  }
}

function renderItem(item) {
  const feedbackBadge =
    item.feedback === true
      ? `<span class="theme-pill" style="background:rgba(94,234,212,0.15);">👍 Marked useful</span>`
      : item.feedback === false
      ? `<span class="theme-pill" style="background:rgba(239,100,97,0.1); color:#f3a09e; border-color:rgba(239,100,97,0.25);">👎 Not useful</span>`
      : "";

  return `
    <div class="history-item">
      <div class="history-meta">
        <strong style="color:var(--text);">${escapeHtml(item.event_description)}</strong>
        <span class="history-date">${formatDate(item.created_at)}</span>
      </div>
      <div style="margin-bottom:10px;">
        ${item.themes.map((t) => `<span class="theme-pill">${escapeHtml(t)}</span>`).join("")}
      </div>
      <ul style="margin:0 0 10px 0; padding-left:18px; color:var(--text);">
        ${item.starters.map((s) => `<li style="margin-bottom:6px;">${escapeHtml(s)}</li>`).join("")}
      </ul>
      ${feedbackBadge}
    </div>
  `;
}

loadHistory();
