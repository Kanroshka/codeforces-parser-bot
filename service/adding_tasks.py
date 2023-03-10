from sqlalchemy import select
from sqlalchemy.orm import sessionmaker

from db.assignment import Assignment, AssignmentTopics, \
    get_assignments_by_id, update_assignment
from db.topic import Topic


async def initial_data_collection(number: str,
                                  name_assigment: str,
                                  complexity: int,
                                  number_of_decisions: int,
                                  topics: str,
                                  session_maker: sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            assignment_test = await get_assignments_by_id(number, session_maker)
            if assignment_test:
                await update_assignment(assignment_test[0][0],
                                        session_maker,
                                        complexity,
                                        number_of_decisions,
                                        True)

                return

            assignment = Assignment(
                id=number,
                name=name_assigment,
                difficulty=complexity,
                solved_by=number_of_decisions,
            )
            session.add(assignment)

            for topicc in topics:
                topic = Topic(name=topicc)

                flag = (await session.execute(select(
                    Topic.name).where(Topic.name == topic.name))
                        ).scalars().unique().one_or_none()
                if not flag:
                    session.add(topic)

                topic_id = (await session.execute(
                    select(Topic.id).where(Topic.name == topic.name))
                            ).scalars().unique().one_or_none()

                flag = (await session.execute(select(
                    AssignmentTopics.assignment_id).where(
                    AssignmentTopics.assignment_id == assignment.id,
                    AssignmentTopics.topic_id == topic_id))
                        ).scalars().unique().one_or_none()

                if not flag:
                    new_task_topic = AssignmentTopics(
                        assignment_id=assignment.id,
                        topic_id=topic_id)
                    session.add(new_task_topic)
