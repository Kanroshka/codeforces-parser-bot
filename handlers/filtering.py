from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from sqlalchemy.orm import sessionmaker

from db.assignment import get_all_contest
from db.topic import get_topic
from service.tasks_selection import selection


class FilterStates(StatesGroup):
    complexity_from = State()
    complexity_up_to = State()
    contest_name = State()
    selection_topic = State()


async def filter(message: types.Message, state: FSMContext,
                 session_maker: sessionmaker) -> None:
    await message.answer(f"Введите от какой сложности выбрать задачи")
    await state.set_state(FilterStates.complexity_from)


async def wait_for_complexity_from(message: types.Message, state: FSMContext,
                                   session_maker: sessionmaker) -> None:
    await state.update_data(complexity_from=int(message.text))
    await message.answer(f"Введите до какой сложности выбрать задачи")

    await state.set_state(FilterStates.complexity_up_to)


async def wait_for_complexity_up_to(message: types.Message, state: FSMContext,
                                    session_maker: sessionmaker) -> None:
    await state.update_data(complexity_up_to=int(message.text))
    topics = '\n- '.join((await get_topic(session_maker=session_maker)))
    await message.answer(f"Введите одну тему задач из доступных: \n{topics}")

    await state.set_state(FilterStates.selection_topic)


async def waiting_for_selection_topic(message: types.Message,
                                      state: FSMContext,
                                      session_maker: sessionmaker) -> None:
    await state.update_data(selection_topic=message.text)
    await message.answer(
        f"Введите имя констеста под котором будут сохранены задачи")

    await state.set_state(FilterStates.contest_name)


async def wait_for_contest_name(message: types.Message, state: FSMContext,
                                session_maker: sessionmaker) -> None:
    data = await state.update_data(name=message.text)
    await state.clear()

    contests_name = list(await get_all_contest(session_maker=session_maker))
    if data['name'] in contests_name:
        await message.answer(
            f"Такой контест существует. Повторите попытку."
            f"Для отмены действия напишите '/cancel'")
        await filter(message, state, session_maker)
        return

    try:
        tasks = await selection(data['complexity_from'],
                                data['complexity_up_to'],
                                data['selection_topic'],
                                data['name'],
                                session_maker=session_maker)
    except Exception:
        await message.answer("Таких задач не существует, повторите попытку. "
                             "Для отмены действия напишите '/cancel'")
        await filter(message, state, session_maker)

    if tasks:
        await message.answer("Подобранные задачи: ")

        for key, values in tasks.items():
            await message.answer(f"№{key}\nНазвание - {values[0]}\n"
                                 f"Сложность - {values[1]}\nРешили - х{values[2]}\n"
                                 f"Темы - {', '.join(values[3])}")

        await message.answer(
            f"Данные задачи сохранены в контекст - {data['name']}")

    else:
        await message.answer("Таких задач не существует, повторите попытку. "
                             "Для отмены действия напишите '/cancel'")
        await filter(message, state, session_maker)
