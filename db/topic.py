from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy import select, update
from sqlalchemy.orm import sessionmaker

from .base import BaseModel


class Topic(BaseModel):
    __tablename__ = 'topic'

    id = Column(Integer, autoincrement=True, primary_key=True)
    name = Column(String)


async def get_topic(session_maker: sessionmaker) -> list[str]:
    async with session_maker() as session:
        async with session.begin():
            result = await session.execute(
                select(Topic.name))

            return result.scalars().fetchall()
