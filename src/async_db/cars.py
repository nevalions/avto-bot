import asyncio

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, Text, ForeignKey
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import relationship

from models.models import users
from src.async_db.base import DATABASE_URL, Base, Database


class Car(Base):
    __tablename__ = 'cars'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    model = Column('model', String)
    model_name = Column('model_name', String)
    mileage = Column('mileage', BigInteger)
    current_mileage = Column('current_mileage', BigInteger)
    measures = Column('measures', String)
    date_added = Column('date_added', TIMESTAMP, default=func.utcnow())
    description = Column('description', Text)
    fk_users = Column(Integer, ForeignKey(users.c.id))

    def __init__(
            self,
            model,
            model_name,
            mileage,
            current_mileage,
            measures,
            date_added=datetime.utcnow(),
            description='',
            fk_users=None,
    ):
        self.model = model
        self.model_name = model_name
        self.mileage = mileage
        self.current_mileage = current_mileage
        self.measures = measures
        self.date_added = date_added
        self.description = description
        self.fk_users = fk_users

    def __repr__(self):
        return f'({self.id}) {self.model} {self.model_name} registered at {self.date_added} ' \
               f'with {self.mileage} {self.measures}, user_id ({self.fk_users})'


class CarService:
    def __init__(self, database):
        self.db = database

    async def add_car(self, model, model_name, mileage, measures, description='', fk_users=None):
        async with self.db.async_session() as session:
            car = Car(
                model=model,
                model_name=model_name,
                mileage=mileage,
                current_mileage=mileage,
                measures=measures,
                description=description,
                fk_users=fk_users
            )
            session.add(car)
            await session.commit()
            return car


async def async_main() -> None:
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    car = await car_service.add_car('Gmc', 'Savana', 300000, 'miles', fk_users=1)
    print(car)
    print(vars(car))
    await db.engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
