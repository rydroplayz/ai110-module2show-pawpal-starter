import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from pawpal_system import Owner, Pet, Task, Scheduler


def make_owner():
    owner = Owner(name="Jason", available_minutes_per_day=90)
    dog = Pet(name="Rex", species="Dog")
    cat = Pet(name="Milo", species="Cat")
    owner.add_pet(dog)
    owner.add_pet(cat)
    return owner, dog, cat


def test_task_completion():
    task = Task(description="Feed", time="08:00", date="2026-07-06", duration_minutes=10)
    assert task.completed is False
    task.mark_complete()
    assert task.completed is True


def test_adding_task_increases_pet_task_count():
    dog = Pet(name="Rex", species="Dog")
    assert dog.task_count() == 0
    dog.add_task(Task(description="Walk", time="08:00", date="2026-07-06", duration_minutes=30))
    assert dog.task_count() == 1


def test_sort_by_time_is_chronological():
    owner, dog, cat = make_owner()
    dog.add_task(Task(description="Walk", time="18:00", date="2026-07-06", duration_minutes=30))
    cat.add_task(Task(description="Feed", time="07:00", date="2026-07-06", duration_minutes=10))
    scheduler = Scheduler(owner)
    sorted_tasks = scheduler.sort_by_time()
    times = [t.time for t in sorted_tasks]
    assert times == sorted(times)


def test_conflict_detection_flags_same_time_tasks():
    owner, dog, cat = make_owner()
    dog.add_task(Task(description="Walk", time="08:00", date="2026-07-06", duration_minutes=30))
    cat.add_task(Task(description="Vet", time="08:00", date="2026-07-06", duration_minutes=45))
    scheduler = Scheduler(owner)
    conflicts = scheduler.detect_conflicts()
    assert len(conflicts) == 1


def test_filter_by_pet_and_completion_status():
    owner, dog, cat = make_owner()
    dog.add_task(Task(description="Walk", time="08:00", date="2026-07-06",
                       duration_minutes=30, completed=True))
    dog.add_task(Task(description="Feed", time="09:00", date="2026-07-06",
                       duration_minutes=15, completed=False))
    scheduler = Scheduler(owner)
    pending = scheduler.filter_tasks(pet_name="Rex", completed=False)
    assert len(pending) == 1
    assert pending[0].description == "Feed"


def test_build_daily_plan_respects_time_budget():
    owner, dog, cat = make_owner()
    owner.available_minutes_per_day = 30
    dog.add_task(Task(description="Walk", time="08:00", date="2026-07-06",
                       duration_minutes=30, priority="high"))
    cat.add_task(Task(description="Feed", time="09:00", date="2026-07-06",
                       duration_minutes=15, priority="high"))
    scheduler = Scheduler(owner)
    plan = scheduler.build_daily_plan(date="2026-07-06")
    included = [entry for entry in plan if entry["included"]]
    assert len(included) == 1
    assert included[0]["task"].description == "Walk"