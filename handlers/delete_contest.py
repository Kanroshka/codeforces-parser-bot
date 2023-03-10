from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from db.assignment import get_all_contest, get_contest_assignments_by_name, \
    update_assignment


class ContestDelateStates(StatesGroup):
    name_contest = State()


async def delete_contest(message: types.Message, state: FSMContext,
                  session_maker: sessionmaker) -> None:
    contests_name = '\n - '.join(
        list(await get_all_contest(session_maker=session_maker)))

    await message.answer(
        f"Введите имя контеста из доступных, который хотете удалить\n - {contests_name}\n (/cancel для отмены)")
    await state.set_state(ContestDelateStates.name_contest)


async def wait_for_contest_naame(message: types.Message, state: FSMContext,
                                 session_maker: sessionmaker) -> None:
    data = await state.update_data(name=message.text)
    await state.clear()

    try:
        contests_name = list(await get_all_contest(session_maker=session_maker))
        if data['name'] not in contests_name:
            raise Exception

        res = await get_contest_assignments_by_name(data['name'], session_maker)
        for i in res:
            await update_assignment(i.id,
                                    update_flag=False,
                                    session_maker=session_maker)
        await message.answer("Успешно!")
    except Exception:
        await message.answer("Контест не существует, повторите попытку. "
                             "Для отмены действия напишите '/cancel'")
        await delete_contest(message, state, session_maker)
