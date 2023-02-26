from datetime import datetime

from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, BigInteger, Text

metadata = MetaData()

users = Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('username', String(20), nullable=False),
    Column('email', String(50), nullable=False, unique=True),
    Column('registered_at', TIMESTAMP, default=datetime.utcnow),
)

cars = Table(
    'cars',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('model', String(50), nullable=False),
    Column('model_name', String(50), nullable=False),
    Column('mileage', BigInteger, nullable=False),
    Column('current_mileage', BigInteger, nullable=False),
    Column('measures', String(15), nullable=False),
    Column('date_added', TIMESTAMP, default=datetime.utcnow),
    Column('description', Text, default=''),
    Column('fk_users', ForeignKey('users.id'), nullable=True),
)

tg_users = Table(
    'tg_users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('tg_users_id', BigInteger, nullable=True),
    Column('chat_id', BigInteger, nullable=False, unique=True),
    Column('tg_username', String(50), nullable=False),
    Column('tg_firstname', String(50), default=''),
    Column('tg_lastname', String(50), default=''),
    Column('fk_users', ForeignKey('users.id'), nullable=True)
)
