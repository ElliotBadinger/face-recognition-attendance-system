from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import redis
import json
import httpx

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://facerecognition:facerecognition@postgres/facerecognition")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Redis configuration
redis_url = os.getenv("REDIS_URL", "redis://redis:6379/0")
redis_client = redis.from_url(redis_url)

# OAuth2 scheme for token authentication
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: int
    name: str
    email: str

async def verify_token(token: str = Depends(oauth2_scheme)):
    async with httpx.AsyncClient() as client:
        response = await client.get(
            "http://authentication:8000/verify-token",
            headers={"Authorization": f"Bearer {token}"}
        )
        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return response.json()

@app.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, token: str = Depends(verify_token)):
    db = SessionLocal()
    db_user = User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    db.close()

    # Cache the user data in Redis
    user_data = {"id": db_user.id, "name": db_user.name, "email": db_user.email}
    redis_client.setex(f"user:{db_user.id}", 3600, json.dumps(user_data))

    # Send notification
    await send_notification(db_user.id, f"New user created: {db_user.name}")

    return UserResponse(id=db_user.id, name=db_user.name, email=db_user.email)

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, token: str = Depends(verify_token)):
    # Try to get user data from Redis cache
    cached_user = redis_client.get(f"user:{user_id}")
    if cached_user:
        user_data = json.loads(cached_user)
        return UserResponse(**user_data)

    # If not in cache, get from database
    db = SessionLocal()
    user = db.query(User).filter(User.id == user_id).first()
    db.close()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    # Cache the user data in Redis
    user_data = {"id": user.id, "name": user.name, "email": user.email}
    redis_client.setex(f"user:{user.id}", 3600, json.dumps(user_data))

    return UserResponse(id=user.id, name=user.name, email=user.email)

@app.get("/users", response_model=list[UserResponse])
async def get_all_users(token: str = Depends(verify_token)):
    db = SessionLocal()
    users = db.query(User).all()
    db.close()
    return [UserResponse(id=user.id, name=user.name, email=user.email) for user in users]

async def send_notification(user_id: int, message: str):
    async with httpx.AsyncClient() as client:
        await client.post(
            "http://notification:8000/notifications",
            json={"user_id": str(user_id), "message": message}
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)