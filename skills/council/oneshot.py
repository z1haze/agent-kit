#!/usr/bin/env python3
"""One-shot council review through OpenRouter: one request, no tools.

  oneshot.py check
      Prints the key's remaining limit and the account's remaining credit as JSON. Exit 2 when no key is stored.

  oneshot.py review --model M --effort E --repo DIR --base SHA --brief FILE [--paths SPEC ...] [--include PATH ...]
                    [--max-usd X] [--max-output N]
      Sends the brief, `git diff <base>`, every changed or untracked file in full, and each --include file (the brief's
      Read-first docs) as one prompt. Prints {"reply", "cost_usd", "estimate_usd", "finish_reason", ...} as JSON.
      Exit 3 when the estimate exceeds --max-usd (nothing is sent), 4 when OpenRouter refuses or fails.

The key comes from OPENROUTER_API_KEY, or the macOS keychain (service "openrouter").
"""
import argparse
import json
import os
import subprocess
import sys
import urllib.error
import urllib.request

API = "https://openrouter.ai/api/v1"
FILE_CAP = 200_000  # characters per file; bigger files are listed, not included
TOTAL_CAP = 600_000  # characters for the whole prompt
CHARS_PER_TOKEN = 3.5  # conservative, so estimates run high

NOTE = """You are reviewing in one pass, with no tools: you can't open files or run commands. Everything you may use is
below: the brief, the diff, the full text of every changed file, and the docs the brief asks you to read. Where the
brief asks for evidence from a test or command you ran, cite the lines below instead, and name the test that would go
red. Reply in the brief's format and nothing else."""


def key():
    if os.environ.get("OPENROUTER_API_KEY"):
        return os.environ["OPENROUTER_API_KEY"]
    r = subprocess.run(["security", "find-generic-password", "-s", "openrouter", "-w"],
                       capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else None


def call(path, body=None, auth=True, timeout=900):
    req = urllib.request.Request(API + path, data=json.dumps(body).encode() if body is not None else None,
                                 method="POST" if body is not None else "GET")
    req.add_header("Content-Type", "application/json")
    if auth:
        req.add_header("Authorization", "Bearer " + key())
    with urllib.request.urlopen(req, timeout=timeout) as r:
        return json.load(r)


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True, check=True).stdout


def read(path):
    try:
        with open(path, encoding="utf-8") as f:
            text = f.read()
    except (UnicodeDecodeError, FileNotFoundError, IsADirectoryError):
        return None
    return text if len(text) <= FILE_CAP else None


def build_prompt(a):
    with open(a.brief, encoding="utf-8") as f:
        brief = f.read()
    spec = ["--", *a.paths] if a.paths else []
    diff = git(a.repo, "diff", a.base, *spec)
    changed = git(a.repo, "diff", "--name-only", a.base, *spec).split()
    untracked = git(a.repo, "ls-files", "--others", "--exclude-standard", *spec).split()
    parts = [NOTE, "# Brief\n\n" + brief, "# Diff\n\n```diff\n" + diff + "\n```"]
    skipped = []
    for title, paths in (("Changed and untracked files", changed + untracked), ("Read-first docs", a.include or [])):
        section = []
        for p in paths:
            text = read(os.path.join(a.repo, p))
            if text is None:
                skipped.append(p)
            else:
                section.append(f"## {p}\n\n```\n{text}\n```")
        if section:
            parts.append(f"# {title}\n\n" + "\n\n".join(section))
    if skipped:
        parts.append("Not included (deleted, binary or too large): " + ", ".join(skipped))
    prompt = "\n\n".join(parts)
    if len(prompt) > TOTAL_CAP:
        sys.exit(f"prompt is {len(prompt)} characters, over the {TOTAL_CAP} cap; narrow the target")
    return prompt, skipped


def price(model):
    for m in call("/models", auth=False)["data"]:
        if m["id"] == model:
            return float(m["pricing"]["prompt"]), float(m["pricing"]["completion"])
    sys.exit(f"unknown model {model}")


def check():
    if not key():
        print(json.dumps({"ok": False, "error": "no OpenRouter key stored"}))
        sys.exit(2)
    try:
        k = call("/key")["data"]
        c = call("/credits")["data"]
    except urllib.error.HTTPError as e:
        print(json.dumps({"ok": False, "error": f"HTTP {e.code}: {e.read().decode()[:300]}"}))
        sys.exit(4)
    credit = c["total_credits"] - c["total_usage"]
    print(json.dumps({"ok": True, "key_limit_remaining": k.get("limit_remaining"), "credit_remaining": credit}))


def review(a):
    if not key():
        sys.exit("no OpenRouter key stored")
    prompt, skipped = build_prompt(a)
    p_in, p_out = price(a.model)
    estimate = len(prompt) / CHARS_PER_TOKEN * p_in + a.max_output * p_out
    out = {"model": a.model, "effort": a.effort, "estimate_usd": round(estimate, 4), "skipped": skipped}
    if a.max_usd is not None and estimate > a.max_usd:
        out["error"] = f"estimate ${estimate:.2f} is over the ${a.max_usd:.2f} left in the budget; nothing sent"
        print(json.dumps(out))
        sys.exit(3)
    body = {"model": a.model, "messages": [{"role": "user", "content": prompt}],
            "reasoning": {"effort": a.effort}, "max_tokens": a.max_output, "usage": {"include": True}}
    try:
        r = call("/chat/completions", body)
    except urllib.error.HTTPError as e:
        out["error"] = f"HTTP {e.code}: {e.read().decode()[:500]}"
        print(json.dumps(out))
        sys.exit(4)
    choice = r["choices"][0]
    usage = r.get("usage", {})
    out.update(reply=choice["message"].get("content") or "", finish_reason=choice.get("finish_reason"),
               cost_usd=usage.get("cost"), prompt_tokens=usage.get("prompt_tokens"),
               completion_tokens=usage.get("completion_tokens"))
    print(json.dumps(out))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("check")
    r = sub.add_parser("review")
    r.add_argument("--model", required=True)
    r.add_argument("--effort", default="high")
    r.add_argument("--repo", required=True)
    r.add_argument("--base", required=True)
    r.add_argument("--brief", required=True)
    r.add_argument("--paths", nargs="*", help="limit the diff and files to these pathspecs (an audit area)")
    r.add_argument("--include", nargs="*")
    r.add_argument("--max-usd", type=float)
    r.add_argument("--max-output", type=int, default=32000)
    a = ap.parse_args()
    check() if a.cmd == "check" else review(a)


if __name__ == "__main__":
    main()
