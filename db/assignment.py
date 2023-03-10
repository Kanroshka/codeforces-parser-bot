from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy import select
from sqlalchemy.orm import relationship, sessionmaker

from .base import BaseModel


class Assignment(BaseModel):
    __tablename__ = "assignment"

    id = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    difficulty = Column(Integer, nullable=False)
    solved_by = Column(Integer, nullable=False)
    booking = Column(Boolean, default=False)
    contest_name = Column(String, nullable=True)

    topics = relationship('Topic', secondary='assignment_topic')


async def update_assignment(assignment_id: str,
                            session_maker: sessionmaker,
                            complexity: int = 0,
                            solved_by: int = 0,
                            update_flag: bool = False
                            ) -> None:
    async with session_maker() as session:
        async with session.begin():
            old_assignment = (await session.execute(select(
                Assignment).where(Assignment.id == assignment_id))
                              ).scalars().fetchall()
            if update_flag:
                old_assignment[0].solved_by = solved_by
                old_assignment[0].difficulty = complexity
            else:
                old_assignment[0].booking = False
                old_assignment[0].contest_name = None


async def get_assignments_by_id(id: str, session_maker: sessionmaker) -> list:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Assignment.id, Assignment.name, Assignment.difficulty,
                       Assignment.solved_by, Assignment.contest_name).filter(
                    Assignment.id == id)
            )

            return result.fetchall()


async def get_contest_assignments_by_name(name: str,
                                          session_maker: sessionmaker) -> list:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Assignment.id, Assignment.name).filter(
                    Assignment.contest_name == name)
            )

            return result


async def get_all_contest(session_maker: sessionmaker) -> set[str]:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Assignment.contest_name).filter(
                    Assignment.contest_name != None)
            )

            return set(result.scalars().fetchall())


class AssignmentTopics(BaseModel):
    __tablename__ = 'assignment_topic'

    assignment_id = Column(String, ForeignKey('assignment.id'),
                           primary_key=True)
    topic_id = Column(Integer, ForeignKey('topic.id'), primary_key=True)
