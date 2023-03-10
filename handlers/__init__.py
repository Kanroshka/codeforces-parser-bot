from aiogram import Router
from aiogram.filters.command import CommandStart, Command

from handlers.cancel import cancel_handler
from handlers.contest import contest, ContestStates, wait_for_contest_namee
from handlers.delete_contest import delete_contest, wait_for_contest_naame, \
    ContestDelateStates
from handlers.search import search_task, wait_for_task_name, TaskStates
from handlers.start import start
from handlers.filtering import filter, wait_for_complexity_from, FilterStates, \
    wait_for_contest_name, wait_for_complexity_up_to, \
    waiting_for_selection_topic


def register_user_commands(router: Router) -> None:
    router.message.register(start, CommandStart())
    router.message.register(filter, Command(commands=["filter"]))
    router.message.register(contest, Command(commands=["contest"]))
    router.message.register(search_task, Command(commands=["search"]))
    router.message.register(cancel_handler, Command(commands=["cancel"]))
    router.message.register(delete_contest, Command(commands=["delete"]))
    router.message.register(wait_for_complexity_from,
                            FilterStates.complexity_from)
    router.message.register(wait_for_complexity_up_to,
                            FilterStates.complexity_up_to)
    router.message.register(wait_for_contest_name,
                            FilterStates.contest_name)
    router.message.register(waiting_for_selection_topic,
                            FilterStates.selection_topic)
    router.message.register(wait_for_contest_namee,
                            ContestStates.name_contest)
    router.message.register(wait_for_task_name,
                            TaskStates.id_task)
    router.message.register(wait_for_contest_naame,
                            ContestDelateStates.name_contest)


register_user_handlers = register_user_commands
