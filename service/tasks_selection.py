from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db.assignment import Assignment, AssignmentTopics
from db.topic import Topic


async def selection(ot: int,
                    do: int,
                    topic: str,
                    name_trend: str,
                    session_maker: sessionmaker) -> dict:
    tasks = {}
    async with session_maker() as session:
        async with session.begin():
            list_task = (await session.execute(select(Assignment).filter(
                Assignment.difficulty.between(ot, do),
                Assignment.booking == False, Assignment.id == (
                    select(AssignmentTopics.assignment_id).filter(
                        AssignmentTopics.topic_id == (
                            select(Topic.id).filter(Topic.name == topic)),
                        AssignmentTopics.assignment_id == Assignment.id))).limit(
                10))).scalars().fetchall()

            for i in list_task:
                i.booking = True
                i.contest_name = name_trend
                temi = (await session.execute(
                    select(AssignmentTopics.topic_id).filter(
                        i.id == AssignmentTopics.assignment_id))).scalars().fetchall()

                temiz = []
                for j in temi:
                    temiz.append(''.join((await session.execute(
                        select(Topic.name).filter(
                            Topic.id == j))).scalars().fetchall()))

                tasks[i.id] = [i.name, i.difficulty, i.solved_by, temiz]

    return tasks
