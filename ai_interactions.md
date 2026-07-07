# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

After adding recurring-task support to the Scheduler, I asked the agent to audit my entire repo against the grading rubric and fix any resulting inconsistencies across multiple files at once, rather than one file at a time.

**What did the agent do?**

It reviewed `pawpal_system.py`, `diagrams/uml.mmd`, `reflection.md`, `README.md`, and `tests/test_pawpal.py` together, and found that: the UML diagram was missing the new `complete_task()` method, my reflection still said I "would add" recurring tasks even though I'd already built it, the README's feature table and test-coverage summary didn't mention recurring tasks, and there were no tests covering the new feature at all. It then edited all four non-code files in one coordinated pass and wrote two new pytest tests for the recurring-task behavior.

**What did you have to verify or fix manually?**

I ran the full test suite myself afterward to confirm all 8 tests actually passed, rather than trusting that they would. I also personally reworded the reflection text the agent drafted, since it initially described my past design decisions in a way I didn't think sounded like me, and I asked for it to focus only on the concrete "late completion" limitation instead.

---

## Prompt Comparison (SF11)

> Compare two different prompts (or two different models) on the same task.

| | Option A | Option B |
|-|----------|----------|
| **Model / tool used** | ChatGPT | Claude |
| **Prompt** | "How should recurring weekly tasks reschedule themselves?" (with class context) | Same prompt, same context |
| **Response summary** | Recommended creating a new Task via `next_occurrence()`, called separately from a `complete_task()` method | Recommended the same core idea, but folded next-occurrence logic directly into `mark_complete()`, returning the new task |
| **What was useful** | Clear explanation of Option 1 vs Option 2 tradeoffs (new task vs. mutating date), good SRP reasoning | Reused my existing `mark_complete()` name instead of introducing a new one; flagged a real edge case (day-of-week drift on late completions) I hadn't considered |
| **Problems noticed** | Introduced a new method name (`next_occurrence`) that didn't match anything already in my code | Needed adapting to use `datetime.strptime` instead of `date.fromisoformat` to match my existing imports |
| **Decision** | — | Used Claude's approach, since it fit my existing method names and codebase with less restructuring |

**Which approach did you use in your final implementation and why?**

I used Claude's version because it extended my existing `mark_complete()` method instead of requiring a new method name, so it needed fewer changes to `main.py` and `app.py`. Both tools agreed on the core design (create a new task rather than mutate the old one, to preserve history), which gave me confidence the approach was sound.
