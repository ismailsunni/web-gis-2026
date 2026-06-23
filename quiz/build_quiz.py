#!/usr/bin/env python3
"""Build an interactive quiz page (quiz/index.html) from soal-ogc-lbs.md.

Parses the 50 multiple-choice questions + answer key and emits a self-contained,
client-side quiz: take it as a test, then submit to see the score and a review."""
import os, re, json, html

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "soal-ogc-lbs.md")
OUT = os.path.join(HERE, "index.html")


def fmt(text):
    """Escape HTML, then turn `code` spans into <code>."""
    text = html.escape(text.strip())
    text = re.sub(r"`([^`]+)`", r"<code>\1</code>", text)
    return text


def parse(md):
    questions = []
    section = ""
    cur = None
    q_re = re.compile(r"^\*\*(\d+)\.\s*(.*?)\*\*\s*$")
    opt_re = re.compile(r"^([A-D])\.\s+(.*)$")
    for line in md.splitlines():
        s = line.strip()
        if s.startswith("## Bagian"):
            # "## Bagian A — OGC Services (WMS & WFS) — Soal 1–30"
            m = re.search(r"Bagian\s+\w+\s*—\s*(.+?)\s*—", s)
            section = m.group(1).strip() if m else s
            cur = None
            continue
        if s.startswith("## Kunci"):
            cur = None
            break  # answer key parsed separately below
        qm = q_re.match(s)
        if qm:
            cur = {"n": int(qm.group(1)), "section": section,
                   "q": fmt(qm.group(2)), "opts": [], "ans": ""}
            questions.append(cur)
            continue
        om = opt_re.match(s)
        if om and cur is not None:
            cur["opts"].append({"k": om.group(1), "t": fmt(om.group(2))})
    return questions


def parse_key(md):
    key = {}
    after = md.split("## Kunci", 1)[1] if "## Kunci" in md else ""
    for line in after.splitlines():
        if not line.strip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        cells = [c for c in cells if c]
        # skip header/separator rows
        if not cells or cells[0].lower() in ("no", "") or set(cells[0]) <= set("-"):
            continue
        # cells are repeated (No, Jwb) pairs
        for i in range(0, len(cells) - 1, 2):
            num, ans = cells[i], cells[i + 1]
            if num.isdigit() and ans in "ABCD":
                key[int(num)] = ans
    return key


md = open(SRC, encoding="utf-8").read()
questions = parse(md)
key = parse_key(md)
for q in questions:
    q["ans"] = key.get(q["n"], "")

# sanity checks
missing = [q["n"] for q in questions if not q["ans"] or len(q["opts"]) != 4]
assert len(questions) == 50, f"expected 50 questions, got {len(questions)}"
assert not missing, f"questions with missing answer/options: {missing}"

sections = []
for q in questions:
    if q["section"] not in sections:
        sections.append(q["section"])

QUESTIONS_JSON = json.dumps(questions, ensure_ascii=False)

TEMPLATE = r"""<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Quiz UAS — OGC Services & LBS · Web GIS 2026</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: #f5f5f5; color: #333; padding: 0 1rem 4rem;
        }
        .container { max-width: 760px; margin: 0 auto; padding-top: 1.5rem; }
        a.back { color: #2563eb; text-decoration: none; font-size: 0.85rem; }
        a.back:hover { text-decoration: underline; }
        h1 { font-size: 1.6rem; margin: 0.6rem 0 0.3rem; }
        .subtitle { color: #666; font-size: 0.92rem; margin-bottom: 1rem; }
        .intro { background: #fff; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 1.2rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08); font-size: 0.88rem; color: #555; }
        .intro ul { margin: 0.5rem 0 0 1.1rem; }
        .controls { display: flex; gap: 0.6rem; align-items: center; flex-wrap: wrap; margin-bottom: 1rem; }
        .controls label { font-size: 0.85rem; color: #555; display: flex; align-items: center; gap: 0.35rem; }
        .q { background: #fff; border-radius: 10px; padding: 1rem 1.2rem; margin-bottom: 0.9rem;
            box-shadow: 0 1px 3px rgba(0,0,0,0.08); border-left: 4px solid transparent; }
        .q.correct { border-left-color: #16a34a; }
        .q.wrong { border-left-color: #dc2626; }
        .q-head { display: flex; gap: 0.55rem; margin-bottom: 0.7rem; font-size: 0.95rem; line-height: 1.45; }
        .q-num { flex: none; width: 1.7rem; height: 1.7rem; border-radius: 50%; background: #eef2f7;
            color: #475569; font-weight: 700; font-size: 0.8rem; display: inline-flex;
            align-items: center; justify-content: center; }
        .q-text { font-weight: 500; }
        .tag { display: inline-block; font-size: 0.66rem; font-weight: 600; text-transform: uppercase;
            letter-spacing: 0.03em; color: #64748b; background: #f1f5f9; border-radius: 4px;
            padding: 0.05rem 0.4rem; margin-top: 0.25rem; }
        .opts { display: flex; flex-direction: column; gap: 0.4rem; }
        .opt { display: flex; align-items: flex-start; gap: 0.55rem; padding: 0.5rem 0.65rem;
            border: 1px solid #e5e7eb; border-radius: 8px; cursor: pointer; font-size: 0.88rem;
            transition: background 0.12s, border-color 0.12s; }
        .opt:hover { background: #f8fafc; }
        .opt input { margin-top: 0.15rem; flex: none; }
        .opt .key { font-weight: 700; color: #475569; flex: none; }
        .opt.pick-correct { background: #dcfce7; border-color: #16a34a; }
        .opt.pick-wrong { background: #fee2e2; border-color: #dc2626; }
        .opt.reveal-correct { border-color: #16a34a; }
        .opt.reveal-correct .key { color: #16a34a; }
        code { background: #f1f5f9; padding: 0.05rem 0.3rem; border-radius: 4px;
            font-size: 0.85em; color: #be123c; }
        .actions { margin: 1.4rem 0; display: flex; gap: 0.7rem; flex-wrap: wrap; }
        button { font-size: 0.92rem; font-weight: 600; padding: 0.6rem 1.3rem; border-radius: 8px;
            border: none; cursor: pointer; }
        .btn-primary { background: #2563eb; color: #fff; }
        .btn-primary:hover { background: #1d4ed8; }
        .btn-ghost { background: #fff; color: #2563eb; border: 1px solid #cbd5e1; }
        .btn-ghost:hover { background: #f8fafc; }
        .btn-sm { padding: 0.4rem 0.9rem; font-size: 0.82rem; }
        .btn-ghost.active { background: #2563eb; color: #fff; border-color: #2563eb; }
        .btn-ghost:disabled { opacity: 0.5; cursor: not-allowed; }
        .empty-state { background: #fff; border-radius: 10px; padding: 1.4rem; text-align: center;
            color: #64748b; font-size: 0.9rem; box-shadow: 0 1px 3px rgba(0,0,0,0.08); }
        .empty-state[hidden] { display: none; }
        /* sticky progress */
        .progress-bar { position: sticky; top: 0; z-index: 20; background: rgba(245,245,245,0.95);
            backdrop-filter: blur(4px); padding: 0.6rem 0; margin-bottom: 0.5rem; }
        .progress-track { height: 8px; background: #e5e7eb; border-radius: 99px; overflow: hidden; }
        .progress-fill { height: 100%; width: 0; background: #2563eb; transition: width 0.2s; }
        .progress-label { font-size: 0.78rem; color: #64748b; margin-top: 0.3rem; }
        /* result panel */
        .result { background: #fff; border-radius: 12px; padding: 1.4rem 1.5rem; margin-bottom: 1.2rem;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1); text-align: center; }
        .result[hidden] { display: none; }
        .score-big { font-size: 2.6rem; font-weight: 800; line-height: 1; }
        .score-pct { font-size: 1.1rem; color: #64748b; margin-top: 0.3rem; }
        .grade { display: inline-block; margin-top: 0.6rem; padding: 0.25rem 0.9rem; border-radius: 99px;
            font-size: 0.85rem; font-weight: 700; }
        .grade.pass { background: #dcfce7; color: #15803d; }
        .grade.fail { background: #fee2e2; color: #b91c1c; }
        .breakdown { display: flex; gap: 0.6rem; justify-content: center; flex-wrap: wrap; margin-top: 1rem; }
        .bd { background: #f8fafc; border-radius: 8px; padding: 0.5rem 0.9rem; font-size: 0.82rem; color: #475569; }
        .bd b { display: block; font-size: 1.1rem; color: #1e293b; }
        footer { text-align: center; margin-top: 2rem; color: #999; font-size: 0.8rem; }
    </style>
</head>
<body>
    <div class="container">
        <a class="back" href="../">← Kembali ke materi kuliah</a>
        <h1>📝 Quiz UAS — OGC Services &amp; LBS / Mobile GIS</h1>
        <p class="subtitle">CPMK-3 · __COUNT__ soal pilihan ganda · Web GIS 2026</p>

        <div class="intro">
            Kerjakan seluruh soal, lalu tekan <b>Selesai &amp; Lihat Nilai</b> untuk melihat skor dan pembahasan.
            <ul>
                <li>Pilih satu jawaban yang paling tepat untuk tiap soal.</li>
                <li>Nilai dan jawaban benar baru ditampilkan setelah kamu menekan tombol selesai.</li>
                <li>Gunakan <b>Acak urutan soal</b> bila ingin latihan dengan urutan berbeda.</li>
            </ul>
        </div>

        <div class="progress-bar">
            <div class="progress-track"><div class="progress-fill" id="fill"></div></div>
            <div class="progress-label" id="plabel">0 / __COUNT__ terjawab</div>
        </div>

        <div class="controls">
            <label><input type="checkbox" id="shuffle" onchange="render()"> Acak urutan soal</label>
            <button class="btn-ghost btn-sm" id="filterBtn" onclick="toggleFilter()">Tampilkan: Semua soal</button>
        </div>

        <div class="result" id="result" hidden></div>

        <div id="quiz"></div>
        <div class="empty-state" id="emptyState" hidden>🎉 Semua soal sudah dijawab. Tekan <b>Selesai &amp; Lihat Nilai</b> untuk melihat skor.</div>

        <div class="actions">
            <button class="btn-primary" id="submitBtn" onclick="submitQuiz()">Selesai &amp; Lihat Nilai</button>
            <button class="btn-ghost" onclick="resetQuiz()">Ulangi</button>
        </div>

        <footer>Web GIS 2026 · Ismail Sunni</footer>
    </div>

    <script>
        const QUESTIONS = __QUESTIONS__;
        const TOTAL = QUESTIONS.length;
        let order = QUESTIONS.map((_, i) => i);
        let submitted = false;
        let filterUnanswered = false;

        function shuffleArr(a) {
            for (let i = a.length - 1; i > 0; i--) {
                const j = Math.floor(Math.random() * (i + 1));
                [a[i], a[j]] = [a[j], a[i]];
            }
            return a;
        }

        function render() {
            submitted = false;
            filterUnanswered = false;
            const fb = document.getElementById('filterBtn');
            fb.disabled = false;
            fb.classList.remove('active');
            fb.textContent = 'Tampilkan: Semua soal';
            document.getElementById('result').hidden = true;
            document.getElementById('submitBtn').disabled = false;
            order = QUESTIONS.map((_, i) => i);
            if (document.getElementById('shuffle').checked) shuffleArr(order);
            const quiz = document.getElementById('quiz');
            quiz.innerHTML = '';
            for (const idx of order) {
                const q = QUESTIONS[idx];
                const opts = q.opts.map(o => `
                    <label class="opt" id="opt-${q.n}-${o.k}">
                        <input type="radio" name="q${q.n}" value="${o.k}" onchange="updateProgress()">
                        <span class="key">${o.k}.</span>
                        <span class="opt-text">${o.t}</span>
                    </label>`).join('');
                quiz.insertAdjacentHTML('beforeend', `
                    <div class="q" id="q${q.n}" data-ans="${q.ans}">
                        <div class="q-head">
                            <span class="q-num">${q.n}</span>
                            <span class="q-text">${q.q}<br><span class="tag">${q.section}</span></span>
                        </div>
                        <div class="opts">${opts}</div>
                    </div>`);
            }
            updateProgress();
            window.scrollTo({ top: 0 });
        }

        function answeredCount() {
            let n = 0;
            for (const q of QUESTIONS) if (document.querySelector(`input[name="q${q.n}"]:checked`)) n++;
            return n;
        }

        function updateProgress() {
            if (submitted) return;
            const n = answeredCount();
            document.getElementById('fill').style.width = (n / TOTAL * 100) + '%';
            document.getElementById('plabel').textContent = `${n} / ${TOTAL} terjawab`;
            applyFilter();
        }

        function applyFilter() {
            let visible = 0;
            for (const q of QUESTIONS) {
                const el = document.getElementById('q' + q.n);
                if (!el) continue;
                const answered = !!document.querySelector(`input[name="q${q.n}"]:checked`);
                const hide = filterUnanswered && !submitted && answered;
                el.style.display = hide ? 'none' : '';
                if (!hide) visible++;
            }
            document.getElementById('emptyState').hidden = !(filterUnanswered && !submitted && visible === 0);
        }

        function toggleFilter() {
            if (submitted) return;
            filterUnanswered = !filterUnanswered;
            const fb = document.getElementById('filterBtn');
            fb.classList.toggle('active', filterUnanswered);
            fb.textContent = filterUnanswered ? 'Tampilkan: Belum dijawab' : 'Tampilkan: Semua soal';
            applyFilter();
        }

        function submitQuiz() {
            if (submitted) return;
            const n = answeredCount();
            if (n < TOTAL && !confirm(`Masih ada ${TOTAL - n} soal belum dijawab. Tetap selesaikan?`)) return;
            submitted = true;
            document.getElementById('submitBtn').disabled = true;
            // show all questions for review and lock the filter
            filterUnanswered = false;
            const fb = document.getElementById('filterBtn');
            fb.disabled = true;
            fb.classList.remove('active');
            fb.textContent = 'Tampilkan: Semua soal';
            document.getElementById('emptyState').hidden = true;
            QUESTIONS.forEach(q => { const el = document.getElementById('q' + q.n); if (el) el.style.display = ''; });

            let score = 0;
            const bySection = {};
            for (const q of QUESTIONS) {
                bySection[q.section] = bySection[q.section] || { correct: 0, total: 0 };
                bySection[q.section].total++;
                const picked = document.querySelector(`input[name="q${q.n}"]:checked`);
                const pick = picked ? picked.value : null;
                const qEl = document.getElementById('q' + q.n);
                // lock inputs
                qEl.querySelectorAll('input').forEach(i => i.disabled = true);
                // reveal correct option
                document.getElementById(`opt-${q.n}-${q.ans}`).classList.add('reveal-correct');
                if (pick === q.ans) {
                    score++;
                    bySection[q.section].correct++;
                    qEl.classList.add('correct');
                    document.getElementById(`opt-${q.n}-${pick}`).classList.add('pick-correct');
                } else {
                    qEl.classList.add('wrong');
                    if (pick) document.getElementById(`opt-${q.n}-${pick}`).classList.add('pick-wrong');
                }
            }

            const pct = Math.round(score / TOTAL * 100);
            const pass = pct >= 60;
            const bd = Object.entries(bySection).map(([s, v]) =>
                `<div class="bd"><b>${v.correct}/${v.total}</b>${s}</div>`).join('');
            const res = document.getElementById('result');
            res.innerHTML = `
                <div class="score-big">${score} <span style="font-size:1.3rem;color:#94a3b8">/ ${TOTAL}</span></div>
                <div class="score-pct">${pct}% benar</div>
                <div class="grade ${pass ? 'pass' : 'fail'}">${pass ? 'LULUS' : 'BELUM LULUS'} (batas 60%)</div>
                <div class="breakdown">${bd}</div>
                <p style="margin-top:1rem;font-size:0.82rem;color:#64748b">Gulir ke bawah untuk melihat pembahasan tiap soal.</p>`;
            res.hidden = false;
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }

        function resetQuiz() {
            render();
        }

        render();
    </script>
</body>
</html>
"""

out = (TEMPLATE
       .replace("__QUESTIONS__", QUESTIONS_JSON)
       .replace("__COUNT__", str(len(questions))))
with open(OUT, "w", encoding="utf-8") as f:
    f.write(out)

print(f"Parsed {len(questions)} questions across sections: {sections}")
print("answers mapped:", sum(1 for q in questions if q['ans']))
print("HTML ->", OUT)
