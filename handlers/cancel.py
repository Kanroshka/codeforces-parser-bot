from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from db.assignment import get_assignments_by_id


async def cancel_handler(message: types.Message, state: FSMContext,
                         session_maker: sessionmaker) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return

    await state.clear()
    await message.answer("Действие отменено.")
