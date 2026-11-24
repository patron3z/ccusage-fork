#!/usr/bin/env python3
"""List the heaviest ccusage sessions with their Claude Code titles. Local files only."""
import argparse, glob, json, os, shutil, subprocess, sys


def describe(path):
    title = first = None
    t0 = t1 = None
    for line in open(path, encoding="utf8", errors="replace"):
        try:
            d = json.loads(line)
        except ValueError:
            continue
        ts = d.get("timestamp")
        if ts:
            t0 = t0 or ts
            t1 = ts
        if d.get("type") in ("ai-title", "summary", "custom-title"):
            title = d.get("aiTitle") or d.get("summary") or d.get("customTitle") or title
        if d.get("type") == "user" and not d.get("isMeta") and first is None:
            c = d.get("message", {}).get("content")
            if isinstance(c, list):
                c = " ".join(x.get("text", "") for x in c if isinstance(x, dict) and x.get("type") == "text")
            if isinstance(c, str) and c.strip() and not c.startswith("<"):
                first = c.strip()[:100]
    return title, first, (t0 or "")[:10], (t1 or "")[:10]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--top", type=int, default=10)
    ap.add_argument("--projects", default=os.path.join(os.path.expanduser("~"), ".claude", "projects"))
    a = ap.parse_args()
    exe = shutil.which("ccusage")
    if not exe:
        sys.exit("ccusage not found. Install it with: npm install -g ccusage")
    out = subprocess.run([exe, "session", "--json"], capture_output=True, text=True, check=False)
    start = out.stdout.find("{")
    if start < 0:
        sys.exit("ccusage returned no JSON: " + out.stderr.strip()[:200])
    data = json.loads(out.stdout[start:])
    rows = data.get("sessions") or data.get("session") or []
    rows.sort(key=lambda s: -s.get("totalCost", 0))
    for s in rows[: a.top]:
        sid = str(s.get("sessionId") or s.get("period") or "")
        files = glob.glob(os.path.join(a.projects, "*", sid + ".jsonl"))
        title, first, d0, d1 = describe(files[0]) if files else (None, None, "", "")
        print(f"{s.get('totalCost', 0):8.2f} $  {s.get('totalTokens', 0):>14,} tok  {d0}..{d1}  {title or first or sid}")


if __name__ == "__main__":
    main()
