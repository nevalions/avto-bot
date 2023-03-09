from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, \
    ForeignKey, BigInteger, Text, Boolean

metadata = MetaData()

user = Table(
    'user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(20), nullable=False),
    Column('email', String(50), nullable=False, unique=True),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
)

car = Table(
    'car',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('model', String(50), nullable=False),
    Column('model_name', String(50), nullable=False),
    Column('mileage', BigInteger, nullable=False),
    Column('current_mileage', BigInteger, nullable=False),
    Column('measures', String(15), nullable=False),
    Column('date_added', TIMESTAMP, default=datetime.utcnow),
    Column('description', Text, default=''),
    Column('fk_user', ForeignKey('user.id', ondelete="CASCADE"), nullable=True),
)

tg_users = Table(
    'tg_user',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('tg_user_id', BigInteger, nullable=True),
    Column('chat_id', BigInteger, nullable=False, unique=True),
    Column('tg_username', String(50), nullable=False),
    Column('tg_firstname', String(50), default=''),
    Column('tg_lastname', String(50), default=''),
    Column('fk_user', ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
)

maintenance = Table(
    'maintenance',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(50), nullable=False),
    Column('date', TIMESTAMP, default=datetime.utcnow),
    Column('maintenance_mileage', BigInteger, nullable=False),
    Column('description', Text, default=''),
    Column('fk_car', ForeignKey('car.id', ondelete="CASCADE"), nullable=True)
)

work = Table(
    'work',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('title', String(50), nullable=False),
    Column('is_regular', Boolean, default=False),
    Column('description', Text, default=''),
    Column('next_maintenance_after', BigInteger, default=0),
    Column('is_custom', Boolean, default=False),
    Column('fk_user', ForeignKey('user.id', ondelete="CASCADE"), nullable=True)
)

maint_work = Table(
    'maint_work',
    metadata,
    Column('fk_maintenance', ForeignKey('maintenance.id', ondelete="CASCADE"),
           nullable=False, primary_key=True),
    Column('fk_work', ForeignKey('work.id', ondelete="CASCADE"), nullable=False)
)
