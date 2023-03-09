import asyncio

from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP
from sqlalchemy import func
from sqlalchemy import select
from sqlalchemy.orm import relationship

from src.async_db.base import DATABASE_URL, Base, Database


class User(Base):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    username = Column('username', String)
    email = Column('email', String)
    registered_at = Column('registered_at', TIMESTAMP, default=func.utcnow())

    tg_users = relationship(
        'TgUser', cascade="all, delete", back_populates="users",
        passive_deletes=True)
    cars = relationship(
        'Car', cascade="all, delete-orphan", back_populates="users",
        passive_deletes=True)
    works = relationship(
        'Work', cascade="all, delete-orphan", back_populates="users",
        passive_deletes=True)

    def __init__(self, username, email, registered_at=datetime.utcnow()):
        super().__init__()
        self.username = username
        self.email = email
        self.registered_at = registered_at

    def __repr__(self):
        return f'({self.id}) {self.username} {self.email} ' \
               f'registered at {self.registered_at}'


class UserService:
    def __init__(self, database):
        self.db = database

    async def add_user(self, username, email):
        async with self.db.async_session() as session:
            user = User(username=username, email=email)
            session.add(user)
            await session.commit()
            return user

    async def get_user_by_id(self, user_id):
        async with self.db.async_session() as session:
            user = await session.execute(select(User).filter_by(id=user_id))
            return user.scalars().one_or_none()

    async def get_user_by_email(self, user_email):
        async with self.db.async_session() as session:
            user = await session.execute(select(User).filter_by(email=user_email))
            return user.scalars().one_or_none()

    async def update_username(self, username, user_id):
        async with self.db.async_session() as session:
            result = await session.execute(select(User).filter_by(id=user_id))

            user = result.scalars().one_or_none()
            if user:
                user.username = username
            else:
                print('Error changing username')

            await session.commit()
            return user


async def async_main() -> None:
    db = Database(DATABASE_URL)
    user_service = UserService(db)
    # await user_service.add_user('John Doe', 'mail@mail.ru')
    #
    # # found_user = await user_service.get_user_by_id(14)
    # found_user = await user_service.get_user_by_email('mail@mail.ru')
    # print(vars(found_user)['email'])
    # print(found_user.__dict__)
    # print(found_user.username)
    # x = [*vars(found_user).values()]
    # print(x[1:])
    # change_username = await user_service.update_username('ROOT', found_user.id)
    # print(vars(change_username))
    # print(vars(found_user))
    #
    # await db.engine.dispose()

if __name__ == '__main__':
    asyncio.run(async_main())
