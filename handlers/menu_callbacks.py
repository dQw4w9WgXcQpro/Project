from aiogram import types, utils
from aiogram.dispatcher.handler import ctx_data
from dispatcher import dp
from database.models.user import User
from database.models.task import Task
import database.services.tasks as tasks
import database.services.lessons as lessons
import os
from aiogram.types import InputFile
from mongo import botdb
from bson.objectid import ObjectId
import re


async def print_menu(message: types.Message, user: User, from_callback: bool = False):
    bot = dp.bot

    text = "👤" + utils.markdown.hbold(user.name)
    text += '\n'
    text += '\n'
    text += f'{utils.markdown.hbold("Твой XP:")} {str(user.xp)}'

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    keyboard.add(types.InlineKeyboardButton(
        "📚 К таскам", callback_data="callback_tasks"))
    keyboard.add(types.InlineKeyboardButton(
        "🏫 К урокам", callback_data="callback_lessons"))
    keyboard.add(types.InlineKeyboardButton(
        "📊 Таблица лидеров", callback_data="callback_sb"))

    if (from_callback):
        await message.edit_text(text, reply_markup=keyboard)
    else:
        await message.answer(text=text, reply_markup=keyboard)
    pass


@dp.message_handler(commands='menu')
async def on_menu_command(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])
    if not user.isInit:
        return

    await print_menu(message, user)


@dp.callback_query_handler(lambda callback: callback.data == "callback_menu")
async def on_menu_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])
    if not user.isInit:
        return

    await print_menu(callback.message, user, True)


@dp.callback_query_handler(lambda callback: callback.data == "callback_tasks")
async def on_tasks_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])

    text = "Выберите категорию:"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    taskthemes = list(set([element.lower()
                      for element in tasks.tasks_collection.distinct('theme')]))
    taskthemes.sort()

    for theme in taskthemes:
        tasks_by_theme = tasks.get_tasks(
            {
                'theme': {
                    '$regex': re.compile(r"^" + theme + "(?i)")
                }
            }
        )
        themecnt = len(tasks_by_theme)
        solvedcnt = 0
        for theme_task in tasks_by_theme:
            if theme_task.id in user.solved:
                solvedcnt += 1

        button_text = theme + f" ({solvedcnt}/{themecnt})"

        if solvedcnt == themecnt:
            button_text = "✅ " + button_text

        keyboard.add(types.InlineKeyboardButton(
            button_text.upper(), callback_data="gettasks_" + theme))

    keyboard.add(types.InlineKeyboardButton(
        '⬅️ Назад', callback_data="callback_menu"))

    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.__contains__("gettasks_") and list(set([element.lower() for element in tasks.tasks_collection.distinct('theme')])).__contains__(callback.data.replace("gettasks_", '').lower()))
async def on_theme_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])
    callback.data = callback.data.replace("gettasks_", '')

    text = utils.markdown.hbold(callback.data) + '\n\n'
    text += "Выберите таск:"

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    tasklist = tasks.get_tasks({'theme': re.compile(
        '^' + re.escape(str(callback.data)) + '$', re.IGNORECASE)})

    for task in tasklist:
        taskname = task.name

        if user.solved.__contains__(task.id):
            taskname = "✅ " + taskname

        data = "gettask_" + str(task.id)

        keyboard.add(types.InlineKeyboardButton(
            taskname, callback_data=data))
    keyboard.add(types.InlineKeyboardButton(
        '⬅️ Назад', callback_data="callback_tasks"))
    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.__contains__("gettask_") and str(tasks.tasks_collection.distinct('_id')).__contains__(callback.data.replace("gettask_", '')))
async def on_task_callback(callback: types.CallbackQuery):
    task = tasks.get_task(ObjectId(callback.data.replace("gettask_", '')))
    task.text = task.text.replace("\\n", '\n')

    text = f"{utils.markdown.bold(task.name)}\n"
    text += f"{task.text}\n\n"
    text += utils.markdown.italic(f"Цена: {task.cost}")

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if task.url != '':
        keyboard.add(types.InlineKeyboardButton(
            "🔗 Ссылочка", url=task.url))

    # add lesson button
    if task.lesson != '':
        data = f"getlessons_{str(task.lesson)}__{str(callback.data.replace('gettask_', ''))}"
        keyboard.add(types.InlineKeyboardButton(
            "🏫 Урок", callback_data=data))

    elif len(lessons.get_lessons_by_theme(task.theme)) > 0:
        data = f"getlessons_{task.theme}"
        keyboard.add(types.InlineKeyboardButton(
            "🏫 Уроки по теме", callback_data=data))

    keyboard.add(types.InlineKeyboardButton(
        '⬅️ Назад', callback_data="gettasks_" + task.theme))

    #
    await callback.message.edit_text(text, reply_markup=keyboard, parse_mode='Markdown')

    # send files
    if len(task.file) > 0:
        for file in task.file:
            iofile = InputFile(os.path.join('.',
                                            "files", str(task.id), file), file)
            keyboard = types.InlineKeyboardMarkup(row_width=1)
            keyboard.add(types.InlineKeyboardButton(
                "❌ закрыть", callback_data="file_close"))
            await callback.message.answer_document(iofile, caption=f"Файл к таску {task.name}", reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data == "file_close")
async def on_file_close_callback(callback: types.CallbackQuery):
    await callback.message.delete()
    await callback.answer("Ок")
