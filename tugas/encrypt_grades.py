#!/usr/bin/env python3
"""Encrypt the sensitive fields of the grades CSV for publishing.

Workflow:
  1. Edit the PLAINTEXT source `tugas/grades.source.csv` (kept local / gitignored).
  2. Run `python3 tugas/encrypt_grades.py` and enter the reveal password.
  3. It writes `homework/grades.csv` with the sensitive fields encrypted
     (SHA-256 counter-mode keystream XOR, per-cell random nonce, base64).

Only these fields are encrypted; everything else (name, repo/live URLs,
room) stays readable:
  nim, w7_id, w11_id, w7_score, w7_note, w11_score, w11_note, uas_score

The password is never written anywhere — the key is derived from it at
run time. The page derives the same key in the browser to decrypt.
"""
import csv, os, hashlib, struct, base64, getpass, sys

SALT = "wg2026:"
ENC_FIELDS = ["nim", "w7_id", "w11_id", "w7_score", "w7_note", "w11_score", "w11_note", "uas_score"]
HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "grades.source.csv")
OUT = os.path.join(HERE, "..", "homework", "grades.csv")

def key_bytes(pw):
    return hashlib.sha256((SALT + pw).encode()).digest()

def keystream(key, nonce, n):
    out, i = b"", 0
    while len(out) < n:
        out += hashlib.sha256(key + nonce + struct.pack(">I", i)).digest()
        i += 1
    return out[:n]

def encrypt(key, plain):
    if plain == "":
        return ""
    nonce = os.urandom(8)
    pt = plain.encode()
    ks = keystream(key, nonce, len(pt))
    ct = bytes(a ^ b for a, b in zip(pt, ks))
    return base64.b64encode(nonce + ct).decode()

def main():
    if not os.path.exists(SOURCE):
        sys.exit("Missing %s — create it from homework/grades.csv (plaintext)." % SOURCE)
    pw = getpass.getpass("Reveal password: ")
    if hashlib.sha256(("verify:" + SALT + pw).encode()).hexdigest() != \
       "d099007c7be937cabe523cbf6004c6d2b403c1abf907b3fcaf11837276a1bccd":
        sys.exit("Password does not match the one baked into table.js (PW_CHECK). Aborting.")
    key = key_bytes(pw)
    rows = list(csv.DictReader(open(SOURCE)))
    cols = list(rows[0].keys())
    with open(OUT, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(cols)
        for r in rows:
            w.writerow([encrypt(key, r[c]) if c in ENC_FIELDS else r[c] for c in cols])
    print("Wrote %s (%d rows, encrypted: %s)" % (OUT, len(rows), ", ".join(ENC_FIELDS)))

if __name__ == "__main__":
    main()
