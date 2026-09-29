#!/usr/bin/env python3
"""Deterministic helpers for chronos-artemis: classify, normalise status, find free time, plan.

Standard library only (Python 3.9+). Every command reads arguments or a JSON file and
prints JSON, so the model can call it mid-task and trust the arithmetic.

    python chronos.py classify "Standup with design team at 10:00"
    python chronos.py status "in review" --type custom
    python chronos.py slots day.json
    python chronos.py plan day.json

day.json (times are ISO 8601 with an offset; all in one time zone):
    {
      "day_start": "2026-09-29T09:00:00+07:00",
      "day_end":   "2026-09-29T18:00:00+07:00",
      "min_block_minutes": 25,
      "buffer_minutes": 10,
      "busy": [{"start": "...", "end": "...", "title": "Standup"}],
      "tasks": [{"id": "abc", "name": "Write spec", "estimate_minutes": 90,
                 "priority": "high", "due": "2026-09-29", "status": "to do"}]
    }

The classifier is a first pass, not a verdict: it returns its signals and a confidence so
the model can overrule it, and it says "ask" when the signals conflict.
"""
import json
import re
import sys
from datetime import datetime, timedelta

# --------------------------------------------------------------------------- classify

TIME_RE = re.compile(
    r"\b(at|@|from)\s*\d{1,2}([:.]\d{2})?\s*(am|pm)?\b"
    r"|\b\d{1,2}[:.]\d{2}\b"
    r"|\b\d{1,2}\s*(am|pm)\b"
    r"|\b\d{1,2}\s*(-|to|–)\s*\d{1,2}(\s*(am|pm))?\b"
    r"|\bโมง\b|\bน\.\b",
    re.I,
)
DURATION_RE = re.compile(r"\b(for\s+)?\d+(\.\d+)?\s*(min|mins|minutes|h|hr|hrs|hours?)\b|\bชั่วโมง\b|\bนาที\b", re.I)
RECUR_RE = re.compile(
    r"\b(every|each|daily|weekly|weekdays|nightly|mornings?|evenings?|\d+\s*x\s*(a|per)\s*(week|day))\b"
    r"|ทุกวัน|ทุกสัปดาห์|ทุกเช้า|ทุกเย็น",
    re.I,
)
DEADLINE_RE = re.compile(r"\b(by|before|due|deadline|until|no later than)\b|ภายใน|ก่อนวัน|กำหนดส่ง|เดดไลน์", re.I)

SCHEDULE_WORDS = (
    "meeting", "meet ", "call", "standup", "stand-up", "sync", "1:1", "one-on-one", "interview",
    "appointment", "dentist", "doctor", "flight", "class", "lecture", "webinar", "workshop",
    "dinner", "lunch with", "party", "wedding", "conference", "demo day", "exam",
    "ประชุม", "นัด", "สัมภาษณ์", "เรียน", "สอบ", "บินไป", "งานเลี้ยง",
)
TASK_WORDS = (
    "write", "draft", "fix", "finish", "submit", "send", "review", "prepare", "prep ", "deploy",
    "ship", "publish", "book", "buy", "pay", "file", "update", "create", "design", "build",
    "implement", "migrate", "refactor", "reply", "call back", "email", "complete", "deliver",
    "เขียน", "แก้", "ส่ง", "ทำให้เสร็จ", "เตรียม", "จ่าย", "ซื้อ", "อัปเดต", "สร้าง", "ตรวจ",
)
ACTIVITY_WORDS = (
    "gym", "workout", "run ", "running", "yoga", "meditate", "meditation", "study", "practice",
    "practise", "read ", "reading", "learn", "deep work", "focus time", "focus block", "journal",
    "walk", "stretch", "language", "piano", "guitar", "habit", "routine", "work on", "time on",
    "ออกกำลังกาย", "วิ่ง", "อ่านหนังสือ", "นั่งสมาธิ", "ฝึก", "ทบทวน", "โฟกัส",
)
WITH_PERSON_RE = re.compile(r"\bwith\s+[A-Z@]|\bกับ", re.U)


def _hits(text, words):
    low = " " + text.lower() + " "
    return [w.strip() for w in words if w in low]


def classify(text):
    """Return {kind, confidence, signals, ask} for one captured item.

    kind is "schedule", "task", "activity" or "ask" (signals conflict — ask the user one
    question rather than guess). See references/item-classification.md for the rules.
    """
    s = {"schedule": 0.0, "task": 0.0, "activity": 0.0}
    signals = []

    has_time = bool(TIME_RE.search(text))
    has_recur = bool(RECUR_RE.search(text))
    has_deadline = bool(DEADLINE_RE.search(text))
    has_duration = bool(DURATION_RE.search(text))
    sched = _hits(text, SCHEDULE_WORDS)
    task = _hits(text, TASK_WORDS)
    act = _hits(text, ACTIVITY_WORDS)

    if has_time and not has_deadline:
        s["schedule"] += 2; signals.append("fixed clock time")
    if sched:
        s["schedule"] += 2; signals.append("event noun: " + ", ".join(sched))
    if WITH_PERSON_RE.search(text):
        s["schedule"] += 1; signals.append("involves another person")
    if has_deadline:
        s["task"] += 2; signals.append("deadline wording")
    if task:
        s["task"] += 2; signals.append("outcome verb: " + ", ".join(task))
    if act:
        s["activity"] += 2; signals.append("ongoing practice: " + ", ".join(act))
    if has_recur:
        s["activity"] += 1.5; s["schedule"] += 0.5; signals.append("recurrence")
    if has_duration and not has_time:
        s["activity"] += 1; signals.append("duration without a clock time")

    ranked = sorted(s.items(), key=lambda kv: kv[1], reverse=True)
    (top, top_score), (_, second) = ranked[0], ranked[1]
    if top_score == 0:
        # Nothing matched: default to task — a task can always be scheduled later,
        # while a wrong calendar event blocks time and may notify people.
        return {"kind": "task", "confidence": 0.3, "signals": ["no signals; default to task"], "ask": False}
    margin = top_score - second
    if margin < 1:
        return {"kind": "ask", "candidates": [ranked[0][0], ranked[1][0]],
                "confidence": 0.4, "signals": signals, "ask": True}
    conf = round(min(0.95, 0.5 + margin / 8), 2)
    return {"kind": top, "confidence": conf, "signals": signals, "ask": False}


# --------------------------------------------------------------------------- status

TODO, DOING, DONE = "To Do", "In Progress", "Completed"

TODO_NAMES = ("to do", "todo", "open", "backlog", "not started", "new", "ready", "planned",
              "queued", "pending", "icebox", "later", "ยังไม่เริ่ม", "รอทำ")
DONE_NAMES = ("complete", "completed", "done", "closed", "finished", "shipped", "released",
              "resolved", "delivered", "archived", "cancelled", "canceled", "won't do", "wont do",
              "เสร็จ", "เสร็จแล้ว", "ปิด")
BLOCKED_NAMES = ("blocked", "on hold", "waiting", "stuck", "paused", "ติด", "รอ")
REVIEW_NAMES = ("review", "qa", "testing", "approval", "verify", "ตรวจ")
CANCEL_NAMES = ("cancelled", "canceled", "won't do", "wont do", "dropped", "duplicate")


def _matches(name, options):
    return any(name == o or o in name for o in options)


def normalize_status(name, status_type=None):
    """Map any ClickUp status to To Do / In Progress / Completed, with flags.

    ClickUp status types are authoritative when known: "open" is the list's first
    status, "done" and "closed" are completion, "custom" is everything between.
    Names decide only when the type is unknown, or to spot a to-do-like custom status.
    """
    n = (name or "").strip().lower()
    t = (status_type or "").strip().lower()
    flags = []
    if _matches(n, BLOCKED_NAMES):
        flags.append("blocked")
    if _matches(n, REVIEW_NAMES):
        flags.append("in_review")
    if _matches(n, CANCEL_NAMES):
        flags.append("cancelled")

    if t in ("done", "closed"):
        cls, basis = DONE, "type:" + t
    elif t == "open":
        cls, basis = TODO, "type:open"
    elif t == "custom":
        cls, basis = (TODO, "type:custom+name") if _matches(n, TODO_NAMES) and "blocked" not in flags \
            else (DOING, "type:custom")
    elif _matches(n, DONE_NAMES):
        cls, basis = DONE, "name"
    elif _matches(n, TODO_NAMES):
        cls, basis = TODO, "name"
    elif n:
        cls, basis = DOING, "name:default-middle"
    else:
        cls, basis = TODO, "empty"
    return {"status": name, "class": cls, "flags": flags, "basis": basis}


def pick_list_status(target_class, list_statuses):
    """Choose the real status name to write, given the list's configured statuses.

    list_statuses: [{"status": "in progress", "type": "custom", "orderindex": 1}, ...]
    Returns the first status (by orderindex) whose class is target_class and that is
    not blocked/review/cancelled — or None, in which case ask the user.
    """
    ordered = sorted(list_statuses, key=lambda s: s.get("orderindex", 0))
    clean = [s for s in ordered
             if normalize_status(s["status"], s.get("type"))["class"] == target_class
             and not normalize_status(s["status"], s.get("type"))["flags"]]
    if target_class == DONE:
        # Prefer "done" over "closed": closed usually hides the task from default views.
        clean.sort(key=lambda s: 0 if s.get("type") == "done" else 1)
    return clean[0]["status"] if clean else None


# --------------------------------------------------------------------------- time

def _dt(v):
    return datetime.fromisoformat(v.replace("Z", "+00:00"))


def _iso(d):
    return d.isoformat(timespec="minutes")


def free_slots(day_start, day_end, busy, min_minutes=25, buffer_minutes=0):
    """Gaps between busy intervals inside [day_start, day_end], each >= min_minutes.

    A buffer is kept after every busy block (travel, context switch). Overlapping
    busy intervals are merged first. All-day events should not be passed as busy.
    """
    start, end = _dt(day_start), _dt(day_end)
    iv = sorted((_dt(b["start"]), _dt(b["end"]) + timedelta(minutes=buffer_minutes)) for b in busy)
    merged = []
    for a, b in iv:
        if merged and a <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], b)
        else:
            merged.append([a, b])
    slots, cur = [], start
    for a, b in merged:
        if a > cur:
            slots.append((cur, min(a, end)))
        cur = max(cur, b)
        if cur >= end:
            break
    if cur < end:
        slots.append((cur, end))
    out = []
    for a, b in slots:
        mins = int((b - a).total_seconds() // 60)
        if mins >= min_minutes:
            out.append({"start": _iso(a), "end": _iso(b), "minutes": mins})
    return out


PRIORITY = {"urgent": 0, "high": 1, "normal": 2, "low": 3, None: 2, "": 2}


def plan(day):
    """Pack open tasks into free slots: overdue/due-first, then priority, then smallest.

    Tasks are split across slots when they do not fit one; the unscheduled remainder
    is reported, never silently dropped. Completed tasks are skipped.
    """
    slots = free_slots(day["day_start"], day["day_end"], day.get("busy", []),
                       day.get("min_block_minutes", 25), day.get("buffer_minutes", 0))
    today = day["day_start"][:10]
    tasks = [t for t in day.get("tasks", [])
             if normalize_status(t.get("status", ""), t.get("status_type"))["class"] != DONE]

    def key(t):
        due = t.get("due") or "9999-12-31"
        return (0 if due[:10] <= today else 1, PRIORITY.get(t.get("priority"), 2),
                due, t.get("estimate_minutes") or 60)

    tasks.sort(key=key)
    free = [[_dt(s["start"]), _dt(s["end"])] for s in slots]
    blocks, unscheduled = [], []
    min_block = day.get("min_block_minutes", 25)
    for t in tasks:
        need = t.get("estimate_minutes") or 60
        for s in free:
            if need <= 0:
                break
            avail = int((s[1] - s[0]).total_seconds() // 60)
            if avail < min(min_block, need):
                continue
            take = min(avail, need)
            blocks.append({"task_id": t.get("id"), "task": t["name"],
                           "start": _iso(s[0]), "end": _iso(s[0] + timedelta(minutes=take)),
                           "minutes": take})
            s[0] += timedelta(minutes=take)
            need -= take
        if need > 0:
            unscheduled.append({"task_id": t.get("id"), "task": t["name"], "minutes_left": need,
                                "due": t.get("due")})
    free_total = sum(s["minutes"] for s in slots)
    demand = sum((t.get("estimate_minutes") or 60) for t in tasks)
    return {"free_minutes": free_total, "demand_minutes": demand,
            "load": round(demand / free_total, 2) if free_total else None,
            "blocks": blocks, "unscheduled": unscheduled}


# --------------------------------------------------------------------------- cli

def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    if cmd == "classify":
        print(json.dumps(classify(" ".join(argv[2:])), ensure_ascii=False, indent=2))
    elif cmd == "status":
        args = argv[2:]
        stype = None
        if "--type" in args:
            i = args.index("--type")
            stype = args[i + 1]
            args = args[:i] + args[i + 2:]
        print(json.dumps(normalize_status(" ".join(args), stype), ensure_ascii=False, indent=2))
    elif cmd in ("slots", "plan"):
        with open(argv[2], encoding="utf-8") as f:
            day = json.load(f)
        if cmd == "slots":
            out = free_slots(day["day_start"], day["day_end"], day.get("busy", []),
                             day.get("min_block_minutes", 25), day.get("buffer_minutes", 0))
        else:
            out = plan(day)
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        print("unknown command: %s" % cmd, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
