from ..models import Task, tasks_collection
from bson import ObjectId

def get_tasks(filter) -> list[Task]:
    tasks = tasks_collection.find(filter)
    return [Task(**u) for u in tasks]


def get_task(id: ObjectId) -> Task:
    task = tasks_collection.find_one({'_id': id})
    return Task(**task) if task else None

def get_task(filter) -> Task:
    task = tasks_collection.find_one(filter)
    return Task(**task) if task else None
