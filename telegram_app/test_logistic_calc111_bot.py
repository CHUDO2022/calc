import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.fsm.storage.memory import MemoryStorage

API_TOKEN = '7545272422:AAEKcO-OdL9HlSJV6KlST7lLsE5lDcVoD6I'

bot = Bot(token=API_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)  # Создаем диспетчер


@dp.message(Command("start"))
async def start(message: types.Message):
    telegram_id = message.from_user.id  # ID пользователя
    username = message.from_user.username or "не указан"  # Никнейм
    first_name = message.from_user.first_name or "не указано"  # Имя
    last_name = message.from_user.last_name or "не указано"  # Фамилия
    language_code = message.from_user.language_code  # Язык интерфейса Telegram

    # Кодируем данные для передачи в URL
    web_app_url = (
        f"https://7553-94-159-108-159.ngrok-free.app?"
        f"tg_id={telegram_id}&"
        f"username={username}&"
        f"first_name={first_name}&"
        f"last_name={last_name}&"
        f"lang={language_code}"
    )

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(
            text="Открыть форму",
            web_app=types.WebAppInfo(url=web_app_url)
        )]
    ])
    await message.reply("Нажмите кнопку, чтобы открыть форму:", reply_markup=keyboard)


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
