import uuid

from sqlalchemy import Column, ForeignKey, Integer, UUID

from src.async_db.base import Base


class MaintWork(Base):
    __tablename__ = 'maint_work'
    __table_args__ = {'extend_existing': True}

    id = Column('id', Integer, primary_key=True)
    # uuid_mw = Column('uuid', UUID, primary_key=True, default=lambda: uuid.uuid4().hex)
    fk_maintenance = Column(Integer, ForeignKey('maintenance.id', ondelete='CASCADE'),
                            nullable=False)
    fk_work = Column(Integer, ForeignKey('work.id', ondelete='CASCADE'),
                     nullable=False)

    def __init__(
            self,
            fk_maintenance,
            fk_work,
    ):
        super().__init__()
        self.fk_maintenance = fk_maintenance
        self.fk_work = fk_work


# class MaintWorkService:
#     def __init__(self, database):
#         self.db = database

    # async def m2m_maint_work(self, fk_maintenance, fk_work):
    #     async with self.db.async_session() as session:
    #         m2m_maint_work = MaintWork(
    #             fk_maintenance=fk_maintenance, fk_work=fk_work)
    #         session.add(m2m_maint_work)
    #         await session.commit()
    #         return m2m_maint_work
