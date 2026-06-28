/* Shared table helpers for the homework pages.
   All data comes from grades.csv — the HTML files only render it. */

// --- robust CSV parser (handles quoted fields with commas/quotes) ---
function parseCSV(text) {
  const rows = [];
  let field = "", row = [], inQ = false, i = 0;
  while (i < text.length) {
    const c = text[i];
    if (inQ) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else inQ = false; }
      else field += c;
    } else if (c === '"') inQ = true;
    else if (c === ",") { row.push(field); field = ""; }
    else if (c === "\n") { row.push(field); rows.push(row); row = []; field = ""; }
    else if (c !== "\r") field += c;
    i++;
  }
  if (field.length || row.length) { row.push(field); rows.push(row); }
  const header = rows.shift().map(h => h.trim());
  return rows
    .filter(r => r.some(v => v !== ""))
    .map(r => Object.fromEntries(header.map((h, j) => [h, (r[j] ?? "").trim()])));
}

function esc(s) {
  return String(s).replace(/[&<>"]/g, c => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
}

// escape then turn bare URLs into links (for note popovers)
function linkifyNote(note) {
  return esc(note).replace(/https?:\/\/[^\s]+/g,
    u => `<a href="${u}" target="_blank" rel="noopener">${u}</a>`);
}

const NOTE_BTN = '<button type="button" class="note-btn" onclick="toggleNote(this)" aria-expanded="false" aria-label="Show note" title="Show note">i</button>';

// a table cell holding a badge (+ optional note popover)
function badgeCell(tdClass, sort, badgeHtml, note) {
  if (note && note.trim())
    return `<td class="${tdClass}" data-sort="${sort}"><span class="cell">${badgeHtml}${NOTE_BTN}</span><div class="note" hidden>${linkifyNote(note)}</div></td>`;
  return `<td class="${tdClass}" data-sort="${sort}"><span class="cell">${badgeHtml}</span></td>`;
}

// a repo/live link cell (or em-dash)
function linkCell(url, label) {
  if (url && url.trim())
    return `<td data-sort="1"><a href="${esc(url)}" target="_blank" rel="noopener">${label}&nbsp;↗</a></td>`;
  return '<td data-sort="0"><span class="none">—</span></td>';
}

function scoreBadge(score) {
  return `<span class="badge s${esc(score)}">${esc(score)}</span>`;
}
function uasBadge(score) {
  const n = parseFloat(score);
  const cls = n >= 80 ? "u80" : n >= 60 ? "u60" : "u0";
  return `<span class="badge ${cls}">${esc(score)}</span>`;
}

// --- interactions (work on the rendered DOM) ---
function toggleNote(btn) {
  const note = btn.closest("td").querySelector(".note");
  const show = note.hasAttribute("hidden");
  if (show) note.removeAttribute("hidden"); else note.setAttribute("hidden", "");
  btn.setAttribute("aria-expanded", show ? "true" : "false");
}

let sortState = { col: null, dir: 1 };
function sortBy(col, type) {
  const tbody = document.getElementById("tbody");
  const rows = Array.from(tbody.querySelectorAll("tr"));
  sortState.dir = (sortState.col === col) ? -sortState.dir : 1;
  sortState.col = col;
  const val = tr => {
    const cell = tr.children[col];
    const v = cell.dataset.sort !== undefined ? cell.dataset.sort : cell.textContent.trim();
    return type === "num" ? parseFloat(v) : v.toLowerCase();
  };
  rows.sort((a, b) => { const x = val(a), y = val(b); return x < y ? -sortState.dir : x > y ? sortState.dir : 0; });
  rows.forEach(r => tbody.appendChild(r));
  document.querySelectorAll("thead th").forEach((th, i) => {
    th.classList.toggle("sorted", i === col);
    th.querySelector(".arrow").textContent = i === col ? (sortState.dir === 1 ? "▲" : "▼") : "";
  });
}

async function loadGrades() {
  const res = await fetch("grades.csv", { cache: "no-store" });
  if (!res.ok) throw new Error("Failed to load grades.csv (" + res.status + ")");
  return parseCSV(await res.text());
}
