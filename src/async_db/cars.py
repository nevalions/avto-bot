import asyncio

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, Text, ForeignKey
from sqlalchemy import func
from sqlalchemy import select, delete, update

from sqlalchemy.orm import relationship

from src.models.models import user
from src.async_db.base import DATABASE_URL, Base, Database


class Car(Base):
    __tablename__ = 'car'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    model = Column('model', String)
    model_name = Column('model_name', String)
    mileage = Column('mileage', BigInteger)
    current_mileage = Column('current_mileage', BigInteger)
    measures = Column('measures', String)
    date_added = Column('date_added', TIMESTAMP, default=func.utcnow())
    description = Column('description', Text)
    fk_user = Column(Integer, ForeignKey(user.c.id))

    def __init__(
            self,
            model,
            model_name,
            mileage,
            current_mileage,
            measures,
            date_added=datetime.utcnow(),
            description='',
            fk_user=None,
    ):
        self.model = model
        self.model_name = model_name
        self.mileage = mileage
        self.current_mileage = current_mileage
        self.measures = measures
        self.date_added = date_added
        self.description = description
        self.fk_user = fk_user

    def __repr__(self):
        return f'({self.id}) {self.model} {self.model_name} registered at {self.date_added} ' \
               f'with {self.mileage} {self.measures}, user_id ({self.fk_user})'


class CarService:
    def __init__(self, database):
        self.db = database

    async def add_car(self, model, model_name, mileage, measures, description='', fk_user=None):
        async with self.db.async_session() as session:
            car = Car(
                model=model,
                model_name=model_name,
                mileage=mileage,
                current_mileage=mileage,
                measures=measures,
                description=description,
                fk_user=fk_user
            )
            session.add(car)
            await session.commit()
            return car

    async def get_car_by_id(self, car_id):
        async with self.db.async_session() as session:
            car = await session.execute(select(Car).filter_by(id=car_id))
            return car.scalars().one_or_none()

    async def get_all_cars(self):
        async with self.db.async_session() as session:
            result = await session.execute(select(Car))

            all_cars = []
            for car in result.scalars():
                all_cars.append(vars(car))

            return all_cars

    async def get_all_user_cars(self, user_id):
        async with self.db.async_session() as session:
            result = await session.execute(select(Car).order_by(Car.model).filter_by(fk_user=user_id))

            all_user_cars = []
            for car in result.scalars():
                all_user_cars.append(vars(car))

            return all_user_cars

    async def update_car_model(self, car_id, new_model):
        async with self.db.async_session() as session:
            await session.execute(update(Car).where(Car.id == car_id).values(model=new_model))
            await session.commit()

    async def update_car_model_name(self, car_id, new_model_name):
        async with self.db.async_session() as session:
            await session.execute(update(Car).where(Car.id == car_id).values(model_name=new_model_name))
            await session.commit()

    async def update_car_current_mileage(self, car_id, current_mileage):
        async with self.db.async_session() as session:
            await session.execute(update(Car).where(Car.id == car_id).values(current_mileage=current_mileage))
            await session.commit()

    async def update_car_description(self, car_id, description):
        async with self.db.async_session() as session:
            await session.execute(update(Car).where(Car.id == car_id).values(description=description))
            await session.commit()

    async def delete_car(self, car_id):
        async with self.db.async_session() as session:
            await session.execute(delete(Car).filter_by(id=car_id))
            await session.commit()


async def async_main() -> None:
    db = Database(DATABASE_URL)
    car_service = CarService(db)
    # car = await car_service.add_car('Gmc', 'Savana', 300000, 'miles', fk_user=1)
    # print(car)
    # print(vars(car))

    # car = await car_service.add_car('Chevrolet', 'Astro', 100000, 'miles', fk_user=2)
    # print(car)
    # print(vars(car))

    # all_cars = await car_service.get_all_cars()
    # pprint(all_cars)
    #
    # await car_service.delete_car(9)
    #
    # all_user_cars = await car_service.get_all_user_cars(1)
    # pprint((all_user_cars))
    await car_service.update_car_model(10, 'Ford')
    # await car_service.update_car_current_mileage(10, 22222222)

    await db.engine.dispose()


if __name__ == '__main__':
    asyncio.run(async_main())
