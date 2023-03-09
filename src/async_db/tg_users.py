import asyncio

from sqlalchemy import ForeignKey, Column, Integer, String, BigInteger
from sqlalchemy import select
from sqlalchemy.orm import relationship

from src.async_db.base import DATABASE_URL, Base, Database


class TgUser(Base):
    __tablename__ = 'tg_user'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    tg_user_id = Column('tg_user_id', BigInteger)
    chat_id = Column('chat_id', BigInteger)
    tg_username = Column('tg_username', String)
    tg_firstname = Column('tg_firstname', String)
    tg_lastname = Column('tg_lastname', String)
    fk_user = Column(Integer, ForeignKey('user.id', ondelete='CASCADE'), nullable=False)

    users = relationship('User', back_populates='tg_users')

    def __init__(
            self,
            chat_id,
            tg_username,
            tg_firstname,
            tg_lastname,
            fk_user=None,
            tg_user_id=None
    ):
        super().__init__()
        self.chat_id = chat_id
        self.tg_username = tg_username
        self.tg_firstname = tg_firstname
        self.tg_lastname = tg_lastname
        self.fk_user = fk_user
        self.tg_user_id = tg_user_id

    def __repr__(self):
        return f'({self.id}) {self.chat_id} {self.tg_username} {self.tg_firstname} ' \
               f'{self.tg_lastname} ' \
               f'connected to user {self.fk_user}'


class TgUserService:
    def __init__(self, database):
        self.db = database

    async def add_tg_user(
            self,
            chat_id,
            tg_username,
            tg_firstname,
            tg_lastname,
            fk_user=None,
            tg_user_id=None,
    ):
        async with self.db.async_session() as session:
            tg_user = TgUser(
                chat_id=chat_id,
                tg_username=tg_username,
                tg_firstname=tg_firstname,
                tg_lastname=tg_lastname,
                fk_user=fk_user,
                tg_user_id=tg_user_id
            )
            session.add(tg_user)
            await session.commit()
            return tg_user

    async def get_tg_user_by_id(self, tg_id):
        async with self.db.async_session() as session:
            tg_user = await session.execute(select(TgUser).filter_by(id=tg_id))
            return tg_user.scalars().one_or_none()

    async def get_tg_user_by_chat_id(self, chat_id):
        async with self.db.async_session() as session:
            tg_user = await session.execute(select(TgUser).filter_by(chat_id=chat_id))
            return tg_user.scalars().one_or_none()

    async def get_all_tg_users(self):
        async with self.db.async_session() as session:
            result = await session.execute(select(TgUser))

            all_tg_users = []
            for tg_user in result.scalars():
                all_tg_users.append(vars(tg_user))

            return all_tg_users

    async def add_tg_user_register(self, tg_user_id, fk_user, chat_id):
        async with self.db.async_session() as session:
            result = await session.execute(select(TgUser).filter_by(chat_id=chat_id))

            tg_user = result.scalars().one_or_none()
            if tg_user:
                tg_user.tg_user_id = tg_user_id
                tg_user.fk_user = fk_user
            else:
                print('Error user adding to tg_user')

            await session.commit()
            return tg_user


async def async_main() -> None:
    db = Database(DATABASE_URL)
    tg_user_service = TgUserService(db)

    # tg_user = await tg_user_service.add_tg_user(13, 'test_tg', 'tg1', 'tg2')
    # print(vars(tg_user))

    found_tg_user = await tg_user_service.get_all_tg_users()
    found_tg_user = await tg_user_service.get_tg_user_by_chat_id(84891021)
    # found_tg_user = await tg_user_service.get_tg_user_by_id(26)
    print(vars(found_tg_user))

    register_user = await tg_user_service.add_tg_user_register()

    # engine = create_async_engine(DATABASE_URL, echo=True)
    # async_session = async_sessionmaker(engine, expire_on_commit=False)

    # try:
    #     await insert_tg_user(async_session, 12, 'test_tg', 'tg1', 'tg2')
    # except Exception as ex:
    #     print(ex)
    #
    # try:
    #     all_tg_users = await find_all_tg_users(async_session)
    #     print(all_tg_users)
    # except Exception as ex:
    #     print(ex)
    #
    # tu = await find_tg_user_by_chat_id(async_session, 1)
    # if tu:
    #     print(tu)
    # else:
    #     print(tu)
        # print(tu.fk_users)
    #
    # try:
    #     tu = await find_tg_user_by_chat_id(async_session, 1234)
    #     if tu:
    #         print(tu)
    #         print(tu.fk_users)
    #
    # except Exception as ex:
    #     print(ex)

    await db.engine.dispose()


if __name__ == "__main__":
    asyncio.run(async_main())
