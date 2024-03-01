from pydantic import BaseModel, Field
from datetime import datetime


class DevicesSchema(BaseModel):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = Field(..., min_length=3, max_length=50)


class DevicesDB(DevicesSchema):
    id: int


class DeviceData(BaseModel):
    id_dev: int
    x: float
    y: float
    z: float
    timestamp: datetime = datetime.now()



