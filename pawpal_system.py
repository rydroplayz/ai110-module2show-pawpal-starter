from dataclasses import dataclass, field
from typing import List, Optional


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
        pass


@dataclass
class Pet:
    name: str
    species: str
    tasks: List[Task] = field(default_factory=list)

    def add_task(self, task: Task):
        pass

    def list_tasks(self):
        pass

    def task_count(self):
        pass


@dataclass
class Owner:
    name: str
    available_minutes_per_day: int = 120
    pets: List[Pet] = field(default_factory=list)

    def add_pet(self, pet: Pet):
        pass

    def get_pet(self, name: str):
        pass

    def all_tasks(self):
        pass


class Scheduler:
    def __init__(self, owner: Owner):
        self.owner = owner

    def sort_by_time(self, tasks=None):
        pass

    def sort_by_priority(self, tasks=None):
        pass

    def filter_tasks(self, pet_name=None, completed=None):
        pass

    def detect_conflicts(self):
        pass

    def build_daily_plan(self):
        pass

    def next_available_slot(self, date, duration_minutes=30):
        pass

    def save_to_json(self, filepath):
        pass

    def load_from_json(self, filepath):
        pass