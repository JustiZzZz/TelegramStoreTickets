import asyncio
from aiogram import Bot, Dispatcher
from files.config import TOKEN
from handlers import router

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(router)

async def main():
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())