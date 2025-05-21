import asyncio
from dispatcher import dp, bot
import handlers
import middlewares

async def main():
    await dp.start_polling(bot, skip_updates=True)

if __name__ == "__main__":
    asyncio.run(main())
 