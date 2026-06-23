#!/usr/bin/env python3
"""Combined result recap across Week 7 and Week 11.

Scoring per week:
  - live site accessible (HTTP 200)        -> 100
  - repo accessible but no working live     -> 90  (note: no live / live not accessible)
  - neither repo nor live accessible        -> 0   (note why)
  - no submission that week                 -> 0   (note: no submission)

Students are matched across weeks by name (submission-folder ids differ per week).
The `id` column is the NIM extracted from the PDF (best effort, blank if unreadable).
Live/repo URLs come from week7_recap.csv / week11_recap.csv and are checked over HTTP."""
import csv, os, re, glob, subprocess, html
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))


def norm_name(n):
    return re.sub(r"\s+", " ", n.strip()).lower()


def load_recap(path):
    d = {}
    with open(path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            d[norm_name(row["name"])] = row
    return d


def build_pdf_map(weekdir):
    m = {}
    base = os.path.join(HERE, weekdir)
    if not os.path.isdir(base):
        return m
    for dname in sorted(os.listdir(base)):
        full = os.path.join(base, dname)
        if not os.path.isdir(full):
            continue
        nm = norm_name(dname.split("_")[0])
        pdfs = glob.glob(full + "/*.pdf") + glob.glob(full + "/*.PDF")
        if pdfs:
            m[nm] = pdfs[0]
    return m


NIM_RE = re.compile(
    r"(20\d{2}\.\d{4,6}\.SV\.\d{3,5}"          # 2024.545224.SV.25633
    r"|\d{2,4}/\d{4,6}/SV/\d{3,5}"             # 24/541443/SV/24907
    r"|\d{6,8}/SV/\d{3,5})",                   # 24544769/SV/25525
    re.I)


def extract_nim(pdf):
    try:
        t = subprocess.run(["pdftotext", "-f", "1", "-l", "1", "-layout", pdf, "-"],
                           capture_output=True, timeout=30).stdout.decode("utf-8", "ignore")
    except Exception:
        return ""
    for line in t.splitlines():
        if re.search(r"\bNIM\b", line, re.I):
            m = NIM_RE.search(line)
            if m:
                return m.group(1).strip()
    m = NIM_RE.search(t)
    return m.group(1).strip() if m else ""


def check_url(url):
    try:
        r = subprocess.run(["curl", "-sS", "-o", "/dev/null", "-L", "--max-time", "15",
                            "-w", "%{http_code}", url], capture_output=True, timeout=20)
        return r.stdout.decode().strip() or "000"
    except Exception:
        return "000"


w7 = load_recap(os.path.join(HERE, "week7_recap.csv"))
w11 = load_recap(os.path.join(HERE, "week11_recap.csv"))
pdf7 = build_pdf_map("week-7")
pdf11 = build_pdf_map("week-11")

# all student names (union)
names = {}
for d in (w7, w11):
    for k, v in d.items():
        names.setdefault(k, v["name"])

# NIM per student (prefer whichever week has it)
def nim_for(nm):
    for pm in (pdf11, pdf7):
        if nm in pm:
            nim = extract_nim(pm[nm])
            if nim:
                return nim
    return ""

# collect and check all URLs once
urls = set()
for d in (w7, w11):
    for v in d.values():
        if v["github_repo"]:
            urls.add(v["github_repo"])
        if v["live_url"]:
            urls.add(v["live_url"])
urls = sorted(urls)
print(f"Checking {len(urls)} URLs over HTTP...")
with ThreadPoolExecutor(max_workers=20) as ex:
    status = dict(zip(urls, ex.map(check_url, urls)))


def score_week(row):
    if row is None:
        return 0, "Tidak ada submission"
    repo, live, rnote = row["github_repo"], row["live_url"], row["notes"]
    live_ok = bool(live) and status.get(live) == "200"
    repo_ok = bool(repo) and status.get(repo) == "200"
    if live_ok:
        return 100, ""
    if repo_ok:
        if live:
            return 90, f"Live site tidak bisa diakses (HTTP {status.get(live)})"
        return 90, "Tidak ada live site"
    # score 0
    reasons = []
    if not repo and not live:
        reasons.append(rnote or "Tidak ada link repo/live")
    else:
        if repo and not repo_ok:
            reasons.append(f"Repo tidak bisa diakses (HTTP {status.get(repo)})")
        if not repo:
            reasons.append("Tidak ada repo")
        if live and not live_ok:
            reasons.append(f"Live site tidak bisa diakses (HTTP {status.get(live)})")
        if not live:
            reasons.append("Tidak ada live site")
        if rnote:
            reasons.append(rnote)
    return 0, "; ".join(reasons)


rows = []
for nm in sorted(names, key=lambda x: names[x].lower()):
    name = names[nm]
    s7, n7 = score_week(w7.get(nm))
    s11, n11 = score_week(w11.get(nm))
    rows.append([nim_for(nm), name, s7, n7, s11, n11])

out = os.path.join(HERE, "results_recap.csv")
with open(out, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["student_id", "name", "week7_score", "week7_note", "week11_score", "week11_note"])
    w.writerows(rows)

print(f"\nStudents: {len(rows)}")
for wk, idx in (("Week 7", 2), ("Week 11", 4)):
    c100 = sum(1 for r in rows if r[idx] == 100)
    c90 = sum(1 for r in rows if r[idx] == 90)
    c0 = sum(1 for r in rows if r[idx] == 0)
    print(f"  {wk}: 100={c100}  90={c90}  0={c0}")
print("CSV ->", out)


# ---- published web page (homework/results.html) ----
def cell(score, note):
    cls = {100: "s100", 90: "s90", 0: "s0"}[score]
    badge = f'<span class="badge {cls}">{score}</span>'
    if note:
        btn = ('<button type="button" class="note-btn" onclick="toggleNote(this)" '
               'aria-expanded="false" aria-label="Show note" title="Show note">i</button>')
        inner = f'<span class="cell">{badge}{btn}</span><div class="note" hidden>{html.escape(note)}</div>'
    else:
        inner = f'<span class="cell">{badge}</span>'
    return f'<td class="wk" data-sort="{score}">{inner}</td>'


trs = []
for i, (nim, name, s7, n7, s11, n11) in enumerate(rows, 1):
    trs.append(
        f'    <tr>'
        f'<td class="num" data-sort="{i}">{i}</td>'
        f'<td class="nim" data-sort="{html.escape(nim)}">{html.escape(nim) or "—"}</td>'
        f'<td class="name">{html.escape(name)}</td>'
        f'{cell(s7, n7)}{cell(s11, n11)}</tr>'
    )
table_rows = "\n".join(trs)


def stat_block(label, idx):
    c100 = sum(1 for r in rows if r[idx] == 100)
    c90 = sum(1 for r in rows if r[idx] == 90)
    c0 = sum(1 for r in rows if r[idx] == 0)
    return (f'<div class="statgrp"><div class="statgrp-label">{label}</div>'
            f'<span class="chip c100">{c100} × 100</span>'
            f'<span class="chip c90">{c90} × 90</span>'
            f'<span class="chip c0">{c0} × 0</span></div>')


stats_html = stat_block("Week 7", 2) + stat_block("Week 11", 4)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rekap Nilai Tugas — Web GIS 2026</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5; color: #333; padding: 2rem 1rem; }
        .container { max-width: 920px; margin: 0 auto; }
        a.back { color: #2563eb; text-decoration: none; font-size: 0.85rem; }
        a.back:hover { text-decoration: underline; }
        h1 { font-size: 1.7rem; margin: 0.6rem 0 0.3rem; }
        .subtitle { color: #666; font-size: 0.92rem; margin-bottom: 1rem; }
        .statgrp { display: flex; align-items: center; gap: 0.45rem; flex-wrap: wrap; margin-bottom: 0.5rem; }
        .statgrp-label { font-weight: 600; font-size: 0.85rem; width: 4.5rem; color: #475569; }
        .chip { font-size: 0.8rem; padding: 0.2rem 0.6rem; border-radius: 99px; font-weight: 600; }
        .chip.c100 { background: #dcfce7; color: #15803d; }
        .chip.c90 { background: #fef9c3; color: #a16207; }
        .chip.c0 { background: #fee2e2; color: #b91c1c; }
        .controls { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; margin: 1rem 0 0.6rem; }
        .search { flex: 1; min-width: 200px; max-width: 320px; padding: 0.5rem 0.8rem; font-size: 0.9rem;
            border: 1px solid #ddd; border-radius: 8px; }
        .controls label { font-size: 0.85rem; color: #555; display: flex; align-items: center; gap: 0.35rem; }
        .legend { color: #888; font-size: 0.78rem; margin-bottom: 1rem; }
        .table-wrap { background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08); overflow-x: auto; }
        table { border-collapse: collapse; width: 100%; font-size: 0.85rem; }
        thead th { position: sticky; top: 0; background: #f8fafc; text-align: left; padding: 0.7rem 0.8rem;
            border-bottom: 2px solid #e5e7eb; font-weight: 600; white-space: nowrap; cursor: pointer; user-select: none; }
        thead th:hover { background: #eef2f7; }
        thead th .arrow { color: #9ca3af; font-size: 0.7rem; margin-left: 0.2rem; }
        thead th.sorted .arrow { color: #2563eb; }
        td { padding: 0.6rem 0.8rem; border-bottom: 1px solid #f0f0f0; vertical-align: top; }
        tbody tr:hover { background: #f9fafb; }
        .num { color: #999; }
        .nim { color: #555; font-variant-numeric: tabular-nums; white-space: nowrap; }
        .name { font-weight: 500; }
        .cell { display: inline-flex; align-items: center; gap: 0.45rem; }
        .badge { display: inline-flex; align-items: center; justify-content: center; min-width: 2.2rem;
            height: 1.5rem; padding: 0 0.5rem; border-radius: 99px; font-size: 0.8rem; font-weight: 700; }
        .badge.s100 { background: #dcfce7; color: #15803d; }
        .badge.s90 { background: #fef9c3; color: #a16207; }
        .badge.s0 { background: #fee2e2; color: #b91c1c; }
        .note-btn { width: 1.25rem; height: 1.25rem; flex: none; border-radius: 50%; border: 1px solid #d1d5db;
            background: #fff; color: #6b7280; font-size: 0.72rem; font-family: Georgia, serif; font-style: italic;
            font-weight: 700; line-height: 1; cursor: pointer; display: inline-flex; align-items: center;
            justify-content: center; transition: all 0.12s; }
        .note-btn:hover { border-color: #2563eb; color: #2563eb; }
        .note-btn[aria-expanded="true"] { background: #2563eb; border-color: #2563eb; color: #fff; }
        .note { display: block; color: #92400e; font-size: 0.75rem; margin-top: 0.35rem; max-width: 260px;
            background: #fffbeb; border: 1px solid #fde68a; border-radius: 6px; padding: 0.35rem 0.5rem; word-break: break-word; }
        .note[hidden] { display: none; }
        footer { text-align: center; margin-top: 1.5rem; color: #999; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="container">
        <a class="back" href="../">← Kembali ke materi kuliah</a>
        <h1>📊 Rekap Nilai Tugas</h1>
        <p class="subtitle">Hasil penilaian submission Week 7 (Mini WebGIS) &amp; Week 11 (WMS &amp; WFS) · Web GIS 2026</p>

        __STATS__

        <div class="controls">
            <input class="search" id="q" type="search" placeholder="Cari nama atau NIM…" oninput="filterRows()">
            <label><input type="checkbox" id="reviewOnly" onchange="filterRows()"> Hanya yang ada skor &lt; 100</label>
        </div>
        <p class="legend">Klik header kolom untuk mengurutkan &nbsp;·&nbsp; <b>100</b> = live site bisa diakses &nbsp;·&nbsp; <b>90</b> = repo ada tapi live site tidak ada/tidak bisa diakses &nbsp;·&nbsp; <b>0</b> = tidak ada submission / repo &amp; live tidak tersedia &nbsp;·&nbsp; klik tombol <i>i</i> untuk melihat catatan.</p>

        <div class="table-wrap">
        <table>
            <thead><tr>
                <th onclick="sortBy(0,'num')">#<span class="arrow"></span></th>
                <th onclick="sortBy(1,'text')">NIM<span class="arrow"></span></th>
                <th onclick="sortBy(2,'text')">Nama<span class="arrow"></span></th>
                <th onclick="sortBy(3,'num')">Week 7<span class="arrow"></span></th>
                <th onclick="sortBy(4,'num')">Week 11<span class="arrow"></span></th>
            </tr></thead>
            <tbody id="tbody">
__ROWS__
            </tbody>
        </table>
        </div>

        <footer>Dihasilkan dari submission · Web GIS 2026 · Ismail Sunni</footer>
    </div>
    <script>
        function toggleNote(btn) {
            const note = btn.closest('td').querySelector('.note');
            const show = note.hasAttribute('hidden');
            if (show) note.removeAttribute('hidden'); else note.setAttribute('hidden', '');
            btn.setAttribute('aria-expanded', show ? 'true' : 'false');
        }
        function filterRows() {
            const q = document.getElementById('q').value.toLowerCase();
            const reviewOnly = document.getElementById('reviewOnly').checked;
            for (const tr of document.querySelectorAll('#tbody tr')) {
                const matchText = tr.textContent.toLowerCase().includes(q);
                let needsReview = false;
                tr.querySelectorAll('.wk').forEach(td => { if (+td.dataset.sort < 100) needsReview = true; });
                tr.style.display = (matchText && (!reviewOnly || needsReview)) ? '' : 'none';
            }
        }
        let sortState = { col: null, dir: 1 };
        function sortBy(col, type) {
            const tbody = document.getElementById('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            sortState.dir = (sortState.col === col) ? -sortState.dir : 1;
            sortState.col = col;
            const val = (tr) => {
                const cell = tr.children[col];
                const v = cell.dataset.sort !== undefined ? cell.dataset.sort : cell.textContent.trim();
                return type === 'num' ? parseFloat(v) : v.toLowerCase();
            };
            rows.sort((a, b) => {
                const x = val(a), y = val(b);
                if (x < y) return -1 * sortState.dir;
                if (x > y) return 1 * sortState.dir;
                return 0;
            });
            rows.forEach(r => tbody.appendChild(r));
            document.querySelectorAll('thead th').forEach((th, i) => {
                th.classList.toggle('sorted', i === col);
                th.querySelector('.arrow').textContent = i === col ? (sortState.dir === 1 ? '▲' : '▼') : '';
            });
        }
    </script>
</body>
</html>
"""

REPO_ROOT = os.path.dirname(HERE)
hw_dir = os.path.join(REPO_ROOT, "homework")
os.makedirs(hw_dir, exist_ok=True)
page = TEMPLATE.replace("__ROWS__", table_rows).replace("__STATS__", stats_html)
out_html = os.path.join(hw_dir, "results.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(page)
print("HTML ->", out_html)
