from aiogram import types, utils
from aiogram.utils.emoji import emojize
from aiogram.dispatcher.handler import ctx_data
from dispatcher import dp
from database.models.user import User
from os import path
import config
import database.services.users as users
from mongo import botdb
from bson.objectid import ObjectId
import re
usersdb = botdb.users
sbtext = ''


def get_scoreboard(userdat: User):
    usersbpers = ""
    sbtext = utils.markdown.bold("Таблица лидеров:") + '\n'
    
    sbdata = users.get_users()
    sbdata.sort(key=lambda user: user.xp, reverse=True)

    for i, user in enumerate(sbdata, 1):
        itext = '🥇🥈🥉'[i - 1] if i < 4 else utils.markdown.bold(str(i)) + "."

        if user.id == userdat.id:
            if i <= 10:
                sbtext += f"{itext} {utils.markdown.bold(user.name)} - {str(user.xp)} баллов.\n"
            else:
                usersbpers += f"\n{utils.markdown.bold(user.name)} вы на {str(i)} месте, у вас {str(user.xp)} баллов!"
        else:
            if i <= 10:
                sbtext += f"{itext} {user.name} - {str(user.xp)} баллов.\n"

    # sbdata = usersdb.find({}).sort("xp", -1).limit(10)
    # for i, user in enumerate(sbdata, 1):
    #     if 'xp' not in user:
    #         users.set_xp_user(user['_id'], 0)
    #     else:
    #         if str(user['_id']) == userid:
    #             sbtext += f"{utils.markdown.bold(str(i))}. {utils.markdown.bold(user['name'])} - {str(user['xp'])} баллов.\n"
    #         else:
    #             sbtext += f"{utils.markdown.bold(str(i))}. {user['name']} - {str(user['xp'])} баллов.\n"

    sbtext += usersbpers
    return sbtext


async def print_scoreboard(message: types.Message, user: User, from_callback: bool = False):
    keyboard = types.InlineKeyboardMarkup(row_width=2)
    keyboard.row(
        types.InlineKeyboardButton(
            "⬅️", callback_data="callback_menu"),
        types.InlineKeyboardButton(
            "🔄", callback_data="callback_sb")
    )
    if (from_callback):
        await message.edit_text(get_scoreboard(user), parse_mode="Markdown", reply_markup=keyboard)
    else:
        await message.answer(get_scoreboard(user), parse_mode="Markdown", reply_markup=keyboard)
        pass


@dp.message_handler(commands='sb')
async def on_sb_command(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])
    if not user.isInit:
        return

    await print_scoreboard(message, user)


@dp.callback_query_handler(lambda callback: callback.data == "callback_sb")
async def on_menu_callback(callback: types.CallbackQuery):
    user = User.parse_obj(ctx_data.get()['user'])
    if not user.isInit:
        return
    try:
        await print_scoreboard(callback.message, user, True)
    except utils.exceptions.MessageNotModified:
        await callback.answer("Нечего обновлять", cache_time=2)
