from aiogram import types, utils
from aiogram.dispatcher.handler import ctx_data
from dispatcher import dp
from database.models.user import User
import database.models.lesson as lessonmodel
import database.services.lessons as lessons
import os
from aiogram.types import InputFile
from mongo import botdb
from bson.objectid import ObjectId
import re


@dp.callback_query_handler(lambda callback: callback.data == "callback_lessons")
async def on_tasks_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])

    text = "Выберите категорию:"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    lessonthemes = list(set([element.upper()
                             for element in lessonmodel.lessons_collection.distinct('theme')]))
    lessonthemes.sort()

    for themename in lessonthemes:
        keyboard.add(types.InlineKeyboardButton(
            themename, callback_data="getlessons_" + themename))

    keyboard.add(types.InlineKeyboardButton(
        '⬅️ Назад', callback_data="callback_menu"))

    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.__contains__("getlessons_") and len(lessons.get_lessons_by_theme(callback.data.replace("getlessons_", ''))) > 0)
async def on_lesson_theme_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])
    callback.data = callback.data.replace("getlessons_", '')

    text = utils.markdown.hbold(callback.data) + '\n\n'
    text += "Выберите урок:"

    keyboard = types.InlineKeyboardMarkup(row_width=1)

    lessonlist = lessons.get_lessons({'theme': re.compile(
        '^' + re.escape(str(callback.data)) + '$', re.IGNORECASE)})

    for lesson in lessonlist:

        data = "getlessons_" + str(lesson.id)

        keyboard.add(types.InlineKeyboardButton(
            lesson.name, callback_data=data))

    keyboard.add(types.InlineKeyboardButton(
        '⬅️ Назад', callback_data="callback_lessons"))
    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.__contains__("getlessons_") and str(lessonmodel.lessons_collection.distinct('_id')).__contains__(callback.data.replace("getlessons_", '')))
async def on_lesson_callback(callback: types.CallbackQuery, fromtask: bool = False, returnid: str = ''):
    lesson = lessons.get_lesson(
        ObjectId(callback.data.replace("getlessons_", '')))
    lesson.text = lesson.text.replace("\\n", '\n')

    text = f"{utils.markdown.hbold(lesson.name)}\n"
    text += f"{lesson.text}\n\n"

    keyboard = types.InlineKeyboardMarkup(row_width=1)
    if lesson.link != '':
        keyboard.add(types.InlineKeyboardButton(
            "🔗 Ссылочка", url=lesson.link))
    if fromtask == False:
        keyboard.add(types.InlineKeyboardButton(
            '⬅️ Назад', callback_data="getlessons_" + lesson.theme))
    else:
        keyboard.add(types.InlineKeyboardButton(
            '⬅️ Назад', callback_data="gettask_" + returnid))
    await callback.message.edit_text(text, reply_markup=keyboard)


@dp.callback_query_handler(lambda callback: callback.data.__contains__("getlessons_") and str(lessonmodel.lessons_collection.distinct('_id')).__contains__(callback.data.replace("getlessons_", '').split("__")[0]) and callback.data.__contains__("__"))
async def on_lesson_return_callback(callback: types.CallbackQuery):
    datacallback = callback.data.split("__")
    callback.data = datacallback[0]
    fromtask = True
    returnid = datacallback[1]
    await on_lesson_callback(callback, fromtask, returnid)
