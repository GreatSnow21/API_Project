from typing import List
import statistics
from fastapi import APIRouter, HTTPException, Path
from datetime import datetime
from app.api import crud_devices
from app.api.models import DevicesSchema, DevicesDB, DeviceData
from app.db import database
router = APIRouter()


@router.post("/", response_model=DevicesDB, status_code=201)
async def create_device(payload: DevicesSchema):
    device_id = await crud_devices.post(payload)

    response_object = {
        "id": device_id,
        "name": payload.name,
        "description": payload.description,
    }
    return response_object


@router.get("/{id}/", response_model=DevicesDB)
async def read_devices(id: int = Path(..., gt=0),):
    devices = await crud_devices.get(id)
    if not devices:
        raise HTTPException(status_code=404, detail="Devices not found")
    return devices


@router.get("/", response_model=List[DevicesDB])
async def read_all_devices():
    return await crud_devices.get_all()


@router.put("/{id}/", response_model=DevicesDB)
async def update_devices(payload: DevicesDB, id: int = Path(..., gt=0),):
    device = await crud_devices.get(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    device_id = await crud_devices.put(id, payload)

    response_object = {
        "id": device_id,
        "name": payload.name,
        "description": payload.description,
    }
    return response_object


@router.delete("/{id}/", response_model=DevicesDB)
async def delete_device(id: int = Path(..., gt=0)):
    device = await crud_devices.get(id)
    if not device:
        raise HTTPException(status_code=404, detail="Device not found")

    await crud_devices.delete(id)

    return device


@router.post("/data/")
async def receive_data(device_data: DeviceData):
    query = "INSERT INTO device_data(id_dev, x, y, z, timestamp) VALUES (:id_dev, :x, :y, :z, :timestamp)"
    await database.execute(query, values=device_data.dict())
    return {"message": "Data received successfully"}

@router.get("/data/{uuid}")
async def read_data(id_dev: int, start_time: datetime = None, end_time: datetime = None):
    conditions = ["id_dev = :id_dev"]
    values = {"id_dev": id_dev}

    if start_time:
        conditions.append("timestamp >= :start_time")
        values["start_time"] = start_time.isoformat()
    if end_time:
        conditions.append("timestamp <= :end_time")
        values["end_time"] = end_time.isoformat()

    condition_str = " AND ".join(conditions)
    query = f"""
    SELECT * FROM device_data
    WHERE {condition_str}
    """
    data = await database.fetch_all(query, values=values)
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")

    values_list = [d["x"] + d["y"] + d["z"] for d in data]
    return {
        "min": min(values_list),
        "max": max(values_list),
        "median": statistics.median(values_list),
        "sum": sum(values_list),
        "count": len(values_list)
    }
