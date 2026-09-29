"""Tests for chronos.py. Run: python -m unittest test_chronos (from this folder)."""
import os
import sys
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from chronos import (DONE, DOING, TODO, classify, free_slots, normalize_status,  # noqa: E402
                     pick_list_status, plan)


class Classify(unittest.TestCase):
    def kind(self, text):
        return classify(text)["kind"]

    def test_schedule(self):
        self.assertEqual(self.kind("Standup with design team at 10:00"), "schedule")
        self.assertEqual(self.kind("Dentist appointment Thursday 3pm"), "schedule")
        self.assertEqual(self.kind("ประชุมกับลูกค้า 14:00"), "schedule")

    def test_task(self):
        self.assertEqual(self.kind("Submit the tax form by Friday"), "task")
        self.assertEqual(self.kind("Fix the login redirect bug"), "task")
        self.assertEqual(self.kind("ส่งรายงานภายในวันศุกร์"), "task")

    def test_activity(self):
        self.assertEqual(self.kind("Gym 3x a week"), "activity")
        self.assertEqual(self.kind("Read for 30 minutes every night"), "activity")
        self.assertEqual(self.kind("อ่านหนังสือทุกวัน"), "activity")

    def test_deadline_time_is_not_a_schedule(self):
        self.assertEqual(self.kind("Send the invoice before 5pm"), "task")

    def test_empty_defaults_to_task(self):
        r = classify("the thing")
        self.assertEqual(r["kind"], "task")
        self.assertLess(r["confidence"], 0.5)

    def test_conflict_asks(self):
        r = classify("Review with Anna at 2pm")
        self.assertIn(r["kind"], ("ask", "schedule"))


class Status(unittest.TestCase):
    def cls(self, name, t=None):
        return normalize_status(name, t)["class"]

    def test_types_are_authoritative(self):
        self.assertEqual(self.cls("anything", "open"), TODO)
        self.assertEqual(self.cls("shipped", "done"), DONE)
        self.assertEqual(self.cls("archived", "closed"), DONE)
        self.assertEqual(self.cls("in progress", "custom"), DOING)

    def test_todo_like_custom(self):
        self.assertEqual(self.cls("backlog", "custom"), TODO)
        self.assertEqual(self.cls("ready", "custom"), TODO)

    def test_names_without_type(self):
        self.assertEqual(self.cls("to do"), TODO)
        self.assertEqual(self.cls("Complete"), DONE)
        self.assertEqual(self.cls("in review"), DOING)
        self.assertEqual(self.cls("เสร็จแล้ว"), DONE)

    def test_flags(self):
        self.assertIn("blocked", normalize_status("blocked", "custom")["flags"])
        self.assertEqual(self.cls("blocked", "custom"), DOING)
        self.assertIn("in_review", normalize_status("in review")["flags"])
        self.assertIn("cancelled", normalize_status("cancelled", "closed")["flags"])

    def test_pick_list_status(self):
        statuses = [
            {"status": "backlog", "type": "open", "orderindex": 0},
            {"status": "in progress", "type": "custom", "orderindex": 1},
            {"status": "in review", "type": "custom", "orderindex": 2},
            {"status": "closed", "type": "closed", "orderindex": 4},
            {"status": "done", "type": "done", "orderindex": 3},
        ]
        self.assertEqual(pick_list_status(TODO, statuses), "backlog")
        self.assertEqual(pick_list_status(DOING, statuses), "in progress")
        self.assertEqual(pick_list_status(DONE, statuses), "done")
        self.assertIsNone(pick_list_status(DOING, statuses[:1]))


DAY = {
    "day_start": "2026-09-29T09:00:00+07:00",
    "day_end": "2026-09-29T17:00:00+07:00",
    "busy": [
        {"start": "2026-09-29T10:00:00+07:00", "end": "2026-09-29T10:30:00+07:00"},
        {"start": "2026-09-29T10:15:00+07:00", "end": "2026-09-29T11:00:00+07:00"},
        {"start": "2026-09-29T12:00:00+07:00", "end": "2026-09-29T13:00:00+07:00"},
        {"start": "2026-09-29T16:50:00+07:00", "end": "2026-09-29T18:00:00+07:00"},
    ],
}


class Time(unittest.TestCase):
    def test_free_slots_merges_and_filters(self):
        s = free_slots(DAY["day_start"], DAY["day_end"], DAY["busy"], min_minutes=25)
        self.assertEqual([x["minutes"] for x in s], [60, 60, 230])

    def test_buffer(self):
        s = free_slots(DAY["day_start"], DAY["day_end"], DAY["busy"], min_minutes=25, buffer_minutes=10)
        self.assertEqual(s[1]["start"], "2026-09-29T11:10+07:00")

    def test_plan_orders_and_reports_overflow(self):
        day = dict(DAY, tasks=[
            {"id": "a", "name": "low later", "estimate_minutes": 60, "priority": "low", "due": "2026-10-05"},
            {"id": "b", "name": "due today", "estimate_minutes": 90, "priority": "normal", "due": "2026-09-29"},
            {"id": "c", "name": "done one", "estimate_minutes": 60, "status": "complete"},
            {"id": "d", "name": "huge", "estimate_minutes": 400, "priority": "high"},
        ])
        out = plan(day)
        self.assertEqual(out["blocks"][0]["task_id"], "b")
        self.assertNotIn("c", [b["task_id"] for b in out["blocks"]])
        self.assertTrue(out["unscheduled"])
        self.assertGreater(out["load"], 1)


if __name__ == "__main__":
    unittest.main()
