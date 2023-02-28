import asyncio
from pprint import pprint

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, Text, ForeignKey, Boolean
from sqlalchemy import func
from sqlalchemy import select, delete, update

from sqlalchemy.orm import relationship

from src.models.models import cars, users, maintenances, works
from src.async_db.base import DATABASE_URL, Base, Database


class Maintenance(Base):
    __tablename__ = 'maintenances'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    date = Column('date', TIMESTAMP, default=func.utcnow())
    current_mileage = Column('current_mileage', BigInteger, nullable=False)
    description = Column('description', Text, default='')
    fk_cars = Column('fk_cars', ForeignKey(cars.c.id), nullable=True)

    def __init__(
            self,
            title,
            current_mileage,
            date=datetime.utcnow(),
            description='',
            fk_cars=None
    ):
        self.title = title
        self.current_mileage = current_mileage
        self.date = date
        self.description = description
        self.fk_cars = fk_cars

    def __repr__(self):
        if self.description == '':
            fstring = f'{self.title} {self.date}, with {self.current_mileage}'
        else:
            fstring = (f'{self.title} {self.date}, with {self.current_mileage},\n'
                       f'Description: {str(self.description)}')
        return fstring


class Work(Base):
    __tablename__ = 'works'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    is_regular = Column('is_regular', Boolean, default=False)
    description = Column('description', Text, default='')
    next_maintenance_after = Column('next_maintenance_after', BigInteger, default=0)
    is_custom = Column('is_custom', Boolean, default=False)
    fk_users = Column('fk_users', ForeignKey(users.c.id), nullable=True)

    def __init__(
            self,
            title,
            is_regular,
            description='',
            next_maintenance_after=0,
            is_custom=False,
            fk_users=None
    ):
        self.title = title
        self.is_regular = is_regular
        self.description = description
        self.next_maintenance_after = next_maintenance_after
        self.is_custom = is_custom
        self.fk_users = fk_users

    def __repr__(self):
        if self.is_regular:
            fstring = (f'{self.title} regular: {self.is_regular}, next at: {self.next_maintenance_after}\n'
                       f'Description: {self.description}')
        else:
            fstring = (f'{self.title}\n'
                       f'Description: {self.description}')
        return fstring


class MaintsWorks(Base):
    __tablename__ = 'maints_works'
    __table_args__ = {'extend_existing': True}

    fk_maintenances = Column('fk_maintenances', ForeignKey(maintenances.c.id), nullable=False, primary_key=True)
    fk_works = Column('fk_works', ForeignKey(works.c.id), nullable=False)

    def __init__(
            self,
            fk_maintenances,
            fk_works,
    ):
        self.fk_maintenances = fk_maintenances
        self.fk_works = fk_works


class MaintenanceService:
    def __init__(self, database):
        self.db = database

    async def add_maintenance(self, title, current_mileage, date=datetime.utcnow(), description='', fk_cars=None):
        async with self.db.async_session() as session:
            maintenance = Maintenance(
                title=title,
                current_mileage=current_mileage,
                date=date,
                description=description,
                fk_cars=fk_cars
            )
            session.add(maintenance)
            await session.commit()
            return maintenance

    async def m2m_maints_works(self, fk_maintenances, fk_works):
        async with self.db.async_session() as session:
            m2m_maints_works = MaintsWorks(fk_maintenances=fk_maintenances, fk_works=fk_works)
            session.add(m2m_maints_works)
            await session.commit()
            return m2m_maints_works


class WorkService:
    def __init__(self, database):
        self.db = database

    async def add_work(
            self, title, is_regular, description='', next_maintenance_after=0, is_custom=False, fk_users=None
    ):
        async with self.db.async_session() as session:
            work = Work(
                title=title,
                is_regular=is_regular,
                description=description,
                next_maintenance_after=next_maintenance_after,
                is_custom=is_custom,
                fk_users=fk_users,

            )
            session.add(work)
            await session.commit()
            return work

    async def get_all_default_works(self, is_custom=False):
        async with self.db.async_session() as session:
            result = await session.execute(select(Work).order_by(Work.title).filter_by(is_custom=is_custom))

            all_default_works = []
            for work in result.scalars():
                all_default_works.append(vars(work))

            return all_default_works

    async def get_all_user_custom_works(self, user_id, is_custom=True):
        async with self.db.async_session() as session:
            result = await session.execute(select(Work).order_by(Work.title).filter_by(
                fk_users=user_id, is_custom=is_custom)
            )

            all_user_custom_works = []
            for work in result.scalars():
                all_user_custom_works.append(vars(work))

            return all_user_custom_works


async def async_main() -> None:
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)
    work_service = WorkService(db)


    # maint = await maintenance_service.add_maintenance(
    #     title='TO2', current_mileage=320000, description='Some works2', fk_cars=7
    # )
    # print(maint)
    #
    # work = await work_service.add_work('Change Brake Pads', True, '', 10000)
    # print(work)

    # await maintenance_service.m2m_maints_works(1, 3)

    # default_works = await work_service.get_all_default_works()
    # print(default_works)

    user_works = await work_service.get_all_user_custom_works(2)
    print(user_works)

    await db.engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
