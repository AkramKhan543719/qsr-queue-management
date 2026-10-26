
from sqlalchemy import text, desc
from contextlib import asynccontextmanager
from datetime import datetime, timedelta

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import settings
from app.database import Base, engine, get_db
from app import models, schemas


password_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title=settings.app_name,
    version="1.0.0",
    description="QSR Customer Counting and Queue Management API",
    lifespan=lifespan,
)

# Allow the local Vite frontend to communicate with FastAPI.
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://127.0.0.1:5173",
        "http://localhost:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def create_access_token(username: str) -> str:
    expires = datetime.utcnow() + timedelta(
        minutes=settings.access_token_expire_minutes
    )
    return jwt.encode(
        {"sub": username, "exp": expires},
        settings.secret_key,
        algorithm="HS256",
    )


def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
):
    error = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired token",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.secret_key, algorithms=["HS256"]
        )
        username = payload.get("sub")
        if not username:
            raise error
    except JWTError:
        raise error

    user = db.query(models.User).filter(
        models.User.username == username
    ).first()

    if not user or not user.is_active:
        raise error

    return user


@app.get("/")
def root():
    return {
        "message": "QSR Queue Management API is running",
        "docs": "/docs",
    }


@app.get("/health")
def health():
    return {"status": "healthy"}


@app.get("/health/db")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {"database": "connected"}
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database unavailable",
        )


@app.post(
    "/api/auth/register",
    response_model=schemas.UserResponse,
    status_code=201,
)
def register_user(
    data: schemas.UserCreate,
    db: Session = Depends(get_db),
):
    if db.query(models.User).filter(
        models.User.username == data.username
    ).first():
        raise HTTPException(409, "Username already exists")

    if db.query(models.User).filter(
        models.User.email == data.email
    ).first():
        raise HTTPException(409, "Email already exists")

    user = models.User(
        username=data.username,
        email=data.email,
        hashed_password=password_context.hash(data.password),
        role="admin",
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@app.post("/api/auth/login", response_model=schemas.TokenResponse)
def login(
    data: schemas.LoginRequest,
    db: Session = Depends(get_db),
):
    user = db.query(models.User).filter(
        models.User.username == data.username
    ).first()

    if not user or not password_context.verify(
        data.password, user.hashed_password
    ):
        raise HTTPException(401, "Incorrect username or password")

    if not user.is_active:
        raise HTTPException(403, "Account is disabled")

    return {
        "access_token": create_access_token(user.username),
        "token_type": "bearer",
    }


@app.get("/api/auth/me", response_model=schemas.UserResponse)
def current_user(user=Depends(get_current_user)):
    return user


@app.post(
    "/api/cameras",
    response_model=schemas.CameraResponse,
    status_code=201,
)
def create_camera(
    data: schemas.CameraCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if data.source_type not in {"video", "rtsp", "webcam"}:
        raise HTTPException(
            400, "source_type must be video, rtsp, or webcam"
        )

    camera = models.Camera(**data.model_dump())
    db.add(camera)
    db.commit()
    db.refresh(camera)
    return camera


@app.get("/api/cameras", response_model=list[schemas.CameraResponse])
def list_cameras(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(models.Camera).order_by(
        models.Camera.id.desc()
    ).all()


@app.get("/api/cameras/{camera_id}", response_model=schemas.CameraResponse)
def get_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    camera = db.query(models.Camera).filter(
        models.Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(404, "Camera not found")

    return camera


@app.patch("/api/cameras/{camera_id}/status")
def update_camera_status(
    camera_id: int,
    is_active: bool,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    camera = db.query(models.Camera).filter(
        models.Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(404, "Camera not found")

    camera.is_active = is_active
    db.commit()
    return {"camera_id": camera_id, "is_active": is_active}


@app.delete("/api/cameras/{camera_id}", status_code=204)
def delete_camera(
    camera_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    camera = db.query(models.Camera).filter(
        models.Camera.id == camera_id
    ).first()

    if not camera:
        raise HTTPException(404, "Camera not found")

    db.delete(camera)
    db.commit()


@app.post(
    "/api/queue",
    response_model=schemas.QueueRecordResponse,
    status_code=201,
)
def create_queue_record(
    data: schemas.QueueRecordCreate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    camera = db.query(models.Camera).filter(
        models.Camera.id == data.camera_id
    ).first()

    if not camera:
        raise HTTPException(404, "Camera not found")

    record = models.QueueRecord(**data.model_dump())
    db.add(record)
    db.flush()

    threshold = db.query(models.AlertThreshold).filter(
        models.AlertThreshold.is_enabled.is_(True)
    ).order_by(models.AlertThreshold.id.desc()).first()

    if threshold and record.queue_length >= threshold.max_queue_length:
        alert = models.Alert(
            camera_id=record.camera_id,
            alert_type="QUEUE_LENGTH",
            message=f"Queue length reached {record.queue_length}",
            customer_count=record.customer_count,
        )
        db.add(alert)

    if threshold and (
        record.estimated_wait_seconds >= threshold.max_wait_seconds
    ):
        alert = models.Alert(
            camera_id=record.camera_id,
            alert_type="WAIT_TIME",
            message=(
                f"Estimated wait reached "
                f"{record.estimated_wait_seconds} seconds"
            ),
            customer_count=record.customer_count,
        )
        db.add(alert)

    db.commit()
    db.refresh(record)
    return record


@app.get("/api/queue/latest")
def latest_queue(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return (
        db.query(models.QueueRecord)
        .order_by(desc(models.QueueRecord.recorded_at))
        .limit(100)
        .all()
    )


@app.get("/api/queue/history/{camera_id}")
def queue_history(
    camera_id: int,
    limit: int = 100,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    if not db.query(models.Camera).filter(
        models.Camera.id == camera_id
    ).first():
        raise HTTPException(404, "Camera not found")

    limit = max(1, min(limit, 1000))

    return (
        db.query(models.QueueRecord)
        .filter(models.QueueRecord.camera_id == camera_id)
        .order_by(desc(models.QueueRecord.recorded_at))
        .limit(limit)
        .all()
    )


@app.get("/api/alerts", response_model=list[schemas.AlertResponse])
def list_alerts(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(models.Alert).order_by(
        desc(models.Alert.created_at)
    ).limit(200).all()


@app.patch("/api/alerts/{alert_id}/acknowledge")
def acknowledge_alert(
    alert_id: int,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    alert = db.query(models.Alert).filter(
        models.Alert.id == alert_id
    ).first()

    if not alert:
        raise HTTPException(404, "Alert not found")

    alert.is_acknowledged = True
    db.commit()
    return {"id": alert.id, "is_acknowledged": True}


@app.get("/api/thresholds")
def get_thresholds(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    return db.query(models.AlertThreshold).all()


@app.put("/api/thresholds")
def update_threshold(
    data: schemas.ThresholdUpdate,
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    threshold = db.query(models.AlertThreshold).order_by(
        models.AlertThreshold.id.desc()
    ).first()

    if threshold:
        for key, value in data.model_dump().items():
            setattr(threshold, key, value)
    else:
        threshold = models.AlertThreshold(**data.model_dump())
        db.add(threshold)

    db.commit()
    db.refresh(threshold)
    return threshold


@app.get("/api/dashboard/summary")
def dashboard_summary(
    db: Session = Depends(get_db),
    user=Depends(get_current_user),
):
    cameras_total = db.query(models.Camera).count()
    cameras_active = db.query(models.Camera).filter(
        models.Camera.is_active.is_(True)
    ).count()

    latest_records = (
        db.query(models.QueueRecord)
        .order_by(desc(models.QueueRecord.recorded_at))
        .limit(100)
        .all()
    )

    unacknowledged_alerts = db.query(models.Alert).filter(
        models.Alert.is_acknowledged.is_(False)
    ).count()

    return {
        "total_cameras": cameras_total,
        "active_cameras": cameras_active,
        "latest_customer_count": (
            latest_records[0].customer_count if latest_records else 0
        ),
        "latest_queue_length": (
            latest_records[0].queue_length if latest_records else 0
        ),
        "latest_wait_seconds": (
            latest_records[0].estimated_wait_seconds
            if latest_records else 0
        ),
        "unacknowledged_alerts": unacknowledged_alerts,
        "recent_queue_records": len(latest_records),
    }
