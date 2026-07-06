from datetime import datetime
from pawpal_system import Owner, Pet, Task, Scheduler

today = datetime.now().strftime("%Y-%m-%d")

owner = Owner(name="Jason", available_minutes_per_day=90)

dog = Pet(name="Rex", species="Dog")
cat = Pet(name="Milo", species="Cat")
owner.add_pet(dog)
owner.add_pet(cat)

dog.add_task(Task(description="Morning walk", time="08:00", date=today,
                   duration_minutes=30, priority="high", frequency="daily"))
dog.add_task(Task(description="Give medication", time="19:00", date=today,
                   duration_minutes=10, priority="high", frequency="daily"))
cat.add_task(Task(description="Feed breakfast", time="07:30", date=today,
                   duration_minutes=15, priority="medium", frequency="daily"))
cat.add_task(Task(description="Vet appointment", time="08:00", date=today,
                   duration_minutes=45, priority="high", frequency="once"))

scheduler = Scheduler(owner)

print("=== Today's Schedule (sorted by time) ===")
for task in scheduler.sort_by_time():
    status = "done" if task.completed else "pending"
    print(f"{task.date} {task.time} | {task.pet_name:6} | {task.description:20} | {status}")

print("\n=== Conflict Check ===")
conflicts = scheduler.detect_conflicts()
if conflicts:
    for task_a, task_b in conflicts:
        print(f"WARNING: '{task_a.description}' ({task_a.pet_name}) and "
              f"'{task_b.description}' ({task_b.pet_name}) both scheduled at {task_a.time} on {task_a.date}")
else:
    print("No conflicts found.")

print(f"\n=== Daily Plan (budget: {owner.available_minutes_per_day} min) ===")
plan = scheduler.build_daily_plan(date=today)
for entry in plan:
    task = entry["task"]
    status = "INCLUDED" if entry["included"] else "SKIPPED "
    print(f"[{status}] {task.time} | {task.pet_name:6} | {task.description:20} | {entry['reason']}")

print("\n=== Completing the dog's morning walk ===")
walk = dog.tasks[0]
walk.mark_complete()
print(f"Marked complete: {walk.description} on {walk.date}")

print("\n=== Filtering: pending tasks for Milo ===")
for task in scheduler.filter_tasks(pet_name="Milo", completed=False):
    print(f"{task.time} | {task.description}")

print(f"\n=== Next available 30-minute slot on {today} ===")
slot = scheduler.next_available_slot(date=today, duration_minutes=30)
print(f"Next open slot: {slot}")

print("\n=== Saving data to data.json ===")
scheduler.save_to_json("data.json")
print("Saved.")