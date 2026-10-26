from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class UserCreate(BaseModel):
    username: str = Field(min_length=3, max_length=100)
    email: str = Field(max_length=255)
    password: str = Field(min_length=8, max_length=128)


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class LoginRequest(BaseModel):
    username: str
    password: str


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class CameraCreate(BaseModel):
    name: str = Field(min_length=1, max_length=150)
    location: Optional[str] = None
    source_type: str = "video"
    source_uri: str = Field(min_length=1)
    is_active: bool = True


class CameraResponse(BaseModel):
    id: int
    name: str
    location: Optional[str] = None
    source_type: str
    source_uri: str
    is_active: bool
    created_at: datetime

    class Config:
        orm_mode = True


class QueueRecordCreate(BaseModel):
    camera_id: int
    customer_count: int = Field(ge=0)
    queue_length: int = Field(ge=0)
    estimated_wait_seconds: int = Field(ge=0)
    fps: Optional[float] = Field(default=None, ge=0)


class QueueRecordResponse(BaseModel):
    id: int
    camera_id: int
    customer_count: int
    queue_length: int
    estimated_wait_seconds: int
    fps: Optional[float] = None
    recorded_at: datetime

    class Config:
        orm_mode = True


class AlertCreate(BaseModel):
    camera_id: int
    alert_type: str
    message: str
    customer_count: int = Field(default=0, ge=0)
    evidence_path: Optional[str] = None


class AlertResponse(BaseModel):
    id: int
    camera_id: int
    alert_type: str
    message: str
    customer_count: int
    evidence_path: Optional[str] = None
    is_acknowledged: bool
    created_at: datetime

    class Config:
        orm_mode = True


class ThresholdUpdate(BaseModel):
    name: str = "Default threshold"
    max_queue_length: int = Field(default=10, ge=0)
    max_wait_seconds: int = Field(default=300, ge=0)
    is_enabled: bool = True