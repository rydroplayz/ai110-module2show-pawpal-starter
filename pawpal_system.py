from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional
import json


@dataclass
class Task:
    description: str
    time: str
    date: str
    duration_minutes: int
    priority: str = "medium"
    frequency: str = "once"
    completed: bool = False
    pet_name: str = ""

    def mark_complete(self):
        self.completed = True
        if self.frequency == "once":
            return None
        current_date = datetime.strptime(self.date, "%Y-%m-%d")
        if self.frequency == "daily":
            next_date = current_date + timedelta(days=1)
        elif self.frequency == "weekly":
            next_date = current_date + timedelta(weeks=1)
        else:
            return None
        return Task(
            description=self.description,
            time=self.time,
            date=next_date.strftime("%Y-%m-%d"),
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            frequency=self.frequency,
            pet_name=self.pet_name,
        )


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        task.pet_name = self.name
        self.tasks.append(task)

    def list_tasks(self):
        return self.tasks

    def task_count(self):
        return len(self.tasks)


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 120
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        self.pets.append(pet)

    def get_pet(self, name: str):
        for pet in self.pets:
            if pet.name == name:
                return pet
        return None

    def all_tasks(self):
        tasks = []
        for pet in self.pets:
            tasks.extend(pet.tasks)
        return tasks


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks=None):
        if tasks is None:
            tasks = self.owner.all_tasks()
        return sorted(tasks, key=lambda t: (t.date, t.time))

    def sort_by_priority(self, tasks=None):
        priority_rank = {"high": 0, "medium": 1, "low": 2}
        if tasks is None:
            tasks = self.owner.all_tasks()
        return sorted(tasks, key=lambda t: (priority_rank.get(t.priority, 1), t.date, t.time))

    def filter_tasks(self, pet_name=None, completed=None):
        tasks = self.owner.all_tasks()
        if pet_name is not None:
            tasks = [t for t in tasks if t.pet_name == pet_name]
        if completed is not None:
            tasks = [t for t in tasks if t.completed == completed]
        return tasks

    def detect_conflicts(self):
        tasks = self.owner.all_tasks()
        conflicts = []
        seen = {}
        for task in tasks:
            key = (task.date, task.time)
            if key in seen:
                conflicts.append((seen[key], task))
            else:
                seen[key] = task
        return conflicts
    
    def complete_task(self, task):
        next_task = task.mark_complete()
        if next_task is not None:
            pet = self.owner.get_pet(task.pet_name)
            if pet is not None:
                pet.add_task(next_task)
        return next_task

    def build_daily_plan(self, date=None):
        if date is None:
            date = datetime.now().strftime("%Y-%m-%d")

        candidates = [t for t in self.owner.all_tasks() if t.date == date and not t.completed]
        ordered = self.sort_by_priority(candidates)

        budget = self.owner.available_minutes_per_day
        minutes_used = 0
        plan = []

        for task in ordered:
            minutes_left = budget - minutes_used
            if task.duration_minutes <= minutes_left:
                minutes_used += task.duration_minutes
                reason = f"included: {task.priority} priority, fit within {minutes_left} min remaining"
                plan.append({"task": task, "included": True, "reason": reason})
            else:
                reason = f"skipped: only {minutes_left} min left, task needs {task.duration_minutes} min"
                plan.append({"task": task, "included": False, "reason": reason})

        return plan

    def next_available_slot(self, date, duration_minutes=30, day_start="07:00", day_end="21:00"):
        fmt = "%H:%M"
        start = datetime.strptime(day_start, fmt)
        end = datetime.strptime(day_end, fmt)
        duration = timedelta(minutes=duration_minutes)

        busy_times = sorted(t.time for t in self.owner.all_tasks() if t.date == date)
        busy = [datetime.strptime(t, fmt) for t in busy_times]

        cursor = start
        for busy_time in busy:
            if busy_time - cursor >= duration:
                return cursor.strftime(fmt)
            if busy_time + duration > cursor:
                cursor = busy_time + duration

        if end - cursor >= duration:
            return cursor.strftime(fmt)
        return None

    def save_to_json(self, filepath):
        data = {
            "name": self.owner.name,
            "available_minutes_per_day": self.owner.available_minutes_per_day,
            "pets": [
                {
                    "name": pet.name,
                    "species": pet.species,
                    "tasks": [
                        {
                            "description": t.description,
                            "time": t.time,
                            "date": t.date,
                            "duration_minutes": t.duration_minutes,
                            "priority": t.priority,
                            "frequency": t.frequency,
                            "completed": t.completed,
                            "pet_name": t.pet_name,
                        }
                        for t in pet.tasks
                    ],
                }
                for pet in self.owner.pets
            ],
        }
        with open(filepath, "w") as f:
            json.dump(data, f, indent=2)

    def load_from_json(self, filepath):
        with open(filepath, "r") as f:
            data = json.load(f)

        owner = Owner(name=data["name"], available_minutes_per_day=data["available_minutes_per_day"])
        for pet_data in data["pets"]:
            pet = Pet(name=pet_data["name"], species=pet_data["species"])
            for task_data in pet_data["tasks"]:
                pet.tasks.append(Task(**task_data))
            owner.add_pet(pet)

        self.owner = owner
        return owner