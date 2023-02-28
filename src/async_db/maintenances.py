import asyncio
from pprint import pprint

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, BigInteger, Text, ForeignKey, Boolean
from sqlalchemy import func
from sqlalchemy import select, delete, update

from sqlalchemy.orm import relationship

from src.models.models import users, cars
from src.async_db.base import DATABASE_URL, Base, Database


class Maintenance(Base):
    __tablename__ = 'maintenances'
    __table_args__ = {'extend_existing': True}

    title = Column('title', String, nullable=False),
    date = Column('date', TIMESTAMP, default=func.utcnow()),
    current_mileage = Column('current_mileage', BigInteger, nullable=False),
    description = Column('description', Text, default=''),
    fk_cars = Column('fk_cars', ForeignKey(cars.c.id), nullable=True)

    def __init__(
            self,
            title,
            current_mileage,
            date=datetime.utcnow(),
            description='',
            fk_cars=None,
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

    title = Column('title', String, nullable=False),
    is_regular = Column('is_regular', Boolean, default=False),
    description = Column('description', Text, default=''),
    next_maintenance_after = Column('next_maintenance_after', BigInteger, default=0)

    def __init__(
            self,
            title,
            is_regular,
            description='',
            next_maintenance_after=0
    ):
        self.title = title
        self.is_regular = is_regular
        self.description = description
        self.next_maintenance_after = next_maintenance_after

    def __repr__(self):
        if self.is_regular:
            fstring = (f'{self.title} regular: {self.is_regular}, next at: {self.next_maintenance_after}\n'
                       f'Description: {self.description}')
        else:
            fstring = (f'{self.title}\n'
                       f'Description: {self.description}')
        return fstring
