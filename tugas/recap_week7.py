#!/usr/bin/env python3
"""Recap week-7 submissions: extract student id, name, GitHub repo link, and live (gh-pages/other) link from each PDF."""
import os, re, subprocess, csv, glob, sys, html, json

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "week-7")

# URLs that are noise: bundled-library refs, certificate CRLs, doc links, CDNs, etc.
NOISE = re.compile(
    r"andre-fuchs|kerning-pairs|wikipedia\.org|microsoft\.com|w3\.org|"
    r"openlayers|leafletjs|leaflet|openstreetmap|tile\.|/cdn|cdn\.|unpkg|jsdelivr|"
    r"googleapis|gstatic|fonts\.|schema\.|purl\.|/ns\.|/ns/|xmlns|mozilla|adobe|"
    r"crl\.|/pki/|certs/|Typography|app\.netlify\.com|github\.com/?$|github\.com,|"
    r"google\.com/maps|maps\.google", re.I)

LIVE_HOST = re.compile(r"github\.io|netlify\.app|vercel\.app|pages\.dev|web\.app|surge\.sh|firebaseapp|render\.com|onrender", re.I)

# Wanted hosts are never discarded as noise (repo/page names may contain library words like "openlayers").
WANTED = re.compile(r"github\.com|github\.io|netlify\.app|vercel\.app|pages\.dev|web\.app|surge\.sh|firebaseapp|render\.com|onrender", re.I)
# Always drop these even on a wanted host (bundled-library false positives seen in some PDFs).
HARD_NOISE = re.compile(r"andre-fuchs|kerning-pairs", re.I)


def extract_urls(pdf):
    out = []
    # 1) visible text (layout keeps URLs more intact on one line)
    for mode in ("-layout", "-raw"):
        try:
            t = subprocess.run(["pdftotext", mode, pdf, "-"], capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
            out.append(t)
        except Exception:
            pass
    # 2) decompressed annotations (clickable hyperlinks) via qpdf
    try:
        q = subprocess.run(["qpdf", "--qdf", "--object-streams=disable", pdf, "-"], capture_output=True, timeout=60).stdout.decode("utf-8", "ignore")
        out.append(q)
    except Exception:
        pass
    blob = "\n".join(out)
    raw = re.findall(r"https?://[^\s)>\"'<\]}]+", blob)
    urls = set()
    for u in raw:
        u = u.rstrip(".,);:'\"")
        if not u or HARD_NOISE.search(u):
            continue
        if WANTED.search(u) or not NOISE.search(u):
            urls.add(u)
    return urls


def norm_repo(u):
    m = re.search(r"github\.com/([\w.-]+)/([\w.-]+)", u, re.I)
    if not m:
        return None
    user, repo = m.group(1), m.group(2)
    repo = re.sub(r"\.git$", "", repo)
    if user.lower() in ("andre-fuchs",):
        return None
    return f"https://github.com/{user}/{repo}"


def pick_longest(cands):
    # prefer full (non-trailing-hyphen) and longest
    if not cands:
        return ""
    cands = sorted(cands, key=lambda x: (x.rstrip("/").endswith("-"), -len(x)))
    return cands[0]


# Manual findings for image-only PDFs (links inside browser screenshots, read visually).
# keyed by student_id -> (github_repo, live_url, note)
OVERRIDES = {
    "7751739": ("https://github.com/angelifitranouvalatifah-cmd/angel", "", "repo from screenshot; gh-pages deployment active but live URL not shown (likely https://angelifitranouvalatifah-cmd.github.io/angel/ - verify)"),
    "7751725": ("https://github.com/vishnutama491-creator/ErlanggaKharismaSigWeb", "https://vishnutama491-creator.github.io/ErlanggaKharismaSigWeb/", "both read from gh-pages settings screenshot"),
    "7751711": ("https://github.com/farizalnalendra/final-projects-gweb", "https://farizalnalendra.github.io/final-projects-gweb/", "links from screenshots; live page showed 404 at capture time"),
    "7751746": ("", "", "no link - results page blank, not deployed"),
    "7751716": ("", "", "ran locally (file://), no repo/deployment"),
    "7751713": ("", "", "ran locally (file://), not deployed"),
    "7751721": ("", "", "ran locally (file://), not deployed"),
    "7751749": ("", "", "ran locally (file://), not deployed"),
    "7751742": ("", "", "ran locally (file://), not deployed"),
    "7751728": ("", "", "no URLs; deployment only mentioned generically"),
    "7751705": ("", "", "code only, no repo/deployment link"),
}

rows = []
for d in sorted(os.listdir(BASE)):
    full = os.path.join(BASE, d)
    if not os.path.isdir(full):
        continue
    parts = d.split("_")
    name = parts[0].strip()
    sid = parts[1].strip() if len(parts) > 1 else ""
    pdfs = glob.glob(os.path.join(full, "*.pdf"))
    repo = live = ""
    other = []
    if pdfs:
        urls = extract_urls(pdfs[0])
        repos = {norm_repo(u) for u in urls if norm_repo(u)}
        lives = {u for u in urls if LIVE_HOST.search(u)}
        repo = pick_longest(list(repos))
        live = pick_longest(list(lives))
        for u in urls:
            if "drive.google.com" in u.lower():
                other.append(u)
    note = ""
    if not repo and not live:
        note = "NO LINK in text (likely in screenshot/image)"
        if other:
            note = "Google Drive only: " + pick_longest(other)
    elif not live and other:
        note = "live link maybe in Drive: " + pick_longest(other)
    # apply manual overrides (visual reads of image-only PDFs)
    if sid in OVERRIDES:
        repo, live, note = OVERRIDES[sid]
    # derive repo from a github.io Pages URL when no explicit repo was found
    if not repo and live:
        m = re.match(r"https?://([\w.-]+)\.github\.io/?([\w.-]+)?", live, re.I)
        if m:
            user = m.group(1)
            page_repo = m.group(2)
            repo = f"https://github.com/{user}/{page_repo}" if page_repo else f"https://github.com/{user}/{user}.github.io"
            note = (note + "; " if note else "") + "repo derived from Pages URL"
    rows.append([sid, name, repo, live, note])

rows.sort(key=lambda r: r[1].lower())
out_csv = os.path.join(os.path.dirname(BASE), "week7_recap.csv")
with open(out_csv, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["student_id", "name", "github_repo", "live_url", "notes"])
    w.writerows(rows)

# readable markdown table
out_md = os.path.join(os.path.dirname(BASE), "week7_recap.md")
with open(out_md, "w", encoding="utf-8") as f:
    f.write("# Week 7 Submission Recap\n\n")
    f.write(f"Total submissions: {len(rows)}\n\n")
    f.write("| # | Student ID | Name | GitHub Repo | Live URL | Notes |\n")
    f.write("|---|---|---|---|---|---|\n")
    for i, r in enumerate(rows, 1):
        repo = f"[repo]({r[2]})" if r[2] else "—"
        live = f"[live]({r[3]})" if r[3] else "—"
        f.write(f"| {i} | {r[0]} | {r[1]} | {repo} | {live} | {r[4]} |\n")

# ---- published web page (homework/index.html at repo root) ----
REPO_ROOT = os.path.dirname(os.path.dirname(BASE))
hw_dir = os.path.join(REPO_ROOT, "homework")
os.makedirs(hw_dir, exist_ok=True)

n_repo = sum(1 for r in rows if r[2])
n_live = sum(1 for r in rows if r[3])
n_review = sum(1 for r in rows if not r[2] and not r[3])

trs = []
for i, (sid, name, repo, live, note) in enumerate(rows, 1):
    repo_cell = f'<a href="{html.escape(repo)}" target="_blank" rel="noopener">repo&nbsp;↗</a>' if repo else '<span class="none">—</span>'
    live_cell = f'<a href="{html.escape(live)}" target="_blank" rel="noopener">live&nbsp;↗</a>' if live else '<span class="none">—</span>'
    has_link = bool(repo or live)
    badge_cls, badge_txt = ("ok", "✓") if has_link else ("warn", "⚠")
    note_btn = (f'<button type="button" class="note-btn" onclick="toggleNote(this)" '
                f'aria-expanded="false" aria-label="Show note" title="Show note">i</button>') if note else ""
    note_div = f'<div class="note" hidden>{html.escape(note)}</div>' if note else ""
    inner = (f'<span class="statusline"><span class="badge {badge_cls}">{badge_txt}</span>{note_btn}</span>{note_div}')
    trs.append(
        f'    <tr class="{ "missing" if not has_link else "" }">'
        f'<td class="num" data-sort="{i}">{i}</td>'
        f'<td class="sid" data-sort="{html.escape(sid)}">{html.escape(sid)}</td>'
        f'<td class="name">{html.escape(name)}</td>'
        f'<td data-sort="{1 if repo else 0}">{repo_cell}</td>'
        f'<td data-sort="{1 if live else 0}">{live_cell}</td>'
        f'<td class="status" data-sort="{0 if not has_link else 1}" data-status="{ "review" if not has_link else "ok" }">{inner}</td></tr>'
    )
table_rows = "\n".join(trs)

page = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Homework — Web GIS 2026</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5; color: #333; padding: 2rem 1rem;
        }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        a.back {{ color: #2563eb; text-decoration: none; font-size: 0.85rem; }}
        a.back:hover {{ text-decoration: underline; }}
        h1 {{ font-size: 1.8rem; margin: 0.6rem 0 0.3rem; }}
        .subtitle {{ color: #666; font-size: 0.95rem; margin-bottom: 1rem; }}
        .stats {{ display: flex; gap: 0.6rem; flex-wrap: wrap; margin-bottom: 1.2rem; }}
        .stat {{ background: #fff; border-radius: 8px; padding: 0.5rem 0.9rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08); font-size: 0.85rem; }}
        .stat b {{ font-size: 1.1rem; display: block; }}
        .controls {{ display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; margin-bottom: 0.6rem; }}
        .search {{ flex: 1; min-width: 200px; max-width: 320px; padding: 0.5rem 0.8rem; font-size: 0.9rem;
            border: 1px solid #ddd; border-radius: 8px; }}
        .controls select {{ padding: 0.5rem 0.8rem; font-size: 0.9rem; border: 1px solid #ddd;
            border-radius: 8px; background: #fff; }}
        .table-wrap {{ background: #fff; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.08);
            overflow-x: auto; }}
        table {{ border-collapse: collapse; width: 100%; font-size: 0.85rem; }}
        thead th {{ position: sticky; top: 0; background: #f8fafc; text-align: left;
            padding: 0.7rem 0.8rem; border-bottom: 2px solid #e5e7eb; font-weight: 600;
            white-space: nowrap; cursor: pointer; user-select: none; }}
        thead th:hover {{ background: #eef2f7; }}
        thead th .arrow {{ color: #9ca3af; font-size: 0.7rem; margin-left: 0.2rem; }}
        thead th.sorted .arrow {{ color: #2563eb; }}
        td {{ padding: 0.6rem 0.8rem; border-bottom: 1px solid #f0f0f0; vertical-align: top; }}
        tbody tr:hover {{ background: #f9fafb; }}
        tr.missing {{ background: #fff7ed; }}
        tr.missing:hover {{ background: #ffedd5; }}
        td a {{ color: #2563eb; text-decoration: none; font-weight: 500; white-space: nowrap; }}
        td a:hover {{ text-decoration: underline; }}
        .num {{ color: #999; }}
        .sid {{ color: #555; font-variant-numeric: tabular-nums; }}
        .name {{ font-weight: 500; }}
        .none {{ color: #bbb; }}
        .statusline {{ display: inline-flex; align-items: center; gap: 0.45rem; }}
        .badge {{ display: inline-flex; align-items: center; justify-content: center;
            min-width: 1.5rem; height: 1.5rem; padding: 0 0.45rem; border-radius: 999px;
            font-size: 0.78rem; font-weight: 600; }}
        .badge.ok {{ background: #dcfce7; color: #15803d; }}
        .badge.warn {{ background: #fee2e2; color: #b91c1c; }}
        .note-btn {{ width: 1.25rem; height: 1.25rem; flex: none; border-radius: 50%;
            border: 1px solid #d1d5db; background: #fff; color: #6b7280;
            font-size: 0.72rem; font-family: Georgia, serif; font-style: italic; font-weight: 700;
            line-height: 1; cursor: pointer; display: inline-flex; align-items: center;
            justify-content: center; transition: all 0.12s; }}
        .note-btn:hover {{ border-color: #2563eb; color: #2563eb; }}
        .note-btn[aria-expanded="true"] {{ background: #2563eb; border-color: #2563eb; color: #fff; }}
        .note {{ display: block; color: #92400e; font-size: 0.75rem; margin-top: 0.35rem;
            max-width: 280px; background: #fffbeb; border: 1px solid #fde68a;
            border-radius: 6px; padding: 0.35rem 0.5rem; word-break: break-word; }}
        .note[hidden] {{ display: none; }}
        footer {{ text-align: center; margin-top: 1.5rem; color: #999; font-size: 0.8rem; }}
        .legend {{ color: #888; font-size: 0.78rem; margin-bottom: 1rem; }}
    </style>
</head>
<body>
    <div class="container">
        <a class="back" href="../">← Back to course materials</a>
        <h1>📋 Homework — Week 7</h1>
        <p class="subtitle">Mini WebGIS assignment submissions — GitHub repository &amp; live deployment links</p>

        <div class="stats">
            <div class="stat"><b>{len(rows)}</b> submissions</div>
            <div class="stat"><b>{n_repo}</b> with repo</div>
            <div class="stat"><b>{n_live}</b> with live site</div>
            <div class="stat"><b>{n_review}</b> need review</div>
        </div>

        <div class="controls">
            <input class="search" id="q" type="search" placeholder="Search name or ID…" oninput="filterRows()">
            <select id="statusFilter" onchange="filterRows()">
                <option value="">All statuses</option>
                <option value="ok">✓ Has link</option>
                <option value="review">⚠ Needs review</option>
            </select>
        </div>
        <p class="legend">Click a column header to sort &nbsp;·&nbsp; ✓ = link(s) found &nbsp;·&nbsp; ⚠ = no link found &nbsp;·&nbsp; click the <i>i</i> button to show/hide a note.</p>

        <div class="table-wrap">
        <table>
            <thead><tr>
                <th onclick="sortBy(0,'num')">#<span class="arrow"></span></th>
                <th onclick="sortBy(1,'num')">Student ID<span class="arrow"></span></th>
                <th onclick="sortBy(2,'text')">Name<span class="arrow"></span></th>
                <th onclick="sortBy(3,'num')">Repo<span class="arrow"></span></th>
                <th onclick="sortBy(4,'num')">Live<span class="arrow"></span></th>
                <th onclick="sortBy(5,'num')">Status<span class="arrow"></span></th>
            </tr></thead>
            <tbody id="tbody">
{table_rows}
            </tbody>
        </table>
        </div>

        <footer>Generated from submission PDFs · Web GIS 2026 · Ismail Sunni</footer>
    </div>
    <script>
        function toggleNote(btn) {{
            const note = btn.closest('td').querySelector('.note');
            const show = note.hasAttribute('hidden');
            if (show) note.removeAttribute('hidden'); else note.setAttribute('hidden', '');
            btn.setAttribute('aria-expanded', show ? 'true' : 'false');
        }}
        function filterRows() {{
            const q = document.getElementById('q').value.toLowerCase();
            const st = document.getElementById('statusFilter').value;
            for (const tr of document.querySelectorAll('#tbody tr')) {{
                const matchText = tr.textContent.toLowerCase().includes(q);
                const matchStatus = !st || tr.children[5].dataset.status === st;
                tr.style.display = (matchText && matchStatus) ? '' : 'none';
            }}
        }}
        let sortState = {{ col: null, dir: 1 }};
        function sortBy(col, type) {{
            const tbody = document.getElementById('tbody');
            const rows = Array.from(tbody.querySelectorAll('tr'));
            sortState.dir = (sortState.col === col) ? -sortState.dir : 1;
            sortState.col = col;
            const val = (tr) => {{
                const cell = tr.children[col];
                const v = cell.dataset.sort !== undefined ? cell.dataset.sort : cell.textContent.trim();
                return type === 'num' ? parseFloat(v) : v.toLowerCase();
            }};
            rows.sort((a, b) => {{
                const x = val(a), y = val(b);
                if (x < y) return -1 * sortState.dir;
                if (x > y) return  1 * sortState.dir;
                return 0;
            }});
            rows.forEach(r => tbody.appendChild(r));
            document.querySelectorAll('thead th').forEach((th, i) => {{
                th.classList.toggle('sorted', i === col);
                th.querySelector('.arrow').textContent = i === col ? (sortState.dir === 1 ? '▲' : '▼') : '';
            }});
        }}
    </script>
</body>
</html>
"""
out_html = os.path.join(hw_dir, "week-7.html")
with open(out_html, "w", encoding="utf-8") as f:
    f.write(page)
print("HTML ->", out_html)

# print summary
missing = [r for r in rows if not r[2] and not r[3]]
print(f"Total: {len(rows)} | with repo: {sum(1 for r in rows if r[2])} | with live: {sum(1 for r in rows if r[3])} | missing both: {len(missing)}")
print("CSV ->", out_csv)
print("\n--- needs attention ---")
for r in rows:
    if not r[2] and not r[3]:
        print(f"  {r[0]}  {r[1]:35}  {r[4]}")
