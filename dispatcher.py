import logging
from aiogram import Bot, Dispatcher
import config
from filters import IsOwnerFilter, IsAdminFilter, MemberCanRestrictFilter

# Configure logging
logging.basicConfig(level=logging.INFO)

# Check token
if not config.BOT_TOKEN:
    exit("No token provided")

# Bot and Dispatcher
bot = Bot(token=config.BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher()

# Register filters
dp.message.filter(IsOwnerFilter())
dp.message.filter(IsAdminFilter(is_admin=True))
dp.message.filter(MemberCanRestrictFilter(member_can_restrict=True))

import middlewares  # оставим, если у тебя мидлвари инициализируются при импорте
