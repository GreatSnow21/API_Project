import os

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Float,
    MetaData,
    String,
    Table,
    ForeignKey,
    create_engine
)
from sqlalchemy.sql import func
from datetime import datetime
from databases import Database

# заменить при запуске в докере, для локального запуска
#DATABASE_URL = "postgresql://postgres:24233@127.0.0.1:5432/test_analitics"
DATABASE_URL = os.getenv("DATABASE_URL") # для докера


# SQLAlchemy создание движка
engine = create_engine(DATABASE_URL)
metadata = MetaData()
# Определяем таблицу Device
devices = Table(
    "devices",
    metadata,
    Column("id", Integer, primary_key=True, index=True), #добавляем индекс для быстрого поиска
    Column("name", String(50), index=True),
    Column("description", String, index=True)
)
device_data = Table(
    "device_data",
    metadata,
    Column("id", Integer, primary_key=True, index=True),
    Column("id_dev", Integer, ForeignKey('devices.id')),
    Column("x", Float),
    Column("y", Float),
    Column("z", Float),
    Column("timestamp", DateTime, default=datetime.utcnow())
)

# databases query builder
database = Database(DATABASE_URL)
