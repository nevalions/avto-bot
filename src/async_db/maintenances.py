import asyncio
from datetime import datetime

from sqlalchemy import (TIMESTAMP, BigInteger, Column, ForeignKey, Integer,
                        String, Text, delete, func, select, update)

from src.async_db.base import DATABASE_URL, Base, Database
from src.models.models import car, maintenance, work


class Maintenance(Base):
    __tablename__ = 'maintenance'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    title = Column('title', String, nullable=False)
    date = Column('date', TIMESTAMP, default=func.utcnow())
    maintenance_mileage = Column(
        'maintenance_mileage', BigInteger, nullable=False)
    description = Column('description', Text, default='')
    fk_car = Column('fk_car', ForeignKey(car.c.id), nullable=True)

    def __init__(
            self,
            title,
            maintenance_mileage,
            date=datetime.utcnow(),
            description='',
            fk_car=None
    ):
        self.title = title
        self.maintenance_mileage = maintenance_mileage
        self.date = date
        self.description = description
        self.fk_car = fk_car

    def __repr__(self):
        if self.description == '':
            fstring = f'{self.title} {self.date}, with {self.maintenance_mileage}'
        else:
            fstring = (f'{self.title} {self.date}, with {self.maintenance_mileage},\n'
                       f'Description: {str(self.description)}')
        return fstring


class MaintWork(Base):
    __tablename__ = 'maint_work'
    __table_args__ = {'extend_existing': True}

    fk_maintenances = Column('fk_maintenances', ForeignKey(
        maintenance.c.id), nullable=False, primary_key=True)
    fk_work = Column('fk_work', ForeignKey(work.c.id), nullable=False)

    def __init__(
            self,
            fk_maintenance,
            fk_work,
    ):
        self.fk_maintenance = fk_maintenance
        self.fk_work = fk_work


class MaintenanceService:
    def __init__(self, database):
        self.db = database

    async def add_maintenance(
            self,
            title,
            maintenance_mileage,
            date=datetime.utcnow(),
            description='',
            fk_car=None
    ):
        async with self.db.async_session() as session:
            maintenance = Maintenance(
                title=title,
                maintenance_mileage=maintenance_mileage,
                date=date,
                description=description,
                fk_car=fk_car
            )
            session.add(maintenance)
            await session.commit()
            return maintenance

    async def m2m_maint_work(self, fk_maintenance, fk_work):
        async with self.db.async_session() as session:
            m2m_maint_work = MaintWork(
                fk_maintenance=fk_maintenance, fk_work=fk_work)
            session.add(m2m_maint_work)
            await session.commit()
            return m2m_maint_work

    async def get_all_car_maintenances(self, car_id):
        async with self.db.async_session() as session:
            result = await session.execute(
                select(Maintenance).order_by(
                    Maintenance.date).filter_by(fk_car=car_id)
            )

            all_car_maintenances = []
            for maint in result.scalars():
                all_car_maintenances.append(vars(maint))

            return all_car_maintenances

    async def get_car_maintenance_by_id(self, maintenance_id):
        async with self.db.async_session() as session:
            return await session.execute(
                select(Maintenance).filter_by(id=maintenance_id)
            )

    async def update_maintenance_title(self, maint_id, new_title):
        async with self.db.async_session() as session:
            await session.execute(
                update(Maintenance).where(Maintenance.id == maint_id).values(
                    title=new_title)
            )
            await session.commit()

    async def update_maintenance_date(self, maint_id, new_date):
        async with self.db.async_session() as session:
            await session.execute(
                update(Maintenance).where(Maintenance.id == maint_id).values(
                    date=new_date)
            )
            await session.commit()

    async def update_maintenance_mileage(self, maint_id, new_maintenance_mileage):
        async with self.db.async_session() as session:
            await session.execute(update(Maintenance).where(
                Maintenance.id == maint_id).values(
                maintenance_mileage=new_maintenance_mileage))
            await session.commit()

    async def update_maintenance_description(self, maint_id, new_description):
        async with self.db.async_session() as session:
            await session.execute(update(Maintenance).where(
                Maintenance.id == maint_id).values(
                description=new_description))
            await session.commit()

    async def delete_maintenance(self, maintenance_id):
        async with self.db.async_session() as session:
            await session.execute(delete(Maintenance).filter_by(id=maintenance_id))
            await session.commit()


async def async_main() -> None:
    db = Database(DATABASE_URL)
    maintenance_service = MaintenanceService(db)

    maint = await maintenance_service.add_maintenance(
        title='TO3', maintenance_mileage=100, description='Some works3', fk_car=1
    )
    print(maint)

    # maints_show = await maintenance_service.get_all_car_maintenances(7)
    # print(maints_show)

    maint_show = await maintenance_service.get_car_maintenance_by_id(1)
    print(vars(*maint_show.one_or_none()))

    # await maintenance_service.m2m_maint_work(1, 3)

    await db.engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
