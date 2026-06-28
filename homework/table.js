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

// --- encrypted scores/IDs: fields in grades.csv are ciphertext; password derives the key ---
let SHOW_SCORES = false;
let KEY = null; // Uint8Array(32), set only after the correct password
const PW_SALT = "wg2026:";
// verification hash — a DIFFERENT hash than the key, so the key is never in the code
const PW_CHECK = "d099007c7be937cabe523cbf6004c6d2b403c1abf907b3fcaf11837276a1bccd";
const ENC_FIELDS = ["nim", "w7_id", "w11_id", "w7_score", "w7_note", "w11_score", "w11_note", "uas_score"];

// self-contained SHA-256 over bytes (no Web Crypto, so it works on http/file:// too)
function sha256bytes(bytes) {
  const K = [0x428a2f98,0x71374491,0xb5c0fbcf,0xe9b5dba5,0x3956c25b,0x59f111f1,0x923f82a4,0xab1c5ed5,0xd807aa98,0x12835b01,0x243185be,0x550c7dc3,0x72be5d74,0x80deb1fe,0x9bdc06a7,0xc19bf174,0xe49b69c1,0xefbe4786,0x0fc19dc6,0x240ca1cc,0x2de92c6f,0x4a7484aa,0x5cb0a9dc,0x76f988da,0x983e5152,0xa831c66d,0xb00327c8,0xbf597fc7,0xc6e00bf3,0xd5a79147,0x06ca6351,0x14292967,0x27b70a85,0x2e1b2138,0x4d2c6dfc,0x53380d13,0x650a7354,0x766a0abb,0x81c2c92e,0x92722c85,0xa2bfe8a1,0xa81a664b,0xc24b8b70,0xc76c51a3,0xd192e819,0xd6990624,0xf40e3585,0x106aa070,0x19a4c116,0x1e376c08,0x2748774c,0x34b0bcb5,0x391c0cb3,0x4ed8aa4a,0x5b9cca4f,0x682e6ff3,0x748f82ee,0x78a5636f,0x84c87814,0x8cc70208,0x90befffa,0xa4506ceb,0xbef9a3f7,0xc67178f2];
  let h = [0x6a09e667,0xbb67ae85,0x3c6ef372,0xa54ff53a,0x510e527f,0x9b05688c,0x1f83d9ab,0x5be0cd19];
  const l = bytes.length, withOne = l + 1, k = (56 - withOne % 64 + 64) % 64, total = withOne + k + 8;
  const m = new Uint8Array(total); m.set(bytes); m[l] = 0x80;
  const dv = new DataView(m.buffer), bits = l * 8;
  dv.setUint32(total - 4, bits >>> 0); dv.setUint32(total - 8, Math.floor(bits / 0x100000000));
  const rr = (x, n) => (x >>> n) | (x << (32 - n));
  for (let off = 0; off < total; off += 64) {
    const w = new Uint32Array(64);
    for (let i = 0; i < 16; i++) w[i] = dv.getUint32(off + i * 4);
    for (let i = 16; i < 64; i++) {
      const s0 = rr(w[i-15],7) ^ rr(w[i-15],18) ^ (w[i-15]>>>3);
      const s1 = rr(w[i-2],17) ^ rr(w[i-2],19) ^ (w[i-2]>>>10);
      w[i] = (w[i-16] + s0 + w[i-7] + s1) >>> 0;
    }
    let [a,b,c,d,e,f,g,hh] = h;
    for (let i = 0; i < 64; i++) {
      const S1 = rr(e,6) ^ rr(e,11) ^ rr(e,25), ch = (e&f) ^ (~e&g);
      const t1 = (hh + S1 + ch + K[i] + w[i]) >>> 0;
      const S0 = rr(a,2) ^ rr(a,13) ^ rr(a,22), maj = (a&b) ^ (a&c) ^ (b&c);
      const t2 = (S0 + maj) >>> 0;
      hh=g; g=f; f=e; e=(d+t1)>>>0; d=c; c=b; b=a; a=(t1+t2)>>>0;
    }
    h = [(h[0]+a)>>>0,(h[1]+b)>>>0,(h[2]+c)>>>0,(h[3]+d)>>>0,(h[4]+e)>>>0,(h[5]+f)>>>0,(h[6]+g)>>>0,(h[7]+hh)>>>0];
  }
  const o = new Uint8Array(32);
  for (let i = 0; i < 8; i++) { o[i*4]=h[i]>>>24; o[i*4+1]=(h[i]>>>16)&255; o[i*4+2]=(h[i]>>>8)&255; o[i*4+3]=h[i]&255; }
  return o;
}
function sha256hex(str) {
  return [...sha256bytes(new TextEncoder().encode(str))].map(b => b.toString(16).padStart(2, "0")).join("");
}

// --- field decryption (SHA-256 counter-mode keystream XOR, per-cell nonce) ---
function b64ToBytes(b64) { const s = atob(b64), a = new Uint8Array(s.length); for (let i = 0; i < s.length; i++) a[i] = s.charCodeAt(i); return a; }
function catBytes(...arrs) { let n = 0; for (const a of arrs) n += a.length; const o = new Uint8Array(n); let p = 0; for (const a of arrs) { o.set(a, p); p += a.length; } return o; }
function u32be(i) { return new Uint8Array([(i>>>24)&255, (i>>>16)&255, (i>>>8)&255, i&255]); }
function keystream(key, nonce, n) { const bl = []; let t = 0, i = 0; while (t < n) { bl.push(sha256bytes(catBytes(key, nonce, u32be(i)))); t += 32; i++; } return catBytes(...bl).subarray(0, n); }
function decryptField(token) {
  if (!token || !KEY) return "";
  const raw = b64ToBytes(token), nonce = raw.subarray(0, 8), ct = raw.subarray(8), ks = keystream(KEY, nonce, ct.length);
  const pt = new Uint8Array(ct.length);
  for (let i = 0; i < ct.length; i++) pt[i] = ct[i] ^ ks[i];
  return new TextDecoder().decode(pt);
}
function decryptRow(r) { const o = { ...r }; for (const f of ENC_FIELDS) o[f] = decryptField(r[f]); return o; }

function lockedCell(tdClass) {
  return `<td class="${tdClass}" data-sort="-1"><span class="cell"><span class="badge locked">•••</span></span></td>`;
}

function toggleScores() {
  if (SHOW_SCORES) return;
  const p = prompt("Masukkan password untuk menampilkan skor:");
  if (p === null) return;
  if (sha256hex("verify:" + PW_SALT + p) === PW_CHECK) {
    KEY = sha256bytes(new TextEncoder().encode(PW_SALT + p));
    SHOW_SCORES = true;
    const b = document.getElementById("lockBtn");
    if (b) { b.textContent = "🔓 Skor ditampilkan"; b.disabled = true; }
    renderTable();
  } else {
    alert("Password salah.");
  }
}
