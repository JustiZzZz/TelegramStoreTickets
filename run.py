import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties

from files.config import TOKEN
from handlers import router

async def main():
    # Update this line
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage=MemoryStorage())

    dp.include_router(router)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())