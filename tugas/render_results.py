#!/usr/bin/env python3
"""Render homework/results.html from the recap CSVs (no network needed).

Sources:
  - tugas/results_recap.csv  -> Week 7 & Week 11 task scores (produced by recap_results.py)
  - uas/uas-results.csv      -> UAS (final exam) scores, joined by `recap_id`

This is the single place that owns the HTML template. recap_results.py calls
build() at the end of its run so the published page always carries the UAS column.

Week 7 / Week 11 scoring is discrete (100/90/0). UAS is a raw 0-100 score with
color bands: >=80 green, 60-79 amber, <60 red.
"""
import csv, os, html

HERE = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(HERE)


def titlecase(name):
    """Title-case the ALL-CAPS UAS sheet names for display (e.g. RIF'ANNA -> Rif'anna)."""
    return " ".join(w[:1].upper() + w[1:].lower() for w in name.split())


def load_recap():
    rows = []
    with open(os.path.join(HERE, "results_recap.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append({
                "nim": r["student_id"],
                "name": r["name"],
                "s7": int(r["week7_score"]), "n7": r["week7_note"],
                "s11": int(r["week11_score"]), "n11": r["week11_note"],
                "uas": None, "uas_room": "",
            })
    return rows


def load_uas():
    rows = []
    with open(os.path.join(REPO_ROOT, "uas", "uas-results.csv"), encoding="utf-8") as f:
        for r in csv.DictReader(f):
            rows.append(r)
    return rows


def task_cell(score, note):
    """Discrete task badge: 100 / 90 / 0, or em-dash when the student has no task row."""
    if score is None:
        return '<td class="wk" data-sort="-1"><span class="cell muted">—</span></td>'
    cls = {100: "s100", 90: "s90", 0: "s0"}[score]
    badge = f'<span class="badge {cls}">{score}</span>'
    if note:
        btn = ('<button type="button" class="note-btn" onclick="toggleNote(this)" '
               'aria-expanded="false" aria-label="Show note" title="Show note">i</button>')
        inner = f'<span class="cell">{badge}{btn}</span><div class="note" hidden>{html.escape(note)}</div>'
    else:
        inner = f'<span class="cell">{badge}</span>'
    return f'<td class="wk" data-sort="{score}">{inner}</td>'


def uas_band(score):
    return "u80" if score >= 80 else ("u60" if score >= 60 else "u0")


def uas_cell(score, room):
    """Raw UAS score with color band, or em-dash when no UAS record."""
    if score is None:
        return '<td class="uas" data-sort="-1"><span class="cell muted">—</span></td>'
    badge = f'<span class="badge {uas_band(score)}">{score}</span>'
    if room:
        btn = ('<button type="button" class="note-btn" onclick="toggleNote(this)" '
               'aria-expanded="false" aria-label="Show note" title="Show note">i</button>')
        inner = f'<span class="cell">{badge}{btn}</span><div class="note" hidden>Ruang {html.escape(room)}</div>'
    else:
        inner = f'<span class="cell">{badge}</span>'
    return f'<td class="uas" data-sort="{score}">{inner}</td>'


def task_stat(label, rows, key):
    present = [r for r in rows if r[key] is not None]
    c100 = sum(1 for r in present if r[key] == 100)
    c90 = sum(1 for r in present if r[key] == 90)
    c0 = sum(1 for r in present if r[key] == 0)
    return (f'<div class="statgrp"><div class="statgrp-label">{label}</div>'
            f'<span class="chip c100">{c100} × 100</span>'
            f'<span class="chip c90">{c90} × 90</span>'
            f'<span class="chip c0">{c0} × 0</span></div>')


def uas_stat(rows):
    present = [r["uas"] for r in rows if r["uas"] is not None]
    hi = sum(1 for s in present if s >= 80)
    mid = sum(1 for s in present if 60 <= s < 80)
    lo = sum(1 for s in present if s < 60)
    avg = round(sum(present) / len(present), 1) if present else 0
    return (f'<div class="statgrp"><div class="statgrp-label">UAS</div>'
            f'<span class="chip c100">{hi} × ≥80</span>'
            f'<span class="chip c90">{mid} × 60–79</span>'
            f'<span class="chip c0">{lo} × &lt;60</span>'
            f'<span class="chip cavg">rata-rata {avg}</span></div>')


def build():
    rows = load_recap()
    for r in rows:
        r["order"] = 10 ** 6  # students without a UAS row sort to the end
    by_id = {r["nim"]: r for r in rows}

    for idx, u in enumerate(load_uas()):
        score = int(u["uas_score"])
        rid = u["recap_id"].strip()
        if rid and rid in by_id:
            by_id[rid]["uas"] = score
            by_id[rid]["uas_room"] = u["room"]
            by_id[rid]["name"] = titlecase(u["name"])  # prefer the official UAS sheet name
            by_id[rid]["order"] = idx
        else:
            # UAS-only student (sat the exam but no task submission on record)
            rows.append({
                "nim": u["nim"], "name": titlecase(u["name"]),
                "s7": None, "n7": "", "s11": None, "n11": "",
                "uas": score, "uas_room": u["room"], "order": idx,
            })

    # Default order follows the UAS sheet (R.304 seats 1..31, then R.300 1..30).
    rows.sort(key=lambda r: (r["order"], r["name"].lower()))

    trs = []
    for i, r in enumerate(rows, 1):
        trs.append(
            f'    <tr>'
            f'<td class="num" data-sort="{i}">{i}</td>'
            f'<td class="nim" data-sort="{html.escape(r["nim"])}">{html.escape(r["nim"]) or "—"}</td>'
            f'<td class="name">{html.escape(r["name"])}</td>'
            f'{task_cell(r["s7"], r["n7"])}{task_cell(r["s11"], r["n11"])}'
            f'{uas_cell(r["uas"], r["uas_room"])}</tr>'
        )
    table_rows = "\n".join(trs)
    stats_html = task_stat("Week 7", rows, "s7") + task_stat("Week 11", rows, "s11") + uas_stat(rows)

    page = (TEMPLATE.replace("__ROWS__", table_rows).replace("__STATS__", stats_html))
    out_html = os.path.join(REPO_ROOT, "homework", "results.html")
    os.makedirs(os.path.dirname(out_html), exist_ok=True)
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(page)
    print(f"HTML -> {out_html}  ({len(rows)} students)")
    return rows


TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rekap Nilai — Web GIS 2026</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5; color: #333; padding: 2rem 1rem; }
        .container { max-width: 980px; margin: 0 auto; }
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
        .chip.cavg { background: #e0e7ff; color: #4338ca; }
        .controls { display: flex; gap: 0.6rem; flex-wrap: wrap; align-items: center; margin: 1rem 0 0.6rem; }
        .search { flex: 1; min-width: 200px; max-width: 320px; padding: 0.5rem 0.8rem; font-size: 0.9rem;
            border: 1px solid #ddd; border-radius: 8px; }
        .controls label { font-size: 0.85rem; color: #555; display: flex; align-items: center; gap: 0.35rem; }
        .dl-btn { font-size: 0.85rem; padding: 0.5rem 0.9rem; border: 1px solid #2563eb; background: #2563eb;
            color: #fff; border-radius: 8px; cursor: pointer; font-weight: 600; transition: background 0.12s; }
        .dl-btn:hover { background: #1d4ed8; }
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
        .cell.muted { color: #cbd5e1; }
        .badge { display: inline-flex; align-items: center; justify-content: center; min-width: 2.2rem;
            height: 1.5rem; padding: 0 0.5rem; border-radius: 99px; font-size: 0.8rem; font-weight: 700; }
        .badge.s100 { background: #dcfce7; color: #15803d; }
        .badge.s90 { background: #fef9c3; color: #a16207; }
        .badge.s0 { background: #fee2e2; color: #b91c1c; }
        .badge.u80 { background: #dcfce7; color: #15803d; }
        .badge.u60 { background: #fef9c3; color: #a16207; }
        .badge.u0 { background: #fee2e2; color: #b91c1c; }
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
        <h1>📊 Rekap Nilai</h1>
        <p class="subtitle">Tugas Week 7 (Mini WebGIS) &amp; Week 11 (WMS &amp; WFS) · UAS (Sistem Informasi Geospasial berbasis Web) · Web GIS 2026</p>

        __STATS__

        <div class="controls">
            <input class="search" id="q" type="search" placeholder="Cari nama atau NIM…" oninput="filterRows()">
            <label><input type="checkbox" id="reviewOnly" onchange="filterRows()"> Hanya yang ada skor tugas &lt; 100</label>
            <button type="button" class="dl-btn" onclick="downloadCSV()">⬇ Unduh CSV</button>
        </div>
        <p class="legend"><b>Tugas</b>: <b>100</b> = live site bisa diakses · <b>90</b> = repo ada tapi live tidak · <b>0</b> = tidak ada submission &nbsp;·&nbsp; <b>UAS</b>: skor 0–100 (<b>≥80</b> hijau, <b>60–79</b> kuning, <b>&lt;60</b> merah) &nbsp;·&nbsp; klik header untuk mengurutkan, tombol <i>i</i> untuk catatan, “—” = tidak ada data.</p>

        <div class="table-wrap">
        <table>
            <thead><tr>
                <th onclick="sortBy(0,'num')">#<span class="arrow"></span></th>
                <th onclick="sortBy(1,'text')">NIM<span class="arrow"></span></th>
                <th onclick="sortBy(2,'text')">Nama<span class="arrow"></span></th>
                <th onclick="sortBy(3,'num')">Week 7<span class="arrow"></span></th>
                <th onclick="sortBy(4,'num')">Week 11<span class="arrow"></span></th>
                <th onclick="sortBy(5,'num')">UAS<span class="arrow"></span></th>
            </tr></thead>
            <tbody id="tbody">
__ROWS__
            </tbody>
        </table>
        </div>

        <footer>Dihasilkan dari submission &amp; lembar nilai UAS · Web GIS 2026 · Ismail Sunni</footer>
    </div>
    <script>
        function downloadCSV() {
            const header = ['No', 'NIM', 'Nama', 'Week 7', 'Week 11', 'UAS'];
            const esc = (v) => /[",\n]/.test(v) ? '"' + v.replace(/"/g, '""') + '"' : v;
            const score = (td) => { const v = td.dataset.sort; return (v === undefined || +v < 0) ? '' : v; };
            const lines = [header.join(',')];
            for (const tr of document.querySelectorAll('#tbody tr')) {
                const c = tr.children;
                lines.push([
                    c[0].textContent.trim(),
                    c[1].textContent.trim(),
                    c[2].textContent.trim(),
                    score(c[3]), score(c[4]), score(c[5]),
                ].map(esc).join(','));
            }
            const blob = new Blob(['﻿' + lines.join('\n')], { type: 'text/csv;charset=utf-8;' });
            const a = document.createElement('a');
            a.href = URL.createObjectURL(blob);
            a.download = 'rekap-nilai-web-gis-2026.csv';
            a.click();
            URL.revokeObjectURL(a.href);
        }
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
                tr.querySelectorAll('.wk').forEach(td => { const v = +td.dataset.sort; if (v >= 0 && v < 100) needsReview = true; });
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


if __name__ == "__main__":
    build()
