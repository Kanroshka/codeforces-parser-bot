import asyncio
from aiogram import Router
from aiogram import Bot, Dispatcher
from sqlalchemy import URL

from config import Config
from db.base import BaseModel
from db.engine import create_async_engine, get_session_maker, proceed_schemas
from handlers import register_user_commands
from middlewares.additional_parameter_transfer import SendingParameter
from service import pulling_data_for_each_page

bot = Bot(token=Config.TOKEN_API)
dp = Dispatcher(bot=bot)


async def main() -> None:
    postgres_url = URL.create(
        "postgresql+asyncpg",
        username=Config.USER,
        host=Config.HOST,
        database=Config.DB_NAME,
        password=Config.PASSWORD
    )
    async_engine = create_async_engine(postgres_url)
    session_maker = get_session_maker(async_engine)
    await proceed_schemas(async_engine, BaseModel.metadata)

    register_user_commands(dp)

    router = Router()
    router.message.middleware(SendingParameter())

    try:
        await dp.start_polling(bot, session_maker=session_maker)
    finally:
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped!')
