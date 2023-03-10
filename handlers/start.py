import asyncio

from aiogram import types
from sqlalchemy.orm import sessionmaker

from service import pulling_data_for_each_page


async def start(message: types.Message, session_maker: sessionmaker) -> None:
    await message.answer(
        f"Привет, {message.chat.username}.\nЯ бот для фильтрации задач по сайту 'https://codeforces.com/'\n"
        f"Через каждый час я проверяю актуальность задач")

    loop = asyncio.get_running_loop()
    loop.create_task(await pulling_data_for_each_page(session_maker))
    loop.create_task(await message.answer("Задачи в БД обновлены"))
