from app.api.models import DevicesSchema
from app.db import database, devices
"""
    Для устройств (devices) определяем CRUD методы
"""

async def post(payload: DevicesSchema):
    query = devices.insert().values(name=payload.name, description=payload.description)
    return await database.execute(query=query)


async def get(id: int):
    query = devices.select().where(id == devices.c.id)
    return await database.fetch_one(query=query)


async def get_all():
    query = devices.select()
    return await database.fetch_all(query=query)


async def put(id: int, payload: DevicesSchema):
    query = (
        devices
        .update()
        .where(id == devices.c.id)
        .values(name=payload.name, description=payload.description)
        .returning(devices.c.id)
    )
    return await database.execute(query=query)


async def delete(id: int):
    query = devices.delete().where(id == devices.c.id)
    return await database.execute(query=query)