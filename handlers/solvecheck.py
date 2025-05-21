from aiogram import types, utils
from aiogram.dispatcher.handler import ctx_data
from dispatcher import dp
import database.services.users as users
from database.models.user import User
from bson import ObjectId
from mongo import botdb
import config
import random
from . import menu_callbacks

tasks = botdb.tasks


@dp.message_handler(lambda message: message.text in tasks.distinct('flag'))
async def lol(message: types.Message):
    user = User.parse_obj(ctx_data.get()['user'])

    enteredflag = message.text
    task = tasks.find_one({"flag": enteredflag})
    
    if task['_id'] in user.solved:
        if user.solved[task] == True:
            await message.reply("Вы уже решили этот таск")
            return
    
    user.solved.append(task['_id'])
    users.set_solved_user(message.from_user.id, user.solved)
    updated_xp = user.xp + int(task["cost"])
    users.set_xp_user(message.from_user.id, updated_xp)
    
    text = f"✅ Замечательно!\n"
    text += f"Таск {utils.markdown.hbold(task['name'])} решён,\nвам начисленно {utils.markdown.hbold(str(task['cost']))} баллов. 🎆\n"
    text += f"На данный момент у вас {utils.markdown.hbold(str(updated_xp))} баллов!"
    await message.reply(text)
