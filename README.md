# PawPal+ (Module 2 Project)

You are building **PawPal+**, a Streamlit app that helps a pet owner plan care tasks for their pet.

## Scenario

A busy pet owner needs help staying consistent with pet care. They want an assistant that can:

- Track pet care tasks (walks, feeding, meds, enrichment, grooming, etc.)
- Consider constraints (time available, priority, owner preferences)
- Produce a daily plan and explain why it chose that plan

Your job is to design the system first (UML), then implement the logic in Python, then connect it to the Streamlit UI.

## What you will build

Your final app should:

- Let a user enter basic owner + pet info
- Let a user add/edit tasks (duration + priority at minimum)
- Generate a daily schedule/plan based on constraints and priorities
- Display the plan clearly (and ideally explain the reasoning)
- Include tests for the most important scheduling behaviors

## Getting started

### Setup

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Suggested workflow

1. Read the scenario carefully and identify requirements and edge cases.
2. Draft a UML diagram (classes, attributes, methods, relationships).
3. Convert UML into Python class stubs (no logic yet).
4. Implement scheduling logic in small increments.
5. Add tests to verify key behaviors.
6. Connect your logic to the Streamlit UI in `app.py`.
7. Refine UML so it matches what you actually built.

## 🖥️ Sample Output

```
$ python main.py
=== Today's Schedule (sorted by time) ===
2026-07-06 07:30 | Milo   | Feed breakfast       | pending
2026-07-06 08:00 | Rex    | Morning walk         | pending
2026-07-06 08:00 | Milo   | Vet appointment      | pending
2026-07-06 19:00 | Rex    | Give medication      | pending

=== Conflict Check ===
WARNING: 'Morning walk' (Rex) and 'Vet appointment' (Milo) both scheduled at 08:00 on 2026-07-06

=== Daily Plan (budget: 90 min) ===
[INCLUDED] 08:00 | Rex    | Morning walk         | included: high priority, fit within 90 min remaining
[INCLUDED] 08:00 | Milo   | Vet appointment      | included: high priority, fit within 60 min remaining
[INCLUDED] 19:00 | Rex    | Give medication      | included: high priority, fit within 15 min remaining
[SKIPPED ] 07:30 | Milo   | Feed breakfast       | skipped: only 5 min left, task needs 15 min

=== Completing the dog's morning walk ===
Marked complete: Morning walk on 2026-07-06

=== Filtering: pending tasks for Milo ===
07:30 | Feed breakfast
08:00 | Vet appointment

=== Next available 30-minute slot on 2026-07-06 ===
Next open slot: 07:00

=== Saving data to data.json ===
Saved.
```

## 🧪 Testing PawPal+

```bash
# Run the full test suite:
pytest

# Run with coverage:
pytest --cov
```

These tests cover: task completion, pet task counting, chronological sorting, conflict detection across pets, filtering by pet and status, and whether the daily plan correctly respects the owner's time budget.

Sample test output:

```
$ python -m pytest -v
=================== test session starts ====================
platform win32 -- Python 3.14.5, pytest-9.1.1, pluggy-1.6.0
rootdir: C:\Users\Windows\ai110-module2show-pawpal-starter
plugins: anyio-4.14.0
collected 6 items
tests/test_pawpal.py::test_task_completion PASSED     [ 16%]
tests/test_pawpal.py::test_adding_task_increases_pet_task_count PASSED [ 33%]
tests/test_pawpal.py::test_sort_by_time_is_chronological PASSED [ 50%]
tests/test_pawpal.py::test_conflict_detection_flags_same_time_tasks PASSED [ 66%]
tests/test_pawpal.py::test_filter_by_pet_and_completion_status PASSED [ 83%]
tests/test_pawpal.py::test_build_daily_plan_respects_time_budget PASSED [100%]
==================== 6 passed in 0.12s =====================
```

## 📐 Smarter Scheduling

| Feature | Method(s) | Notes |
|---------|-----------|-------|
| Task sorting | `Scheduler.sort_by_time()`, `Scheduler.sort_by_priority()` | Sort chronologically or by priority level |
| Filtering | `Scheduler.filter_tasks()` | Filter by pet name and/or completion status |
| Conflict handling | `Scheduler.detect_conflicts()` | Flags tasks scheduled at the same date/time |
| Daily plan with reasoning | `Scheduler.build_daily_plan()` | Orders tasks by priority, fits them to the owner's time budget, explains each include/skip decision |
| Next available slot | `Scheduler.next_available_slot()` | Finds the next open time gap long enough for a new task |

## 📸 Demo Walkthrough

1. <!-- Describe this step -->
2. <!-- Describe this step -->
3. <!-- Describe this step -->
4. <!-- Describe this step -->
5. <!-- Add more steps as needed -->

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or link to a demo video here -->