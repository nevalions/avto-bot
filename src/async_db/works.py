import asyncio

from sqlalchemy import Column, Integer, String, BigInteger, Text, ForeignKey, Boolean
from sqlalchemy import select, delete, update
from sqlalchemy.orm import relationship

from src.async_db.base import DATABASE_URL, Base, Database


class Work(Base):
    __tablename__ = 'work'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    is_regular = Column('is_regular', Boolean, default=False)
    description = Column('description', Text, default='')
    next_maintenance_after = Column('next_maintenance_after', BigInteger, default=0)
    is_custom = Column('is_custom', Boolean, default=False)
    # fk_user = Column('fk_user', ForeignKey(user.c.id), nullable=True)
    fk_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    users = relationship('User', back_populates='works')

    def __init__(
            self,
            title,
            is_regular,
            description='',
            next_maintenance_after=0,
            is_custom=False,
            fk_user=None
    ):
        super().__init__()
        self.title = title
        self.is_regular = is_regular
        self.description = description
        self.next_maintenance_after = next_maintenance_after
        self.is_custom = is_custom
        self.fk_user = fk_user

    def __repr__(self):
        if self.is_regular:
            fstring = (f'{self.title} regular: {self.is_regular}, '
                       f'next at: {self.next_maintenance_after}\n'
                       f'Description: {self.description}')
        else:
            fstring = (f'{self.title}\n'
                       f'Description: {self.description}')
        return fstring


class WorkService:
    def __init__(self, database):
        self.db = database

    async def add_work(
            self, title, is_regular, description='', next_maintenance_after=0,
            is_custom=False, fk_user=None
    ):
        async with self.db.async_session() as session:
            work = Work(
                title=title,
                is_regular=is_regular,
                description=description,
                next_maintenance_after=next_maintenance_after,
                is_custom=is_custom,
                fk_user=fk_user,

            )
            session.add(work)
            await session.commit()
            return work

    async def get_all_default_works(self, is_custom=False):
        async with self.db.async_session() as session:
            result = await session.execute(
                select(Work).order_by(Work.title).filter_by(is_custom=is_custom))

            all_default_works = []
            for work in result.scalars():
                all_default_works.append(vars(work))

            return all_default_works

    async def get_all_user_custom_works(self, user_id, is_custom=True):
        async with self.db.async_session() as session:
            result = await session.execute(select(Work).order_by(Work.title).filter_by(
                fk_user=user_id, is_custom=is_custom)
            )

            all_user_custom_works = []
            for work in result.scalars():
                all_user_custom_works.append(vars(work))

            return all_user_custom_works

    async def get_work_by_id(self, work_id):
        async with self.db.async_session() as session:
            return await session.execute(select(Work).filter_by(id=work_id))

    async def update_work_title(self, work_id, new_title):
        async with self.db.async_session() as session:
            await session.execute(
                update(Work).where(Work.id == work_id).values(title=new_title))
            await session.commit()

    async def update_work_is_regular(self, work_id, new_is_regular):
        async with self.db.async_session() as session:
            await session.execute(update(Work).where(
                Work.id == work_id).values(is_regular=new_is_regular))
            await session.commit()

    async def update_work_description(self, work_id, new_description):
        async with self.db.async_session() as session:
            await session.execute(update(Work).where(
                Work.id == work_id).values(description=new_description))
            await session.commit()

    async def update_work_next_maintenance_after(
            self, work_id, new_next_maintenance_after
    ):
        async with self.db.async_session() as session:
            await session.execute(update(Work).where(Work.id == work_id).values(
                next_maintenance_after=new_next_maintenance_after))
            await session.commit()

    async def delete_work(self, work_id):
        async with self.db.async_session() as session:
            await session.execute(delete(Work).filter_by(id=work_id))
            await session.commit()


async def async_main() -> None:
    db = Database(DATABASE_URL)
    work_service = WorkService(db)

    # work = await work_service.add_work('Change Brake Pads', True, '', 10000)
    # print(work)

    # default_works = await work_service.get_all_default_works()
    # print(default_works)

    user_works = await work_service.get_all_user_custom_works(2)
    print(user_works)

    await db.engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
