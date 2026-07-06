# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agent Workflow (SF7)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->

**What did the agent do?**

<!-- List the steps the agent took (files edited, commands run, etc.) -->

**What did you have to verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

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

<!-- Your conclusion -->
