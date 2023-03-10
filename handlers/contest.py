from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from db.assignment import get_all_contest, get_contest_assignments_by_name


class ContestStates(StatesGroup):
    name_contest = State()


async def contest(message: types.Message, state: FSMContext,
                  session_maker: sessionmaker) -> None:
    contests_name = '\n -'.join(
        list(await get_all_contest(session_maker=session_maker)))

    await message.answer(
        f"Введите имя контеста из доступных\n -{contests_name}\n (/cancel для отмены)")
    await state.set_state(ContestStates.name_contest)


async def wait_for_contest_namee(message: types.Message, state: FSMContext,
                                 session_maker: sessionmaker) -> None:
    data = await state.update_data(name=message.text)
    await state.clear()

    await message.answer(f"Список задач по контесту - {data['name']}")

    try:
        contest_tasks = await get_contest_assignments_by_name(data['name'],
                                                              session_maker)
        for contest_task in contest_tasks:
            await message.answer(
                f"№{contest_task[0]} \nНазвание - {contest_task[1]}")
    except Exception:
        await message.answer("Контест не существует, повторите попытку. "
                             "Для отмены действия напишите '/cancel'")
        await contest(message, state, session_maker)
