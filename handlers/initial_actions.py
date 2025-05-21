from aiogram import types, utils
from aiogram.dispatcher.handler import ctx_data
from dispatcher import dp
import database.services.users as users
from database.models.user import User
from mongo import botdb
import asyncio
import config
import random
from . import menu_callbacks


@dp.message_handler(lambda message: message.text == "Да")
async def start_go(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])
    if (user.isInit):
        return

    users.set_init_user(message.from_user.id, True)
    await message.reply("Замечательно! Тогда начнём.", reply_markup=types.reply_keyboard.ReplyKeyboardRemove())
    await dp.bot.set_my_commands([types.BotCommand("/menu", "Вызвать меню"),
                                  types.BotCommand("/sb", "Таблица лидеров")], types.BotCommandScopeChat(message.chat.id))
    await menu_callbacks.print_menu(message, user)


@dp.message_handler(lambda message: message.text == "Не, спасибо")
async def start_no(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])
    if (user.isInit):
        return

    users.set_init_user(message.from_user.id, False)

    await message.reply("Ну и пошел нахуй тогда")
    await asyncio.sleep(1)
    await message.reply("Не пиши мне больше!")


@dp.message_handler(commands="start")
async def cmd_start(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])

    if (user.isInit):
        return

    text = utils.markdown.hbold(f"Привет, {message.from_user.first_name}!\n\n")

    text += "Я <b>Олег</b>, твой бот для обучения и практике в CTF\n"

    text += "Готов учиться?"

    keyboard = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    keyboard.add(types.KeyboardButton("Да"))
    keyboard.add(types.KeyboardButton("Не, спасибо"))

    await message.reply(text, reply_markup=keyboard)
