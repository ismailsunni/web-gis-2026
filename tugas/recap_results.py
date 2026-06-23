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
# The HTML template (incl. the UAS column) lives in render_results.py so there
# is a single source for the page, shared with manual re-renders. It reads the
# results_recap.csv we just wrote plus uas/uas-results.csv.
import render_results
render_results.build()
