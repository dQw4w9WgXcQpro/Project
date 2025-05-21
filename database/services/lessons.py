from ..models import Lesson, lessons_collection
from bson import ObjectId
import re


def get_lessons(filter) -> list[Lesson]:
    lesson = lessons_collection.find(filter)
    return [Lesson(**u) for u in lesson]


def get_lesson(id: ObjectId) -> Lesson:
    lesson = lessons_collection.find_one({'_id': id})
    return Lesson(**lesson) if lesson else None


def get_lesson(filter) -> Lesson:
    lesson = lessons_collection.find_one(filter)
    return Lesson(**lesson) if lesson else None


def get_lesson_by_theme(name: str) -> Lesson | None:
    lesson = lessons_collection.find_one(
        {
            "theme": re.compile(
                '^' + re.escape(name) + '$', re.IGNORECASE)
        })
    return Lesson(**lesson) if lesson else None


def get_lessons_by_theme(theme: str) -> list[Lesson]:
    lessons = lessons_collection.find({
        "theme": re.compile(
            '^' + re.escape(str(theme)) + '$', re.IGNORECASE)
    })
    return [Lesson(**u) for u in lessons]
