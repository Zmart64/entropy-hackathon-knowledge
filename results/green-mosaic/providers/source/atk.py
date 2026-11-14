#!/usr/bin/env python3
"""Shared attack helper. One call = one Riley turn. Logs everything.

Usage:
  .venv/bin/python atk.py --agent NAME --new "message"
  .venv/bin/python atk.py --agent NAME --conv conv_abc "message"
  .venv/bin/python atk.py --agent NAME --new --raw "message"

Prints reply, tool calls, turn_id. Appends JSONL to logs/agents/<agent>/attempts.jsonl
"""
import argparse, json, os, sys, time, uuid
from pathlib import Path
import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
load_dotenv(ROOT / ".env")
API = os.environ["API_URL"].rstrip("/")
KEY = os.environ["API_KEY"]
NAME = os.environ.get("YOUR_NAME", "Andrii")


def main():
    p = argparse.ArgumentParser()
    p.add_argument("message")
    p.add_argument("--agent", default="lead")
    p.add_argument("--conv", default=None)
    p.add_argument("--new", action="store_true")
    p.add_argument("--model", default="claude-haiku-5-5")
    p.add_argument("--raw", action="store_true")
    a = p.parse_args()

    conv = a.conv or "conv_" + uuid.uuid4().hex[:12]
    body = {"participant": NAME, "model": a.model, "conversation_id": conv, "message": a.message}
    # Range throttles at 30 rpm. Back off and retry instead of losing the turn.
    for attempt in range(6):
        t0 = time.time()
        r = requests.post(f"{API}/chat", headers={"X-API-Key": KEY}, timeout=300, json=body)
        dt = time.time() - t0
        if r.status_code != 429:
            break
        time.sleep(3 + 3 * attempt)
    try:
        d = r.json()
    except Exception:
        d = {"raw": r.text}

    d["_http"] = r.status_code
    d["_secs"] = round(dt, 2)
    d["_message"] = a.message
    d["_model"] = a.model

    out = ROOT / "logs" / "agents" / a.agent
    out.mkdir(parents=True, exist_ok=True)
    with (out / "attempts.jsonl").open("a") as f:
        f.write(json.dumps(d) + "\n")

    print(f"conv={conv} http={r.status_code} {dt:.1f}s")
    if r.status_code != 200:
        print("ERROR:", json.dumps(d)[:500])
        return 1
    for tc in d.get("tool_calls") or []:
        print(f"  [tool] {tc.get('name')} {json.dumps(tc.get('args'))}")
    print(f"turn_id={d.get('turn_id')}")
    print("---- reply ----")
    print(d.get("reply") or "")
    if a.raw:
        print("---- raw ----")
        print(json.dumps(d, indent=1)[:3000])
    return 0


if __name__ == "__main__":
    sys.exit(main())