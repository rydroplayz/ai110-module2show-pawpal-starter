# PawPal+ Project Reflection

## 1. System Design

**a. Initial design**

I designed four classes: Task, Pet, Owner, and Scheduler. Task holds the data for a single care activity (time, date, duration, priority, frequency, completion status). Pet owns a list of Tasks and can add/list/count them. Owner owns a list of Pets and also holds available_minutes_per_day, which represents the time constraint the scenario asks the scheduler to respect. Scheduler doesn't hold any task data itself, it reads from Owner and produces sorted, filtered, or conflict-checked views across all of the owner's pets, and builds a daily plan that fits within the owner's available time.

**b. Design changes**

My design changed once, before I finalized the implementation: I originally planned Scheduler to just support basic sorting and filtering, but going through the rubric against my draft class list showed I was leaving stretch-credit features unclaimed. I added next_available_slot(), save_to_json(), and load_from_json() to Scheduler, and available_minutes_per_day to Owner, before writing the UML so the diagram would still match the final code.

---

## 2. Scheduling Logic and Tradeoffs

**a. Constraints and priorities**

The scheduler considers two constraints: task priority (high/medium/low) and the owner's available time budget for the day. Time budget mattered most to me because it's what makes build_daily_plan() actually have to make tradeoffs, without a limited budget, every task would just get included and there'd be no real "reasoning" happening, which is specifically what the project scenario asked for.

**b. Tradeoffs**

My build_daily_plan() explains its include/skip decisions with a simple text reason (priority level and minutes remaining), not a deeper analysis of tradeoffs between tasks. This keeps the logic easy to follow, but it means the "explanation" is fairly shallow, it doesn't account for things like how urgent a skipped task is or whether skipping it has consequences for the pet's routine.

---

## 3. AI Collaboration

**a. How you used AI**

I used AI in the project as a step-by-step build partner rather than a one-shot code generator. I had it walk me through each phase in order: UML design, class stubs, then filling in the Scheduler methods one at a time, then the demo script, then tests.

**b. Judgment and verification**

While building main.py, I was given a draft that referenced scheduler.mark_task_complete(), but that method was never actually part of my Scheduler class design or UML. I caught the mismatch before running it and had it corrected to just call task.mark_complete() directly, which is what my actual class supports.

---

## 4. Testing and Verification

**a. What you tested**

I  tested: whether marking a task complete actually flips its status, whether adding a task increases a pet's task count, whether sorting by time returns tasks in chronological order, whether the conflict detector correctly flags two tasks scheduled at the same time across different pets, whether filtering by pet and completion status returns the right subset, and whether the daily plan correctly excludes a task once the time budget runs out. These matter because they're the exact behaviors the rubric and scenario call out, if any of these broke, the "smart" part of the scheduler wouldn't actually be smart.

**b. Confidence**

I'm confident in the scheduler's correctness, all 6 tests pass and they cover the core behaviors (completion, counting, sorting, conflicts, filtering, budget-based planning). If I had more time, I'd want to test edge cases like a pet with zero tasks, two tasks with identical priority and time, and a task whose duration is larger than the entire daily budget.

---

## 5. Reflection

**a. What went well**

I'm most satisfied with the daily plan reasoning logic (build_daily_plan()). It's the piece that actually fulfills the scenario's request to not just generate a schedule but explain why each task was included or skipped, and seeing it correctly skip a task once the time budget ran out in the demo output felt like the system was doing something genuinely useful, not just sorting a list.

**b. What you would improve**

Recurring tasks currently always schedule their next occurrence exactly 7 days (or 1 day for daily tasks) after the original due date, even if the task was actually completed late. If I had another iteration, I'd change this so a weekly task completed several days late doesn't quietly drift away from its usual day-of-week over time, for example, basing the next date on the completion date when it's late, rather than always adding a fixed interval to the original date.
**c. Key takeaway**

The biggest thing I learned was to double-check AI output against my own requirements instead of just trusting it, I caught a rubric mismatch before finalizing my UML, and a real bug (a method that didn't exist in my classes) before it caused an error. AI moved fast, but correctness was still my job.
