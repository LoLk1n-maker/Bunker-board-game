from aiogram import Bot, Dispatcher, executor
from config import token
from messege_handlers import register_handlers

bot = Bot(token)
dp = Dispatcher(bot)

async def on_startup(dp):
    await register_handlers(dp, bot)


if __name__ == "__main__":
    # Запускаем обработчики и начинаем опрос
    executor.start_polling(dp, on_startup=on_startup)
