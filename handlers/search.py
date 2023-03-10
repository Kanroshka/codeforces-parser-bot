from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from db.assignment import get_assignments_by_id


class TaskStates(StatesGroup):
    id_task = State()


async def search_task(message: types.Message, state: FSMContext,
                      session_maker: sessionmaker) -> None:
    await message.answer("Введите номер задачи")
    await state.set_state(TaskStates.id_task)


async def wait_for_task_name(message: types.Message, state: FSMContext,
                             session_maker: sessionmaker) -> None:
    data = await state.update_data(id_task=message.text)
    await state.clear()
    try:
        contest_task = await get_assignments_by_id(data['id_task'], session_maker)
        await message.answer(
            f"№{contest_task[0][0]} \nНазвание - {contest_task[0][1]}\n"
            f"Сложность - {contest_task[0][2]}\nРешили - х{contest_task[0][3]}")
    except Exception:
        await message.answer("Задачи не существует, повторите попытку. "
                             "Для отмены действия напишите '/cancel'")
        await search_task(message, state, session_maker)
